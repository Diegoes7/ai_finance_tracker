from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.add_transaction, name="add_transaction"),
    path('all_records', views.balance_view, name='index'),
    path("summary/", views.view_summary, name="view_summary"),
    # path('download/financial-data/', views.download_financial_data,
    #      name='download_financial_data'),
    path('download/', views.download_financial_data, name='download_financial_data'),
    path("chart_transactions/", views.transaction_chart, name="transaction_chart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
