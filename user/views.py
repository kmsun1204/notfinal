from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, FormView
from .forms import UserRegistrationForm, LoginForm, VerificationEmailForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from .mixins import VerifyEmailMixin
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import ProfileForm, UserForm
from django.views import View


class UserRegistrationView(VerifyEmailMixin, CreateView):
    model = get_user_model()  # 자동생성 폼에서 사용할 모델
    form_class = UserRegistrationForm  # 자동생성 폼에서 사용할 필드
    success_url = '/user/login/'
    verify_url = '/user/verify/'
    template_name = 'user/registration.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response


class UserVerificationView(TemplateView):
    model = get_user_model()
    redirect_url = '/user/login/'
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, '인증이 완료되었습니다.')
        else:
            messages.error(request, '인증이 실패되었습니다.', extra_tags='danger')
        return HttpResponseRedirect(self.redirect_url)

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.objects.get(pk=pk)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active = True
            user.save()     # 데이터가 변경되면 save() 호출
        return is_valid


class ResendVerifyEmailView(VerifyEmailMixin, FormView):
    model = get_user_model()
    form_class = VerificationEmailForm
    success_url = '/user/login/'
    template_name = 'user/resend_verify_email.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']  # 폼 객체는 유효성검증이 끝나면 cleaned_data라는 인스턴스 변수에 각 필드 이름으로 사용자가 입력한 값을 저장!
        try:
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            messages.error(self.request, '알 수 없는 사용자 입니다.')
        else:
            self.send_verification_email(user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)


class Index(TemplateView):
    template_name = 'user/home.html'


@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    photos = user.photo_set.filter(is_public=True)[:10]
    context = {"profile_user": user, "photos": photos}
    return render(request, 'user/user_profile.html', context)


class ProfileUpdateView(View): # 간단한 View클래스를 상속 받았으므로 get함수와 post함수를 각각 만들어줘야한다.
    # 프로필 편집에서 보여주기위한 get 메소드
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)  # 로그인중인 사용자 객체를 얻어옴
        user_form = UserForm(initial={
            'name': user.name,
            'username': user.username,
        })

        if hasattr(user, 'profile'):  # user가 profile을 가지고 있으면 True, 없으면 False (회원가입을 한다고 profile을 가지고 있진 않으므로)
            profile = user.profile
            profile_form = ProfileForm(initial={
                'profile_photo': profile.profile_photo,
                'weight': profile.weight,
                'height': profile.height,
            })
        else:
            profile_form = ProfileForm()

        return render(request, 'user/user_profileupdate.html', {"user_form": user_form, "profile_form": profile_form})

    # 프로필 편집에서 실제 수정(저장) 버튼을 눌렀을 때 넘겨받은 데이터를 저장하는 post 메소드
    def post(self, request):
        u = User.objects.get(id=request.user.pk)        # 로그인중인 사용자 객체를 얻어옴
        user_form = UserForm(request.POST, instance=u)  # 기존의 것의 업데이트하는 것 이므로 기존의 인스턴스를 넘겨줘야한다. 기존의 것을 가져와 수정하는 것

        # User 폼
        if user_form.is_valid():
            user_form.save()

        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile) # 기존의 것 가져와 수정하는 것
        else:
            profile_form = ProfileForm(request.POST, request.FILES) # 새로 만드는 것

        # Profile 폼
        if profile_form.is_valid():
            profile = profile_form.save(commit=False) # 기존의 것을 가져와 수정하는 경우가 아닌 새로 만든 경우 user를 지정해줘야 하므로
            profile.user = u
            profile.save()

        return redirect('profile', pk=request.user.pk) # 수정된 화면 보여주기

