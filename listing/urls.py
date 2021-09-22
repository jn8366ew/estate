from django.urls import path
from .views import ManageListingView, ListingDetailView, ListingView, SearchListingView

urlpatterns = [
    path('manage', ManageListingView.as_view()),
    path('detail', ListingDetailView.as_view()),
    path('get-listings', ListingView.as_view()),
    path('search', SearchListingView.as_view()),
]