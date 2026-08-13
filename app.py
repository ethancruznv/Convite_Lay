from flask import Flask, request
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import gspread

app = Flask(__name__)

gc = gspread.service_account(filename='credentials.json')

PLANILHA_NOME = "Convidados_Lay"

@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/rsvp', methods=['POST'])
def rsvp():
    name = request.form.get('name')
    email = request.form.get('email')
    data_conf = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    try:
        # Abre a planilha e insere a nova linha
        sheet = gc.open(PLANILHA_NOME).sheet1
        sheet.append_row([name, email, data_conf])
    except Exception as e:
        return f"Erro ao salvar na planilha. Detalhes: {e}"
        
    return f'''
    <body style="background-color: #A31D1D; color: #F4E7C3; font-family: sans-serif; text-align: center; padding: 50px;">
        <h2>Obrigado, {name}!</h2>
        <p>Sua presença foi confirmada para o aniversário da Lay.</p>
        <a href="/" style="color: #F4E7C3; text-decoration: underline;">Voltar para o convite</a>
    </body>
    '''

@app.route('/disparar-emails-secreto')
def disparar_emails_route():
    # Proteção: a URL precisa ter ?key=LAY2026 no final
    token = request.args.get('key')
    if token != "LAY2026":
        return "Acesso negado", 403
        
    try:
        sheet = gc.open(PLANILHA_NOME).sheet1
        # Pega todos os registros. (Exige que a linha 1 na planilha tenha cabeçalhos)
        registros = sheet.get_all_records() 
        
        # Configure seu e-mail aqui
        remetente = "Meu_email@gmail.com"
        senha = "Minha_Senha" 
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente, senha)
        
        contador = 0
        for row in registros:
            destinatario = row.get('Email', '')
            nome = row.get('Nome', '')
            
            if not destinatario:
                continue
                
            msg = MIMEMultipart()
            msg['From'] = remetente
            msg['To'] = destinatario
            msg['Subject'] = "É HOJE! O Aniversário da Lay! 🪩"
            
            body = f"Olá {nome},\n\nO grande dia chegou! Estamos te esperando hoje às 19:00 para comemorar o aniversário da Lay.\nNão esqueça: Dress up, Drink, Dine & Dance!\n\nNos vemos lá!"
            msg.attach(MIMEText(body, 'plain'))
            
            server.send_message(msg)
            contador += 1
                
        server.quit()
        return f"✅ Sucesso! {contador} e-mails enviados para a lista da planilha."
        
    except Exception as e:
        return f"Erro ao enviar emails: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)