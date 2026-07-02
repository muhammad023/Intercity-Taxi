import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email,code):
    sender_email = "abdullaevmuhammad187@gmail.com"
    password = "ldclpsixspxrfwvb"



    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = """\
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>OTP Code</title>
            </head>
            <body style="margin:0; padding:0; background:#f4f4f4; font-family:Arial, sans-serif;">

                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                        <td align="center" style="padding: 40px 0;">

                            <table width="400" cellpadding="0" cellspacing="0" border="0" 
                                   style="background:#ffffff; border-radius:10px; padding:30px; box-shadow:0 5px 15px rgba(0,0,0,0.1);">

                                <tr>
                                    <td align="center">
                                        <h2 style="color:#333;">Tasdiqlash kodi</h2>
                                        <p style="color:#666; font-size:14px;">
                                            Siz ro‘yxatdan o‘tish uchun quyidagi koddan foydalaning:
                                        </p>
                                    </td>
                                </tr>

                                <tr>
                                    <td align="center" style="padding:20px 0;">
                                        <div style="
                                            display:inline-block;
                                            padding:15px 30px;
                                            font-size:28px;
                                            font-weight:bold;
                                            letter-spacing:5px;
                                            background:#667eea;
                                            color:#fff;
                                            border-radius:8px;">
                                            {code}
                                        </div>
                                    </td>
                                </tr>

                                <tr>
                                    <td align="center">
                                        <p style="color:#888; font-size:13px;">
                                            Bu kod 6 soniya davomida amal qiladi.
                                        </p>
                                        <p style="color:#888; font-size:13px;">
                                            Agar siz bu so‘rovni yubormagan bo‘lsangiz, e’tibor bermang.
                                        </p>
                                    </td>
                                </tr> 

                                <tr>
                                    <td align="center" style="padding-top:20px;">
                                        <p style="font-size:12px; color:#aaa;">
                                            © 2026 Your Company
                                        </p>
                                    </td>
                                </tr>

                            </table>

                        </td>
                    </tr>
                </table>

            </body>
            </html>

        """

    html = html.format(code=code)

    part2 = MIMEText(html, "html")

    message.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )