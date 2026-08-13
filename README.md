# Convite Online - Save the Date (Lay)

Este projeto contém o código completo para rodar o site do convite, gerenciar as confirmações de presença (RSVP) e disparar o e-mail no dia da festa.

## Arquivos:
- `index.html`: O visual do site (contador, design e formulário).
- `app.py`: O servidor backend (feito em Python/Flask) que processa as confirmações e salva numa planilha, além de conter a função de disparar e-mails.
- `convidados.csv`: (Será criado automaticamente) Planilha onde os nomes e e-mails confirmados serão salvos.

## Como usar (Passo a passo):

1. **Instale os requisitos:**
   Certifique-se de ter o Python instalado. No seu terminal, instale o framework Flask:
   `pip install flask`

2. **Rodar o site do convite:**
   Abra o terminal na pasta deste projeto e execute:
   `python app.py`
   Acesse no seu navegador: `http://127.0.0.1:5000`

3. **Confirmações (RSVP):**
   Conforme as pessoas preencherem o formulário no site, os dados serão salvos no arquivo `convidados.csv`.

4. **Enviar os e-mails no dia 11 de Setembro:**
   - Abra o arquivo `app.py` em um bloco de notas.
   - Procure a função `enviar_emails_no_dia()`.
   - Substitua `SEU_EMAIL@gmail.com` pelo seu Gmail e `SUA_SENHA_DE_APLICATIVO` pela sua senha de app (você gera isso nas configurações de segurança da sua conta Google).
   - No dia da festa, abra o terminal na pasta do projeto e rode:
     `python app.py enviar_emails`
