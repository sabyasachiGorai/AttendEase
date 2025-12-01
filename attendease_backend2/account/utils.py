# from django.core.mail import EmailMessage
# from django.conf import settings

# class Util:
#   @staticmethod
#   def send_email(data):
#     email = EmailMessage(
#           subject=data['subject'],
#           body=data['body'],
#           from_email=settings.EMAIL_FROM,
#           to=[data['to_email']]
#     )
#     email.content_subtype = "html"
#     email.send()

# account/utils.py
import logging
from django.conf import settings
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException

logger = logging.getLogger(__name__)

class Util:
    @staticmethod
    def send_email(data):
        """
        data dict must contain:
          - to_email: str
          - subject: str
          - body: str (HTML)
        Returns True on success, False on failure.
        """
        try:
            configuration = Configuration()
            configuration.api_key['api-key'] = settings.BREVO_API_KEY

            api_instance = TransactionalEmailsApi(ApiClient(configuration))

            email = SendSmtpEmail(
                to=[{"email": data["to_email"]}],
                sender={"email": settings.BREVO_SENDER_EMAIL},
                subject=data["subject"],
                html_content=data["body"]
            )

            api_instance.send_transac_email(email)
            logger.info("Sent email to %s subject=%s", data["to_email"], data["subject"])
            return True

        except ApiException as e:
            # Brevo API client error (HTTP error, invalid payload, etc.)
            logger.exception("Brevo ApiException: %s", getattr(e, "body", str(e)))
            return False
        except Exception as e:
            # Unexpected error (network, config)
            logger.exception("Unexpected error sending email: %s", e)
            return False
