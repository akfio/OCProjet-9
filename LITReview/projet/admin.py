from django.contrib import admin
from .models import Review, Ticket, UserFollows


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user']
    search_fields = ['ticket']


class ReviewInlines(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_filter = ['titre', 'time_created', 'user']
    list_display = ('titre', 'user')
    inlines = [ReviewInlines]


@admin.register(UserFollows)
class FollowsAdmin(admin.ModelAdmin):
    list_display = ['user', 'followed_user', 'id']
