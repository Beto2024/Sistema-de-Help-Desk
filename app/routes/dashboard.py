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
    total = Ticket.query.count()
    abertos = Ticket.query.filter_by(status='aberto').count()
    em_andamento = Ticket.query.filter_by(status='em_andamento').count()
    resolvidos = Ticket.query.filter_by(status='resolvido').count()
    fechados = Ticket.query.filter_by(status='fechado').count()

    # Priority breakdown
    critica = Ticket.query.filter_by(priority='critica').count()
    alta = Ticket.query.filter_by(priority='alta').count()
    media = Ticket.query.filter_by(priority='media').count()
    baixa = Ticket.query.filter_by(priority='baixa').count()

    recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(5).all()

    my_tickets = Ticket.query.filter(
        (Ticket.creator_id == current_user.id) | (Ticket.assignee_id == current_user.id)
    ).order_by(Ticket.updated_at.desc()).limit(5).all()

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
