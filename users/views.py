from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from .serializers import UserForm

# Create your views here.
class UserCreate(CreateView):
    form_class = UserForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        user = form.save()
        return super(UserCreate, self).form_valid(form) 



class SuccessView(TemplateView):
    template_name = 'registration/success.html'
