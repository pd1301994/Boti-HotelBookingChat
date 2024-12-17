import smtplib
from email.mime.text import MIMEText
from datetime import datetime  # Importar la biblioteca para formatear fechas

def send_mail(booking_id, email_client, name, surname, entry_date, exit_date, Room_Type):
    sender_email = "botipchotels@gmail.com"
    sender_password = "gisk xakl hylw usov"
    receiver_email = email_client
    
    subject = "Booking confirmation"

    formatted_entry_date = entry_date.strftime("%d of %B de %Y")  # Ej: 14 de julio de 2025
    formatted_exit_date = exit_date.strftime("%d of %B de %Y")    # Ej: 17 de julio de 2025

    # Crear el mensaje en HTML
    body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Booking confirmation</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4; /* Fondo claro para el cuerpo */
            }}
            .container {{
                width: 90%;
                max-width: 800px;
                margin: 20px auto;
                background-color: #30275D; /* Fondo azul */
                color: white;
                border-radius: 8px;
                padding: 40px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}
            h1 {{
                color: #ECCE70;
                font-size: 32px;
                text-align: center;
                margin-bottom: 10px;
            }}
            p {{
                font-size: 20px;
                line-height: 1.5;
                margin: 10px 0;
                text-align: center;
                color: white;

            }}
            .footer {{
                margin-top: 20px;
                font-size: 16px;
                text-align: center;
                color: #d9d9d9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Booking confirmed!</h1>
                <p>Booking number: {booking_id} </p>
                <p>Dear <strong>{name} {surname}</strong>,</p>
                <p>You will be staying at <strong>PC HOTEL</strong> from <strong>{formatted_entry_date}</strong> to <strong>{formatted_exit_date}</strong>.</p>
                <p>You will have a: <strong>{Room_Type}</strong> room</p>
                <div class="footer">
                    <p>We look forward to welcoming you soon!</p>
                </div>
        </div>
    </body>
    </html>
    """

    # Crear el mensaje
    msg = MIMEText(body, "html")  # Cambiar a tipo html
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        # Conectar al servidor SMTP de Gmail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Iniciar conexión segura
            server.login(sender_email, sender_password)  # Iniciar sesión
            server.sendmail(sender_email, receiver_email, msg.as_string())  # Enviar el correo
    except Exception as e:
        print(f"Error al enviar el correo: {e}")




