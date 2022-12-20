from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ChangeUserForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout
from django.contrib import messages

from .forms import RegisterUserForm
from .models import Question, Choice, User, Voter
from django.urls import reverse, reverse_lazy
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if Voter.objects.filter(question_id=question_id, user_id=request.user.id).exists():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Sorry, but you have already voted."
        })
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        v = Voter(user=request.user, question=question)
        v.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class RegisterView(CreateView):
    template_name = 'polls/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('polls:login')


@login_required
def profile(request):
    return render(request, 'polls/profile.html')


class LoginView(LoginView):
    template_name = 'polls/login.html'


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'polls/logout.html'


class ChangeUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'polls/change_user.html'
    form_class = ChangeUserForm
    success_url = reverse_lazy('polls:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class PasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                         PasswordChangeView):
    template_name = 'polls/password_change.html'
    success_url = reverse_lazy('polls:profile')
    success_message = 'Пароль пользователя изменен'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'polls/delete_user.html'
    success_url = reverse_lazy('polls:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
