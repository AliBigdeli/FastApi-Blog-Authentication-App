import pathlib
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from core.config import settings
from pydantic import EmailStr
from fastapi import HTTPException
from jinja2 import Template

# Define mail sender settings
conf = ConnectionConfig(
    MAIL_SERVER=settings.EMAIL_HOST,
    MAIL_USERNAME=settings.EMAIL_HOST_USER,
    MAIL_PASSWORD=settings.EMAIL_HOST_PASSWORD,
    MAIL_PORT=settings.EMAIL_HOST_PORT,
    MAIL_STARTTLS=settings.EMAIL_USE_STARTTLS,
    MAIL_SSL_TLS=settings.EMAIL_USE_SSL_TLS,
    MAIL_FROM=settings.EMAIL_DEFAULT_FROM,
)

# Create a mail sender client
mail = FastMail(conf)


async def send_email(to: EmailStr, subject: str, html_path=None,template_kwargs={}, body=None,silent=True):
    html_body = ''
    if html_path:
        try:
            html_body = pathlib.Path(html_path).read_text()
        except FileNotFoundError:
            if not silent:
                raise
            return
    if template_kwargs:
        template = Template(html_body)
        html_content = template.render(template_kwargs)
        html_body = html_content
    message = MessageSchema(
        subject=subject,
        recipients=[to],
        body=body or html_body,
        subtype="html"
    )
    try:
        await mail.send_message(message)
    except Exception as e:
        if not silent:
            raise HTTPException(status_code=500, detail=str(e))
