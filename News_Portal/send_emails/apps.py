from django.apps import AppConfig


class SendEmailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'send_emails'
    
    def ready(self):  
        import send_emails.signals
