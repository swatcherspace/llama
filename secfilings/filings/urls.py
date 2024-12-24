from django.urls import path
from . import views  # Ensure views.py exists in the same directory

urlpatterns = [
    # Define your API endpoint here
    path('generate-csv/', views.GenerateCSVAPIView.as_view(), name='generate_csv'),
    path('generate-insights/', views.CSVInsightsAPIView.as_view(), name='generate-insights'),
    path('processed-data/', views.CSVInsightsAPIView.as_view(), name='get_processed_data'),
]
