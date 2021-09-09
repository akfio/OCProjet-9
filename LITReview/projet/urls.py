from django.urls import path
from . import views

app_name = 'projet'

urlpatterns = [
    path('follows/', views.get_following, name='follows'),
    path('follows/<int:pk>/delete/', views.FollowOut.as_view(), name='delete-follow'),
    path('flux/', views.flux, name='flux'),
    path('createticket/', views.TicketCreate.as_view(), name="new-ticket"),
    path('ticket/<int:pk>/update/', views.TicketUpdate.as_view(), name="update-ticket"),
    path('ticket/<int:pk>/delete/', views.TicketDelete.as_view(), name='delete-ticket'),
    path('create_answer/<int:id>/', views.review_answer, name="answer"),
    path('review/<int:pk>/update/', views.ReviewUpdate.as_view(), name="update-review"),
    path('review/<int:pk>/delete/', views.ReviewDelete.as_view(), name='delete-review'),
    path('review_ticket/', views.review_ticket, name='review_ticket')
]
