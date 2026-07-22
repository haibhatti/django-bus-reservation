from django.urls import path
from . import views 



urlpatterns = [
path('', views.home, name='home'),
path('login/', views.user_login, name='login'),
path('dashboard/', views.dashboard_view, name='dashboard'),
path('logout/', views.user_logout, name='logout'),
path('view-bookings/', views.view_bookings, name='view_bookings'),
path('book-ticket/', views.book_ticket, name='book_ticket'),
path('confirm-ticket/', views.confirm_ticket, name='confirm_ticket'),
path('search-route/', views.search_route, name='search_route'),
path('edit-ticket/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),
    path('delete-ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),

]