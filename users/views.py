from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, get_user, authenticate, logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User, EmailVerification

from common.views import TitleMixin

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('home'))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        else:
            form = UserLoginForm()

    context = {'form': form}

    return render(request, 'users/login.html', context)

class UserRegistrationView(TitleMixin ,CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    title = 'Registration'


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['title'] = 'Store - Profile'
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        context['total_sum'] = sum(basket.sum() for basket in Basket.objects.filter(user=self.object))
        context['total_quantity'] = sum(basket.quantity for basket in Basket.objects.filter(user=self.object))
        return context

class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Email verification'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expire():
            user.is_verification = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))



def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Siz muvafaqqiyatli ro\'yxatdan o\'tdingiz !')
#             print(form.error_messages)
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(reverse('home'))
#         else:
#             form = UserRegistrationForm()
#
#     context = {'form': form}
#     return render(request, 'users/register.html', context)
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("users:profile"))
#     else:
#         if request.user.is_anonymous:
#             return HttpResponseRedirect(reverse('users:login'))
#         else:
#             form = UserProfileForm(instance=request.user)
#
#         baskets = Basket.objects.filter(user=request.user)
#
#         total_sum = sum(basket.sum() for basket in baskets)
#         total_quantity = sum(basket.quantity for basket in baskets)
#
#         # total_sum = 0
#         # total_quantity = 0
#         # for basket in baskets:
#         #     total_sum += basket.sum()
#         #     total_quantity += basket.quantity
#
#     context = {
#                'form': form,
#                'baskets': Basket.objects.filter(user=request.user),
#                'total_sum': total_sum,
#                'total_quantity': total_quantity
#                }
#     return render(request, 'users/profile.html', context)