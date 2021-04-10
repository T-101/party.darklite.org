from django.urls import path
from django.contrib.auth import views as auth_views

from authentication.views import DisplayNameView, SceneIDAuthRedirect, SceneIDAuthReturn

app_name = "authentication"

urlpatterns = [
    path('create/', DisplayNameView.as_view(), name="create"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('auth/', SceneIDAuthRedirect.as_view(), name="auth"),
    path('login/', SceneIDAuthReturn.as_view(), name="sceneid_return")

]
