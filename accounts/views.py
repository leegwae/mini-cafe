from django.contrib.auth import login
from django.shortcuts import redirect
from django.views import generic
from rest_framework import viewsets

from .forms import UserForm
from .models import User, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignUpView(generic.CreateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

