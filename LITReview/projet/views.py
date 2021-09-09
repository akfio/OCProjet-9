from django.core.paginator import Paginator
from .models import Ticket, Review, UserFollows
from .forms import FollowForm, ReviewForm, TicketForm
from django.contrib.auth.models import User
from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef


def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def index(request):
    followed_user = UserFollows.objects.filter(user=request.user)
    reviews = Review.objects.all()
    tickets = Ticket.objects.all()
    reviews_to_show = []
    tickets_to_show = []

    for review in reviews:
        for user in followed_user:
            if user.followed_user == review.user:
                reviews_to_show.append(review)
        if review.user == request.user:
            reviews_to_show.append(review)

    for ticket in tickets:
        for user in followed_user:
            if user.followed_user == ticket.user:
                tickets_to_show.append(ticket)
        if ticket.user == request.user:
            tickets_to_show.append(ticket)

    posts = sorted(
        chain(reviews_to_show, tickets_to_show),
        key=lambda post: post.time_created,
        reverse=True
    )

    user_review = Review.objects.filter(
        user=request.user, ticket=OuterRef('pk'))
    exists = Ticket.objects.filter(Exists(user_review))

    return render(request, 'index.html', context={'posts': posts, 'exist': exists, 'followed': followed_user})


@login_required
def get_following(request):
    if request.method == "POST":
        form = FollowForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_to_follow']
            if User.objects.filter(username=username).exists():
                user_to_follow = User.objects.get(username=username)
                if user_to_follow == User.objects.get(username=request.user.username):
                    return render(request, "projet/error_follow.html")
                    pass
                elif UserFollows.objects.filter(user=request.user, followed_user=user_to_follow):
                    return render(request, "projet/error_follow.html")
                    pass
                else:
                    UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
            else:
                return render(request, "projet/error_follow.html")
    else:
        form = FollowForm()
    following_list = UserFollows.objects.filter(user=request.user)
    follower_list = UserFollows.objects.filter(followed_user=request.user)

    paginator = Paginator(following_list, 3)
    paginator_bis = Paginator(follower_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj_bis = paginator_bis.get_page(page_number)
    return render(request, 'userfollows.html',
                  context={'following_list': page_obj, 'follower_list': page_obj_bis,
                           'form': form})


class FollowOut(LoginRequiredMixin, DeleteView):
    model = UserFollows
    success_url = reverse_lazy('projet:follows')


@login_required
def flux(request):
    reviews = Review.objects.filter(user=request.user)
    tickets = Ticket.objects.filter(user=request.user)

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'flux.html', context={'posts': posts})


class TicketCreate(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['titre', 'description', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdate(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ['titre', 'description', 'image']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketDelete(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('projet:flux')


class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['rating', 'headline', 'body']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewDelete(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('projet:flux')


@login_required
def review_ticket(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        ticket_form.instance.user = request.user
        tmp = None

        if ticket_form.is_valid():
            tk = Ticket()
            tk.titre = ticket_form.data['titre']
            tk.description = ticket_form.data['description']
            #tk.image = ticket_form.data['image']
            tmp = ticket_form.save()

        if review_form.is_valid():
            rw = Review()
            rw.rating = review_form.data['rating']
            rw.headline = review_form.data['headline']
            rw.body = review_form.data['body']
            Review.objects.create(rating=rw.rating, headline=rw.headline, body=rw.body, ticket=tmp, user=request.user)
            return redirect('index')

    else:
        review_form = ReviewForm()
        ticket_form = TicketForm()

    context = {
        'review': review_form,
        'ticket': ticket_form
    }

    return render(request, 'projet/review_ticket.html', context)


@login_required
def review_answer(request, id):
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        tickets = Ticket.objects.all()
        ticket_id = Ticket.objects.get(id=id)

        if review_form.is_valid():
            rw = Review()
            rw.rating = request.POST.get('rating')
            rw.headline = request.POST.get('headline')
            rw.body = request.POST.get('body')
            Review.objects.create(rating=rw.rating, headline=rw.headline, body=rw.body, user=request.user,
                                  ticket=ticket_id)
            return redirect('index')

    else:
        review_form = ReviewForm()

    context = {
        'review': review_form,
        'ticket': tickets,
        'id': ticket_id
    }
    return render(request, 'projet/review_answer.html', context)
