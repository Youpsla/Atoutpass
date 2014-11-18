# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse

# view imports
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import ListView

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from .forms import UserForm

# Import the customized User model
from .models import User

# Import necessary for integrating first_name and last_name forn in Agent
from agent.models import Agent

# import messages
from django.contrib import messages

from django.http import HttpResponseRedirect

from agent.views import agent_form_redirect 

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = UserForm
    template_name = 'agent/profile.html'

    # we already imported User in the view code above, remember?
    model = User

    def get_object(self):
        # Only get the User record for the user making the request
        Agent.objects.get_or_create(user=self.request.user)
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


    # send the user back to their own page after a successful update
    def get_success_url(self):
        # Retrieve form_state from DB
        form_state = Agent.objects.get(user=self.request.user).form_state

        # Set redirect_url by passing form_state to agent_form_redirect
        redirect_url = agent_form_redirect(form_state)
        
        # Check if agent form is complete
        if 0 in form_state.values():
            print 'Le formulaire est INCOMPLET'
            messages.add_message(self.request, messages.ERROR, u'Votre Profil est incomplet. Veuillez renseigner les formulaires des onglets encore en rouge.')
        else:
            print 'Le formulaire est COMPLET'
            messages.add_message(self.request, messages.SUCCESS, u'Merci. Votre profil va maintenant etre communiqué a un conseiller. Vous serez contacté dans les plus brefs délais')

        # Update messages
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')
        return reverse(redirect_url)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
