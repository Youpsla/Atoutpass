# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse

# view imports
from django.views.generic import UpdateView

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from .forms import UserFormUpdate

# Import the customized User model
from .models import User

# import messages
from django.contrib import messages

from django.http import HttpResponseRedirect

from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from config.common import Common

# Decorator for setting the user type : agent or client
@receiver(user_signed_up)
def set_type(sender, **kwargs):
    print kwargs['request']
    user = kwargs.pop('user')
    print "USER SIGN UP SIGNAL : ", user.__dict__
    if type == 'client':
        # because the default is agent.
        user.type = 'client'
    user.save()

#from allauth.account.views import SignupView
#class LocalSignupView(SignupView):

    #def form_valid(self, form):
        #url = self.request.path
        #print "UUURRRLLL : ", url
        #form = form.save(commit=False)
        #form.type = self.request
        #form.save()
        #return HttpResponseRedirect(self.get_success_url())


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = Common.AUTH_USER_MODEL
    form_class = UserFormUpdate
    template_name = 'users/user_form.html'

    # Define the redirect URL depending on user.type.
    def get_success_url(self):
        if self.request.user.type == 'CL':
            return reverse("clients:client_home",)
        else:
            return reverse("agent:~agent_home",
                           kwargs={"pk": self.request.user})

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)


