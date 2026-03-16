# 🎫 Sistema de Help Desk

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=flat&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3.1.1-D71F00?style=flat)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-CDN-06B6D4?style=flat&logo=tailwindcss&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

Plataforma completa de abertura e acompanhamento de chamados técnicos com **dark theme**, níveis de prioridade, atribuição de responsáveis e histórico de alterações.

## ✨ Funcionalidades

- 🔐 **Autenticação** — Login, registro e controle de acesso por perfil (admin, técnico, usuário)
- 📊 **Dashboard** — Visão geral com contadores, distribuição por prioridade e chamados recentes
- 🎫 **Gestão de Chamados** — Criar, visualizar, editar e filtrar chamados técnicos
- 🏷️ **Prioridades** — Baixa, Média, Alta e Crítica com badges coloridas
- 📋 **Status** — Aberto, Em Andamento, Resolvido e Fechado
- 👤 **Atribuição** — Designar técnicos responsáveis pelos chamados
- 💬 **Comentários** — Discussão diretamente no chamado
- 📜 **Histórico** — Timeline completo de todas as alterações realizadas
- 🔍 **Filtros e Busca** — Por status, prioridade, categoria e responsável
- 📱 **Responsivo** — Interface adaptada para mobile e desktop

## 🎨 Design

Dark theme com paleta de cores profissional:

| Token | Cor | Uso |
|---|---|---|
| `bg-primary` | `#0f172a` | Fundo principal |
| `bg-secondary` | `#1e293b` | Cards e painéis |
| `accent-amber` | `#f59e0b` | Destaques e botões |
| `accent-green` | `#22c55e` | Status ativo / sucesso |
| `accent-red` | `#ef4444` | Prioridade crítica / erros |
| `accent-blue` | `#3b82f6` | Badges informativas |

Cards com **bordas gradiente âmbar → vermelho** e efeito glow sutil.

## 🛠️ Tecnologias

- **Python 3.10+** + **Flask 3.0**
- **Flask-SQLAlchemy** — ORM com SQLite
- **Flask-Login** — Gerenciamento de sessões
- **Flask-WTF** — Formulários com proteção CSRF
- **Werkzeug** — Hash seguro de senhas
- **Tailwind CSS** — Estilização via CDN
- **Jinja2** — Templates HTML

## 🚀 Como Instalar e Rodar

### 1. Clone o repositório

```bash
git clone https://github.com/Beto2024/10-Sistema-de-Help-Desk.git
cd 10-Sistema-de-Help-Desk
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Popule o banco com dados de exemplo (opcional)

```bash
python seed.py
```

### 5. Inicie a aplicação

```bash
python run.py
```

Acesse: **http://localhost:5000**

## 🔑 Credenciais Padrão (após `seed.py`)

| Perfil | Usuário | Senha |
|---|---|---|
| 👑 Administrador | `admin` | `admin123` |
| 🔧 Técnico | `carlos_tec` | `tec123` |
| 🔧 Técnico | `ana_tec` | `tec123` |
| 👤 Usuário | `joao_silva` | `user123` |
| 👤 Usuário | `maria_santos` | `user123` |
| 👤 Usuário | `pedro_costa` | `user123` |

## 📁 Estrutura do Projeto

```
10-Sistema-de-Help-Desk/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # Modelos: User, Ticket, TicketHistory, Comment
│   ├── forms.py             # Formulários WTF
│   ├── routes/
│   │   ├── auth.py          # Login, registro, logout
│   │   ├── tickets.py       # CRUD de chamados
│   │   └── dashboard.py     # Dashboard e métricas
│   ├── templates/
│   │   ├── base.html         # Template base com Navbar
│   │   ├── auth/             # Login e Registro
│   │   ├── tickets/          # Lista, Criar, Detalhe, Editar
│   │   ├── dashboard/        # Dashboard
│   │   └── errors/           # 404 e 500
│   └── static/css/
│       └── custom.css        # Estilos: badges, gradientes, glow
├── config.py
├── run.py
├── seed.py
└── requirements.txt
```

## 📊 Modelos de Dados

- **User** — Usuários com perfis (admin, tecnico, usuario)
- **Ticket** — Chamados com título, descrição, categoria, prioridade, status
- **TicketHistory** — Log de todas as alterações com valores antigo/novo
- **Comment** — Comentários vinculados aos chamados

## 📜 Licença

MIT — veja [LICENSE](LICENSE) para detalhes.
