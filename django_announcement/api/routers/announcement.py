from rest_framework.routers import DefaultRouter

from django_announcement.api.views.announcement import AnnouncementViewSet

router = DefaultRouter()
router.register(r"announcements", AnnouncementViewSet, basename="announcement")

urlpatterns = router.urls
