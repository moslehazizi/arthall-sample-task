from django.urls import path
from .views import (
    ActivityCreateView,
    ActivityListView,
    ActivityListNotAprovedView,
    ActivityUpdateView,
    ActivityCreateViewByAdmin,
    ActivityListViewForAdmin,
)

urlpatterns = [
    path('activity-create/', ActivityCreateView.as_view(), name='activity_create'),
    path('activity-list/', ActivityListView.as_view(), name='activity_list'),
    path('activity-list-not-aproved/', ActivityListNotAprovedView.as_view(), name='activity_list_not_aproved'),
    path('activity-update/<int:pk>/update/', ActivityUpdateView.as_view(), name='activity_update'),
    path('activity-create-by-admin/', ActivityCreateViewByAdmin.as_view(), name='activity_create_by_admin'),
    path('activity-list-all', ActivityListViewForAdmin.as_view(), name='activity_list_all'),
]
