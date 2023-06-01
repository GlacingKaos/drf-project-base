import environ
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

env = environ.Env()


class Util:
    @staticmethod
    def send_email(data):
        message = Mail(
            from_email=env.str("DEFAULT_FROM_EMAIL"),
            to_emails=data["to"],
            subject=data["subject"],
            html_content=data["email_body"],
        )
        try:
            sg = SendGridAPIClient(env.str("SENDGRID_API_KEY"))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(str(e))
