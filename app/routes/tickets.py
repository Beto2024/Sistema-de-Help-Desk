from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import datetime, timezone
from app import db
from app.models import Ticket, TicketHistory, Comment, User
from app.forms import TicketForm, EditTicketForm, CommentForm

tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets')

PRIORITY_ORDER = {'critica': 4, 'alta': 3, 'media': 2, 'baixa': 1}


@tickets_bp.route('/')
@login_required
def list_tickets():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    category_filter = request.args.get('category', '')
    assignee_filter = request.args.get('assignee', '')
    search = request.args.get('search', '').strip()

    query = Ticket.query

    if status_filter:
        query = query.filter(Ticket.status == status_filter)
    if priority_filter:
        query = query.filter(Ticket.priority == priority_filter)
    if category_filter:
        query = query.filter(Ticket.category == category_filter)
    if assignee_filter:
        if assignee_filter == 'me':
            query = query.filter(Ticket.assignee_id == current_user.id)
        elif assignee_filter == 'unassigned':
            query = query.filter(Ticket.assignee_id.is_(None))
        else:
            try:
                query = query.filter(Ticket.assignee_id == int(assignee_filter))
            except ValueError:
                pass
    if search:
        query = query.filter(Ticket.title.ilike(f'%{search}%'))

    tickets = query.order_by(Ticket.created_at.desc()).paginate(
        page=page, per_page=15, error_out=False)

    technicians = User.query.filter(User.role.in_(['admin', 'tecnico'])).all()

    return render_template('tickets/list.html',
                           tickets=tickets,
                           technicians=technicians,
                           status_filter=status_filter,
                           priority_filter=priority_filter,
                           category_filter=category_filter,
                           assignee_filter=assignee_filter,
                           search=search)


@tickets_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            priority=form.priority.data,
            creator_id=current_user.id,
        )
        db.session.add(ticket)
        db.session.flush()

        history = TicketHistory(
            ticket_id=ticket.id,
            user_id=current_user.id,
            field_changed='criacao',
            old_value=None,
            new_value='Chamado criado',
        )
        db.session.add(history)
        db.session.commit()

        flash('Chamado aberto com sucesso!', 'success')
        return redirect(url_for('tickets.detail', ticket_id=ticket.id))
    return render_template('tickets/create.html', form=form)


@tickets_bp.route('/<int:ticket_id>')
@login_required
def detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    comment_form = CommentForm()
    comments = ticket.comments.order_by(Comment.created_at.asc()).all()
    history = ticket.history.order_by(TicketHistory.changed_at.asc()).all()
    technicians = User.query.filter(User.role.in_(['admin', 'tecnico'])).all()
    return render_template('tickets/detail.html',
                           ticket=ticket,
                           comment_form=comment_form,
                           comments=comments,
                           history=history,
                           technicians=technicians)


@tickets_bp.route('/<int:ticket_id>/comment', methods=['POST'])
@login_required
def add_comment(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            ticket_id=ticket.id,
            user_id=current_user.id,
            content=form.content.data,
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comentário adicionado!', 'success')
    else:
        flash('Erro ao adicionar comentário.', 'danger')
    return redirect(url_for('tickets.detail', ticket_id=ticket_id))


@tickets_bp.route('/<int:ticket_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    # Only creator, admin, or assigned technician can edit
    if (current_user.id != ticket.creator_id and
            not current_user.is_admin() and
            current_user.id != ticket.assignee_id):
        flash('Você não tem permissão para editar este chamado.', 'danger')
        return redirect(url_for('tickets.detail', ticket_id=ticket_id))

    form = EditTicketForm(obj=ticket)

    # Populate assignee choices
    technicians = User.query.filter(User.role.in_(['admin', 'tecnico'])).all()
    form.assignee_id.choices = [(0, '— Sem responsável —')] + [
        (t.id, f'{t.username} ({t.role})') for t in technicians
    ]

    # Restrict status changes
    if not current_user.is_admin():
        # Non-admin cannot close tickets
        form.status.choices = [
            ('aberto', 'Aberto'),
            ('em_andamento', 'Em Andamento'),
            ('resolvido', 'Resolvido'),
        ]

    if form.validate_on_submit():
        changes = []

        if ticket.title != form.title.data:
            changes.append(('titulo', ticket.title, form.title.data))
            ticket.title = form.title.data

        if ticket.description != form.description.data:
            changes.append(('descricao', ticket.description[:100], form.description.data[:100]))
            ticket.description = form.description.data

        if ticket.category != form.category.data:
            changes.append(('categoria',
                            ticket.category_label(),
                            Ticket.CATEGORY_LABELS.get(form.category.data, form.category.data)))
            ticket.category = form.category.data

        if ticket.priority != form.priority.data:
            changes.append(('prioridade',
                            ticket.priority_label(),
                            Ticket.PRIORITY_LABELS.get(form.priority.data, form.priority.data)))
            ticket.priority = form.priority.data

        old_status = ticket.status
        if ticket.status != form.status.data:
            if form.status.data == 'fechado' and not current_user.is_admin():
                flash('Apenas administradores podem fechar chamados.', 'warning')
            else:
                changes.append(('status',
                                ticket.status_label(),
                                Ticket.STATUS_LABELS.get(form.status.data, form.status.data)))
                ticket.status = form.status.data
                if form.status.data == 'fechado':
                    ticket.closed_at = datetime.now(timezone.utc)
                elif old_status == 'fechado':
                    ticket.closed_at = None

        new_assignee_id = form.assignee_id.data if form.assignee_id.data != 0 else None
        if current_user.is_tecnico() and ticket.assignee_id != new_assignee_id:
            old_name = ticket.assignee.username if ticket.assignee else 'Nenhum'
            new_assignee = User.query.get(new_assignee_id) if new_assignee_id else None
            new_name = new_assignee.username if new_assignee else 'Nenhum'
            changes.append(('responsavel', old_name, new_name))
            ticket.assignee_id = new_assignee_id

        ticket.updated_at = datetime.now(timezone.utc)

        for field, old_val, new_val in changes:
            history = TicketHistory(
                ticket_id=ticket.id,
                user_id=current_user.id,
                field_changed=field,
                old_value=str(old_val) if old_val else None,
                new_value=str(new_val) if new_val else None,
            )
            db.session.add(history)

        db.session.commit()

        if changes:
            flash('Chamado atualizado com sucesso!', 'success')
        else:
            flash('Nenhuma alteração detectada.', 'info')

        return redirect(url_for('tickets.detail', ticket_id=ticket_id))

    # Pre-populate assignee
    if request.method == 'GET':
        form.assignee_id.data = ticket.assignee_id or 0

    return render_template('tickets/edit.html', form=form, ticket=ticket)


@tickets_bp.route('/<int:ticket_id>/assign', methods=['POST'])
@login_required
def assign(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not current_user.is_tecnico():
        flash('Apenas técnicos e administradores podem atribuir responsáveis.', 'danger')
        return redirect(url_for('tickets.detail', ticket_id=ticket_id))

    assignee_id = request.form.get('assignee_id', type=int)
    new_assignee = User.query.get(assignee_id) if assignee_id else None

    old_name = ticket.assignee.username if ticket.assignee else 'Nenhum'
    new_name = new_assignee.username if new_assignee else 'Nenhum'

    ticket.assignee_id = new_assignee.id if new_assignee else None
    ticket.updated_at = datetime.now(timezone.utc)

    history = TicketHistory(
        ticket_id=ticket.id,
        user_id=current_user.id,
        field_changed='responsavel',
        old_value=old_name,
        new_value=new_name,
    )
    db.session.add(history)
    db.session.commit()
    flash('Responsável atualizado!', 'success')
    return redirect(url_for('tickets.detail', ticket_id=ticket_id))


@tickets_bp.route('/<int:ticket_id>/status', methods=['POST'])
@login_required
def change_status(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    new_status = request.form.get('status')

    valid_statuses = ['aberto', 'em_andamento', 'resolvido', 'fechado']
    if new_status not in valid_statuses:
        flash('Status inválido.', 'danger')
        return redirect(url_for('tickets.detail', ticket_id=ticket_id))

    if new_status == 'fechado' and not current_user.is_admin():
        flash('Apenas administradores podem fechar chamados.', 'warning')
        return redirect(url_for('tickets.detail', ticket_id=ticket_id))

    if (current_user.id != ticket.creator_id and
            not current_user.is_tecnico() and
            current_user.id != ticket.assignee_id):
        flash('Você não tem permissão para alterar o status deste chamado.', 'danger')
        return redirect(url_for('tickets.detail', ticket_id=ticket_id))

    old_label = ticket.status_label()
    old_status = ticket.status
    ticket.status = new_status
    ticket.updated_at = datetime.now(timezone.utc)

    if new_status == 'fechado':
        ticket.closed_at = datetime.now(timezone.utc)
    elif old_status == 'fechado':
        ticket.closed_at = None

    history = TicketHistory(
        ticket_id=ticket.id,
        user_id=current_user.id,
        field_changed='status',
        old_value=old_label,
        new_value=ticket.status_label(),
    )
    db.session.add(history)
    db.session.commit()
    flash('Status atualizado!', 'success')
    return redirect(url_for('tickets.detail', ticket_id=ticket_id))
