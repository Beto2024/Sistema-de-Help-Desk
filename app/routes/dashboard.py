from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Ticket, User
from app import db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        base_query = Ticket.query
    elif current_user.role == 'tecnico':
        base_query = Ticket.query.filter(
            (Ticket.assignee_id == current_user.id) | (Ticket.creator_id == current_user.id)
        )
    else:  # usuario
        base_query = Ticket.query.filter(Ticket.creator_id == current_user.id)

    total = base_query.count()
    abertos = base_query.filter(Ticket.status == 'aberto').count()
    em_andamento = base_query.filter(Ticket.status == 'em_andamento').count()
    resolvidos = base_query.filter(Ticket.status == 'resolvido').count()
    fechados = base_query.filter(Ticket.status == 'fechado').count()

    # Priority breakdown
    critica = base_query.filter(Ticket.priority == 'critica').count()
    alta = base_query.filter(Ticket.priority == 'alta').count()
    media = base_query.filter(Ticket.priority == 'media').count()
    baixa = base_query.filter(Ticket.priority == 'baixa').count()

    recent_tickets = base_query.order_by(Ticket.created_at.desc()).limit(5).all()
    my_tickets = base_query.order_by(Ticket.updated_at.desc()).limit(5).all()

    return render_template('dashboard/index.html',
                           total=total,
                           abertos=abertos,
                           em_andamento=em_andamento,
                           resolvidos=resolvidos,
                           fechados=fechados,
                           critica=critica,
                           alta=alta,
                           media=media,
                           baixa=baixa,
                           recent_tickets=recent_tickets,
                           my_tickets=my_tickets)
