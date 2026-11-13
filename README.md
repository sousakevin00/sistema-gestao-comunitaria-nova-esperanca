# Sistema de Gestão Comunitária da Associação Nova Esperança

MVP web para apoiar o cadastro de famílias, o registro de doações recebidas e o controle das entregas realizadas pela associação. Este repositório é um projeto acadêmico da disciplina **Projeto de Software — Experiência Prática III**. A associação e os dados de exemplo são fictícios; não cadastre dados pessoais reais neste ambiente de demonstração.

## Funcionalidades

- Cadastro e consulta de famílias atendidas.
- Registro e consulta de doações por item, quantidade e data.
- Registro de entregas vinculadas a uma família e a uma doação, com bloqueio de entregas acima do saldo disponível.
- Painel com totais e saldos das doações.

## Tecnologias

Python 3.12, Django 5.2 LTS, HTML/CSS e SQLite no desenvolvimento local. PostgreSQL pode ser configurado numa etapa posterior. A interface usa CSS local e não depende de serviços externos.

## Como executar

```bash
python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. Para verificar o projeto, execute `python manage.py test`.

## Estrutura

- `config/`: configurações e rotas principais do Django.
- `comunidade/`: modelos, formulários, páginas e testes do MVP.
- `comunidade/migrations/`: histórico do esquema do banco.

## Limites deste MVP

Uso local e demonstrativo. Ainda não há autenticação por voluntário, autorização por perfil, relatórios, implantação pública ou coleta de evidências com usuários externos. Antes de usar em produção, essas etapas e uma revisão de privacidade e segurança são necessárias. A soma de itens no painel é apenas ilustrativa e não substitui o saldo por tipo de doação.

## Histórico de desenvolvimento

Os commits do repositório registram a estrutura inicial e a implementação do MVP. As entregas seguintes poderão incluir testes com usuários, integração contínua e melhorias de acessibilidade.
