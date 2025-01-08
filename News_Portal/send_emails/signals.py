from allauth.account.signals import user_signed_up  
from django.dispatch import receiver  
from allauth.account.utils import send_email_confirmation  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.http import urlsafe_base64_encode  
from django.utils.encoding import force_bytes  
from django.template.loader import render_to_string  
from django.utils import timezone  


from allauth.account.signals import email_confirmed   
from django.core.mail import send_mail  
from django.conf import settings
  
# Благодарность за подтверждение
@receiver(email_confirmed)  
def email_confirmed_handler(request, email_address, **kwargs):  
    subject = "Спасибо за подтверждение вашей электронной почты!"  
    message = "Добро пожаловать! Спасибо за подтверждение вашей электронной почты."  
    email_from = settings.DEFAULT_FROM_EMAIL  
    recipient_list = [email_address.email]  

    send_mail(subject, message, email_from, recipient_list)  

# Подтверждение почты после регистрации    
@receiver(user_signed_up)  
def user_signed_up_handler(request, user, **kwargs):  
    send_email_confirmation(request, user)