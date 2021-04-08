from django.urls import path
from django.contrib.auth import views as auth_views

from authentication.views import DisplayNameView, AuthView

app_name = "authentication"

urlpatterns = [
    path('create/', DisplayNameView.as_view(), name="create"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('auth/', AuthView.as_view(), name="auth")

]
