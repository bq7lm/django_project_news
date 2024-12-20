from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from allauth.account.forms import LoginForm
from django import forms


class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
        