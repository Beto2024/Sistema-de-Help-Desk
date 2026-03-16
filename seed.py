"""
Script para popular o banco de dados com dados de exemplo.
Execute: python seed.py
"""
from app import create_app, db
from app.models import User, Ticket, TicketHistory, Comment
from datetime import datetime, timedelta, timezone
import random

app = create_app()

with app.app_context():
    # Drop all and recreate
    db.drop_all()
    db.create_all()

    print("Criando usuários...")

    # Admin
    admin = User(username='admin', email='admin@helpdesk.com', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)

    # Technicians
    tec1 = User(username='carlos_tec', email='carlos@helpdesk.com', role='tecnico')
    tec1.set_password('tec123')
    db.session.add(tec1)

    tec2 = User(username='ana_tec', email='ana@helpdesk.com', role='tecnico')
    tec2.set_password('tec123')
    db.session.add(tec2)

    # Regular users
    u1 = User(username='joao_silva', email='joao@empresa.com', role='usuario')
    u1.set_password('user123')
    db.session.add(u1)

    u2 = User(username='maria_santos', email='maria@empresa.com', role='usuario')
    u2.set_password('user123')
    db.session.add(u2)

    u3 = User(username='pedro_costa', email='pedro@empresa.com', role='usuario')
    u3.set_password('user123')
    db.session.add(u3)

    db.session.flush()

    print("Criando chamados de exemplo...")

    tickets_data = [
        {
            'title': 'Computador não liga após queda de energia',
            'description': 'O computador da sala de reuniões parou de funcionar após uma queda de energia. Ao tentar ligar, nenhuma luz acende e não há sinal de vida no equipamento.',
            'category': 'hardware',
            'priority': 'alta',
            'status': 'aberto',
            'creator': u1,
            'assignee': tec1,
        },
        {
            'title': 'Erro ao acessar sistema ERP',
            'description': 'Ao tentar acessar o sistema ERP, aparece a mensagem "Erro 503 - Serviço indisponível". O problema ocorre para todos os usuários do departamento financeiro desde às 09h de hoje.',
            'category': 'software',
            'priority': 'critica',
            'status': 'em_andamento',
            'creator': u2,
            'assignee': tec2,
        },
        {
            'title': 'Impressora do andar 3 não imprime',
            'description': 'A impressora HP LaserJet do 3º andar não está imprimindo. Os documentos ficam na fila mas não saem. Já tentei reiniciar o equipamento sem sucesso.',
            'category': 'hardware',
            'priority': 'media',
            'status': 'em_andamento',
            'creator': u3,
            'assignee': tec1,
        },
        {
            'title': 'Sem acesso à internet no setor de vendas',
            'description': 'Todos os computadores do setor de vendas perderam acesso à internet às 14h30. A rede interna funciona normalmente. O switch local foi reiniciado mas o problema persiste.',
            'category': 'rede',
            'priority': 'alta',
            'status': 'aberto',
            'creator': u1,
            'assignee': None,
        },
        {
            'title': 'Solicitar criação de conta no Active Directory',
            'description': 'Preciso criar uma conta de acesso para o novo colaborador João Pedro Alves, que iniciará na próxima segunda-feira no departamento de RH.',
            'category': 'acesso',
            'priority': 'baixa',
            'status': 'resolvido',
            'creator': u2,
            'assignee': admin,
        },
        {
            'title': 'Microsoft Office apresentando erros',
            'description': 'O Microsoft Word fecha inesperadamente ao tentar salvar documentos com tamanho superior a 10MB. O problema ocorre nas máquinas do setor de engenharia.',
            'category': 'software',
            'priority': 'media',
            'status': 'aberto',
            'creator': u3,
            'assignee': tec2,
        },
        {
            'title': 'Cabo de rede danificado na sala 205',
            'description': 'O cabo de rede do computador 205-03 está com defeito físico visível. A conexão cai a cada 5-10 minutos. Necessário substituição urgente.',
            'category': 'rede',
            'priority': 'baixa',
            'status': 'fechado',
            'creator': u1,
            'assignee': tec1,
        },
        {
            'title': 'Tela do notebook com linhas verticais',
            'description': 'O notebook do gerente de projetos apresenta linhas verticais coloridas na tela. O problema apareceu após uma queda leve. Equipamento ainda funciona mas a visualização está comprometida.',
            'category': 'hardware',
            'priority': 'media',
            'status': 'em_andamento',
            'creator': u2,
            'assignee': tec1,
        },
        {
            'title': 'VPN não conecta fora do escritório',
            'description': 'Após a atualização do Windows realizada ontem, a VPN corporativa não consegue mais estabelecer conexão quando acesso de casa. Recebo a mensagem "Autenticação falhou".',
            'category': 'acesso',
            'priority': 'alta',
            'status': 'aberto',
            'creator': u3,
            'assignee': tec2,
        },
        {
            'title': 'Atualização de drivers solicitada',
            'description': 'Os drivers da placa de vídeo nos computadores do estúdio criativo estão desatualizados, causando travamentos durante o uso de software de edição de imagem.',
            'category': 'software',
            'priority': 'baixa',
            'status': 'resolvido',
            'creator': u1,
            'assignee': tec2,
        },
    ]

    created_tickets = []
    base_date = datetime.now(timezone.utc) - timedelta(days=30)

    for i, data in enumerate(tickets_data):
        t = Ticket(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            priority=data['priority'],
            status=data['status'],
            creator_id=data['creator'].id,
            assignee_id=data['assignee'].id if data['assignee'] else None,
            created_at=base_date + timedelta(days=i * 3, hours=random.randint(8, 17)),
            updated_at=base_date + timedelta(days=i * 3 + random.randint(1, 2)),
        )
        if data['status'] == 'fechado':
            t.closed_at = t.updated_at
        db.session.add(t)
        created_tickets.append(t)

    db.session.flush()

    print("Criando histórico...")

    for ticket in created_tickets:
        # Creation entry
        history_create = TicketHistory(
            ticket_id=ticket.id,
            user_id=ticket.creator_id,
            field_changed='criacao',
            old_value=None,
            new_value='Chamado criado',
            changed_at=ticket.created_at,
        )
        db.session.add(history_create)

        # Assignee history if assigned
        if ticket.assignee_id:
            assignee = User.query.get(ticket.assignee_id)
            history_assign = TicketHistory(
                ticket_id=ticket.id,
                user_id=admin.id,
                field_changed='responsavel',
                old_value='Nenhum',
                new_value=assignee.username,
                changed_at=ticket.created_at + timedelta(hours=1),
            )
            db.session.add(history_assign)

        # Status history for non-open tickets
        if ticket.status in ('em_andamento', 'resolvido', 'fechado'):
            history_status = TicketHistory(
                ticket_id=ticket.id,
                user_id=ticket.assignee_id or admin.id,
                field_changed='status',
                old_value='Aberto',
                new_value='Em Andamento',
                changed_at=ticket.created_at + timedelta(hours=2),
            )
            db.session.add(history_status)

        if ticket.status in ('resolvido', 'fechado'):
            history_resolved = TicketHistory(
                ticket_id=ticket.id,
                user_id=ticket.assignee_id or admin.id,
                field_changed='status',
                old_value='Em Andamento',
                new_value='Resolvido' if ticket.status == 'resolvido' else 'Fechado',
                changed_at=ticket.updated_at,
            )
            db.session.add(history_resolved)

    print("Criando comentários...")

    comments_data = [
        (created_tickets[0], tec1, 'Vou verificar o equipamento ainda hoje. Qual é a localização exata da sala de reuniões?'),
        (created_tickets[0], u1, 'É na sala de reuniões principal, 2º andar, ao lado da copa.'),
        (created_tickets[1], tec2, 'Identifiquei o problema: o servidor de aplicação travou. Estou reiniciando os serviços.'),
        (created_tickets[1], u2, 'Ótimo, aguardamos normalização. O departamento financeiro está parado.'),
        (created_tickets[1], tec2, 'Serviços reiniciados. Por favor, teste o acesso e confirme se está funcionando.'),
        (created_tickets[2], tec1, 'Verificado: o cartucho de toner está vazio e há um papel preso internamente. Vou providenciar a troca.'),
        (created_tickets[4], admin, 'Conta criada no AD com acesso básico ao sistema. Senha temporária enviada por e-mail.'),
        (created_tickets[6], tec1, 'Cabo substituído. Por favor, confirme se a conexão está estável agora.'),
        (created_tickets[6], u1, 'Confirmado! Conexão estável há mais de 2 horas. Obrigado!'),
        (created_tickets[9], tec2, 'Drivers atualizados em todos os 5 computadores do estúdio. Favor testar e confirmar.'),
    ]

    for ticket, author, content in comments_data:
        comment = Comment(
            ticket_id=ticket.id,
            user_id=author.id,
            content=content,
            created_at=ticket.created_at + timedelta(hours=random.randint(2, 24)),
        )
        db.session.add(comment)

    db.session.commit()

    print("\n✅ Banco de dados populado com sucesso!")
    print("\n📋 Credenciais de acesso:")
    print("  👑 Admin:    admin / admin123")
    print("  🔧 Técnico:  carlos_tec / tec123")
    print("  🔧 Técnico:  ana_tec / tec123")
    print("  👤 Usuário:  joao_silva / user123")
    print("  👤 Usuário:  maria_santos / user123")
    print("  👤 Usuário:  pedro_costa / user123")
    print(f"\n📊 Criados: {len(created_tickets)} chamados, comentários e histórico.")
