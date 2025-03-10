import datetime

from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class SignupView(CreateView):
    form_class = RegistrationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # messages.success(self.request, 'Registration successful. You can now log in.')
        return response

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        university_email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, university_email=university_email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid email or password')
            return self.form_invalid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

# class ProfileView(TemplateView):
#     template_name = 'users/profile.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user
#         return context
    
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

# users/views.py
# users/views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from listings.models import Listing
from borrowing.models import Borrowing


class ProfileListView(LoginRequiredMixin, ListView):
    template_name = 'users/profile.html'
    context_object_name = 'listings'


    def get_queryset(self):
        user = self.request.user
        return Listing.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = True  # Assuming this context key is needed for your template
        #
        user = self.request.user
        # user lendings
        lendings = Borrowing.objects.filter(lender=user).filter(Q(status='requested') | Q(status='returned') | Q(status='accepted'))
        context['lendings'] = lendings
        # user borrowings
        borrowings = Borrowing.objects.filter(borrower=user).filter(Q(status='requested') | Q(status='accepted') | Q(status='returned'))
        context['borrowings'] = borrowings
        # today date for jinja
        context['date'] = datetime.date.today()
        return context
