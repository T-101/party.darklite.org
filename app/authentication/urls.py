from django.urls import path
from django.contrib.auth import views as auth_views

from authentication.views import ProfileView, SceneIDAuthRedirect, SceneIDAuthReturn

app_name = "authentication"

urlpatterns = [
    path('profile/', ProfileView.as_view(), name="profile"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('sceneid/auth/', SceneIDAuthRedirect.as_view(), name="auth"),
    path('sceneid/login/', SceneIDAuthReturn.as_view(), name="sceneid_return")
]
