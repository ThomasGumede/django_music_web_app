from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls.base import reverse_lazy
from .forms import RegistrationForm, UpdateForm, PwdResetConfirmForm, AccountActivationForm
from utils.tokens import account_activation_token

User = get_user_model()
# Create your views here.
from django.views.generic import View

# from django.views.generic.edit import CreateView, FormView
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import login


class SignUpView(View):
    form_class = RegistrationForm
    template_name = 'account/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Listenme Account'
            message = render_to_string('account/acc__activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return render(request, "account/reg__confirm.html", {"form": form})

        else:
            return render(request, self.template_name, {'form': form})

class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('songs:dashboard')
        else:
            return render(request, "account/activation_invalid.html")

class ResendAccountActivationEmail(View):
    form_class = AccountActivationForm
    template_name = 'account/acc__activation_form.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data['email']
            user = User.objects.get(email=cd)

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account/acc__activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return render(request, "account/reg__confirm.html")

class PwdResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password/pwd__reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    form_class=PwdResetConfirmForm