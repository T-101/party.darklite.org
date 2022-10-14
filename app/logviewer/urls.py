from django.urls import path

from logviewer.views import LogViewerIndexView, LogViewerDetailView

app_name = "logviewer"

urlpatterns = [
    path('', LogViewerIndexView.as_view(), name="index"),
    path('<str:filename>/', LogViewerDetailView.as_view(), name="detail")
]
