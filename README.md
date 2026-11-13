# Sistema de Gestão Comunitária da Associação Nova Esperança

MVP web para apoiar o cadastro de famílias, o registro de doações recebidas e o controle das entregas realizadas pela associação. Este repositório é um projeto acadêmico da disciplina **Projeto de Software — Experiência Prática III**. A associação e os dados de exemplo são fictícios; não cadastre dados pessoais reais neste ambiente de demonstração.

## Funcionalidades

- Cadastro e consulta de famílias atendidas.
- Registro e consulta de doações por item, quantidade e data.
- Registro de entregas vinculadas a uma família e a uma doação, com bloqueio de entregas acima do saldo disponível.
- Painel com a quantidade de doações que ainda têm saldo, sem somar unidades diferentes.

## Tecnologias

Python 3.12, Django 5.2 LTS, HTML/CSS e SQLite no desenvolvimento local. PostgreSQL pode ser configurado numa etapa posterior. A interface usa CSS local e não depende de serviços externos.

## Como executar

```text
python -m venv .venv
# Windows (PowerShell): .\.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. Para verificar o projeto, execute `python manage.py check`, `python manage.py makemigrations --check --dry-run` e `python manage.py test`. O fluxo do GitHub Actions executa essas verificações a cada envio de código.

## Fluxo de uso demonstrativo

1. Cadastre uma família fictícia com responsável, bairro e número de integrantes.
2. Registre uma doação fictícia com item, quantidade, unidade e data de recebimento.
3. Registre uma entrega, escolhendo a família e a doação. O sistema rejeita uma quantidade maior que o saldo dessa doação.
4. Consulte os registros nas páginas **Famílias**, **Doações** e **Entregas**. O saldo aparece na lista de doações.

As entidades principais são `Familia`, `Doacao` e `Entrega`. Cada entrega relaciona uma família a uma doação. Famílias e doações com entregas não podem ser excluídas em cascata, preservando o histórico.

## Estrutura

- `config/`: configurações e rotas principais do Django.
- `comunidade/`: modelos, formulários, páginas e testes do MVP.
- `comunidade/migrations/`: histórico do esquema do banco.

## Limites deste MVP

Uso local e demonstrativo. Ainda não há autenticação por voluntário, autorização por perfil, relatórios, implantação pública ou coleta de evidências com usuários externos. Antes de usar em produção, essas etapas e uma revisão de privacidade e segurança são necessárias. O painel conta doações com saldo; o valor disponível de cada item deve ser consultado na lista de doações.

## Histórico de desenvolvimento

Os commits do repositório registram a estrutura inicial, a implementação do MVP, a correção do saldo, os testes e esta documentação. Uma etapa futura poderá incluir testes com usuários e melhorias de acessibilidade.

