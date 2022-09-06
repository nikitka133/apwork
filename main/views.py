from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView, UpdateView, ListView

from main.forms import UserCrForm, CreateJobForm, ChangeUserInfoForm, ChangePasswordForm, ProposalForm
from main.models import AdvUser, Job, Chat, Proposal
from main.services import read_message, write_message


def index(request):
    context = {'form': Job.objects.all()[:10]}
    return render(request, 'basic.html', context)


class RegisterUserView(CreateView):
    template_name = "register.html"
    form_class = UserCrForm
    success_url = reverse_lazy('home')

    def get_absolute_url(self):
        return redirect('home')

    #  авторизация после регистрации
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def create_job(request):
    if request.method == 'POST':
        form = CreateJobForm(request.POST)
        if form.is_valid() and (request.POST['author'] == str(request.user.id)):
            form.save()
            messages.success(request, 'Работа опубликована')
            return redirect('account')
        else:
            return render(request, 'create_job.html', context={'form': form})

    form = CreateJobForm(initial={'author': request.user.id})
    context = {'form': form}
    return render(request, 'create_job.html', context)


@login_required
def account_page(request):
    context = {'jobs': Job.objects.filter(author_id=request.user.id)}
    return render(request, 'account.html', context)


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Изменение дынных в профиле"""
    model = AdvUser
    template_name = "settings.html"
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy("main:profile")
    success_message = "Данные изменены"

    # получаем id пользователя
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ChangePasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = 'Пароль изменён'
    success_url = reverse_lazy('account')
    form_class = ChangePasswordForm


def job_view(request, pk):
    context = {'form': Job.objects.get(pk=pk)}
    return render(request, 'detail_job.html', context)


class JobListView(ListView):
    template_name = 'job.html'
    paginate_by = 2

    def get_queryset(self):
        return Job.objects.filter(is_active=True, processing=False)


class JobSubCatListView(ListView):
    template_name = 'category.html'
    paginate_by = 2

    def get_queryset(self):
        return Job.objects.filter(category=self.kwargs['slug_sub_cat'])


@login_required
def chat(request):
    if request.method == 'GET':
        # получение сообщений чата из ЛК
        if 'chat' in request.GET:
            context = {'message': read_message(request.GET['chat']),
                       'name_chat': request.GET['chat']}

            return render(request, 'chat.html', context)
        else:
            # получение или созадание чата из обьявления
            job_name = request.GET['job_name']
            name_chat = '_'.join(sorted((request.GET['sender'], request.GET['author'])))
            Chat.objects.get_or_create(name_chat=name_chat, path=name_chat + '.txt', job_name=job_name)
            context = {'message': read_message(name_chat),
                       "name_chat": name_chat}
            return render(request, 'chat.html', context)
    # отправка сообщений в чате
    elif 'message' in request.POST:
        message = request.POST['message']
        author = request.POST['author']
        name_chat = request.POST['chat']
        write_message(name_chat, message, author)

        context = {'message': read_message(name_chat),
                   "name_chat": name_chat}
        return render(request, 'chat.html', context)


@login_required
def my_chats(request):
    chats = Chat.objects.filter(name_chat__contains=request.user.username)
    context = {'chats': chats}

    return render(request, 'my_chats.html', context)


@login_required
def send_proposal(request):
    if request.method == 'GET':
        try:
            context = {'form': ProposalForm(initial={'employer': request.GET['employer'],
                                                     'sender': request.user.id,
                                                     'job': request.GET['job_id']
                                                     }
                                            )
                       }
            return render(request, 'send_proposal.html', context)
        except MultiValueDictKeyError:
            print('send_proposal get запрос не содержит нужного ключа--')
            return redirect('job')

    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка отправлена')
            return redirect('job')
        return redirect('job')


@login_required
def proposal(request):
    form = Proposal.objects.filter(employer=request.user.id)
    context = {'form': form}
    return render(request, 'proposal.html', context)


@login_required
def view_proposal(request):
    if request.method == 'GET':
        context = {'form': Proposal.objects.get(pk=request.GET['id'])}
        return render(request, 'view_proposal.html', context)
    return redirect('proposal')


@login_required
def pay(request):
    if request.method == 'POST':
        context = {'proposal_id': request.POST['proposal_id'],
                   'price': request.POST['price']}
        return render(request, 'pay.html', context=context)