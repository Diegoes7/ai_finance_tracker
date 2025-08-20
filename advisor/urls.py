# from django.urls import path
# from .views import chat_view, chat_page

# urlpatterns = [
#     # GET: renders HTML page
#     path('chat/', chat_page, name='chat_page'),
#     # POST: handles JSON chat API
#     path('api/chat/', chat_view, name='chat_api'),
# ]

from django.urls import path
from . import views


urlpatterns = [
    path("chat/", views.chat_view, name="chat_view"),
    path("", views.chat_page, name="chat_page"),
    path("prompts/", views.prompts_page, name="prompts_page"),
]

# urlpatterns = [
#     path("", views.chat_page, name="chat_page"),
#     path("prompts/", views.prompts_page, name="prompts_page"),
#     path("generate/", views.chat_view, name="chat_view"),
#     path('api/chat/', views.chat_view, name='chat_api'),
# ]
