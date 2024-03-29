from django.urls import path
from .views import (
    ActivityCreateView,
    ActivityListView,
    ActivityListNotApprovedView,
    ActivityUpdateView,
    ActivityCreateViewByAdmin,
    ActivityListViewForAdmin,
    ActivityCreateSuccessView,
)

urlpatterns = [
    path('activity-create/', ActivityCreateView.as_view(), name='activity_create'), # url for activity creation page by artists
    path('activity-list/', ActivityListView.as_view(), name='activity_list'), # url for activity list page, this shows artist all their approved activities 
    path('activity-list-not-approved/', ActivityListNotApprovedView.as_view(), name='activity_list_not_approved'), # url for page that admin can see all not approved activity so that can approve them by clicking on each one and update status
    path('activity-update/<int:pk>/update/', ActivityUpdateView.as_view(), name='activity_update'), #url for page that admin update each activity and approve it
    path('activity-create-by-admin/', ActivityCreateViewByAdmin.as_view(), name='activity_create_by_admin'), #url for page that admin can create activity for artist
    path('activity-list-all', ActivityListViewForAdmin.as_view(), name='activity_list_all'), #url for page that admin can see all activities
    path('success/', ActivityCreateSuccessView.as_view(), name='success'), #url for page that come after create activity successfuly.
]
