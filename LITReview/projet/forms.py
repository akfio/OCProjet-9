from django.forms import ModelForm
from .views import Ticket, Review
from django import forms


class TicketForm(ModelForm):

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    class Meta:
        model = Ticket
        fields = ['titre', 'description', 'image']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']

        widgets = {
            'rating': forms.RadioSelect,
        }


class FollowForm(forms.Form):
    user_to_follow = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}))