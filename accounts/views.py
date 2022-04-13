from django.contrib.auth import login
from django.shortcuts import redirect
from django.views import generic

from .forms import UserForm
from .models import User


class SignUpView(generic.CreateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
