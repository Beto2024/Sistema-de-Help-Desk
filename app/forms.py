from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField,
                     SelectField, SubmitField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(message='Campo obrigatório.')])
    password = PasswordField('Senha', validators=[DataRequired(message='Campo obrigatório.')])
    submit = SubmitField('Entrar')


class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired(message='Campo obrigatório.'),
        Length(min=3, max=64, message='O usuário deve ter entre 3 e 64 caracteres.')
    ])
    email = StringField('E-mail', validators=[
        DataRequired(message='Campo obrigatório.'),
        Email(message='E-mail inválido.')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Campo obrigatório.'),
        Length(min=6, message='A senha deve ter pelo menos 6 caracteres.')
    ])
    password2 = PasswordField('Confirmar Senha', validators=[
        DataRequired(message='Campo obrigatório.'),
        EqualTo('password', message='As senhas não coincidem.')
    ])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nome de usuário já está em uso.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este e-mail já está em uso.')


class TicketForm(FlaskForm):
    title = StringField('Título', validators=[
        DataRequired(message='Campo obrigatório.'),
        Length(max=200, message='O título deve ter no máximo 200 caracteres.')
    ])
    description = TextAreaField('Descrição', validators=[
        DataRequired(message='Campo obrigatório.')
    ])
    category = SelectField('Categoria', choices=[
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('rede', 'Rede'),
        ('acesso', 'Acesso'),
        ('outro', 'Outro'),
    ], validators=[DataRequired()])
    priority = SelectField('Prioridade', choices=[
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ], validators=[DataRequired()])
    submit = SubmitField('Abrir Chamado')


class EditTicketForm(FlaskForm):
    title = StringField('Título', validators=[
        DataRequired(message='Campo obrigatório.'),
        Length(max=200)
    ])
    description = TextAreaField('Descrição', validators=[
        DataRequired(message='Campo obrigatório.')
    ])
    category = SelectField('Categoria', choices=[
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('rede', 'Rede'),
        ('acesso', 'Acesso'),
        ('outro', 'Outro'),
    ])
    priority = SelectField('Prioridade', choices=[
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ])
    status = SelectField('Status', choices=[
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('resolvido', 'Resolvido'),
        ('fechado', 'Fechado'),
    ])
    assignee_id = SelectField('Responsável', coerce=int)
    submit = SubmitField('Salvar Alterações')


class CommentForm(FlaskForm):
    content = TextAreaField('Comentário', validators=[
        DataRequired(message='Campo obrigatório.')
    ])
    submit = SubmitField('Adicionar Comentário')
