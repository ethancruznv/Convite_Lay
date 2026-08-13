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
        sheet = gc.open(PLANILHA_NOME).sheet1
        sheet.append_row([name, email, data_conf])
    except Exception as e:
        return f"Erro ao salvar na planilha. Detalhes: {e}"
        
    # HTML atualizado da página de confirmação centralizada e com confetes!
    return f'''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Presença Confirmada!</title>
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Bebas+Neue&display=swap');
            body {{
                background-color: #A31D1D;
                color: #F4E7C3;
                font-family: 'Playfair Display', serif;
                text-align: center;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-image: radial-gradient(circle, #b82121 0%, #7a1212 100%);
                overflow: hidden; /* Evita barra de rolagem com os confetes */
            }}
            .msg-box {{
                background: rgba(0,0,0,0.25);
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                max-width: 90%;
                z-index: 10;
            }}
            h2 {{
                font-family: 'Bebas Neue', sans-serif;
                font-size: 3em;
                letter-spacing: 2px;
                margin-top: 0;
            }}
            p {{
                font-size: 1.3em;
                margin-bottom: 10px;
            }}
            .btn-voltar {{
                display: inline-block;
                background-color: #F4E7C3;
                color: #A31D1D;
                text-decoration: none;
                padding: 15px 30px;
                font-family: 'Bebas Neue', sans-serif;
                font-size: 1.2em;
                letter-spacing: 2px;
                border-radius: 4px;
                transition: transform 0.2s;
            }}
            .btn-voltar:hover {{
                transform: scale(1.05);
                background-color: #fff;
            }}
        </style>
    </head>
    <body>
        <div class="msg-box">
            <h2>PRESENÇA CONFIRMADA!</h2>
            <p>Obrigado, <strong>{name}</strong>!<br>Sua presença no aniversário da Lay foi registrada com sucesso.</p>
            <a href="/" class="btn-voltar">VOLTAR PARA O CONVITE</a>
        </div>
        <script>
            // Dispara os confetes automaticamente ao carregar a página
            var duration = 3 * 1000;
            var end = Date.now() + duration;

            (function frame() {{
                confetti({{
                    particleCount: 5,
                    angle: 60,
                    spread: 55,
                    origin: {{ x: 0 }},
                    colors: ['#F4E7C3', '#ffffff', '#FFD700']
                }});
                confetti({{
                    particleCount: 5,
                    angle: 120,
                    spread: 55,
                    origin: {{ x: 1 }},
                    colors: ['#F4E7C3', '#ffffff', '#FFD700']
                }});

                if (Date.now() < end) {{
                    requestAnimationFrame(frame);
                }}
            }}());
        </script>
    </body>
    </html>
    '''

@app.route('/disparar-emails-secreto')
def disparar_emails_route():
    token = request.args.get('key')
    if token != "LAY2026":
        return "Acesso negado", 403
        
    try:
        sheet = gc.open(PLANILHA_NOME).sheet1
        registros = sheet.get_all_records() 
        
        remetente = "SEU_EMAIL@gmail.com"
        senha = "SUA_SENHA_DE_APLICATIVO" 
        
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
            
            body = f"""Olá {nome},

O grande dia chegou! Estamos te esperando hoje às 19:00 para comemorar o aniversário da Lay.
Não esqueça: Dress up, Drink, Karaoke & Dance!

Nos vemos lá!
"""
            msg.attach(MIMEText(body, 'plain'))
            
            server.send_message(msg)
            contador += 1
                
        server.quit()
        return f"✅ Sucesso! {contador} e-mails enviados para a lista da planilha."
        
    except Exception as e:
        return f"Erro ao enviar emails: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
