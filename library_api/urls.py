from rest_framework.routers import SimpleRouter

from library_api import views

router = SimpleRouter()

router.register(r'book', views.BookViewSet)
router.register(r'client', views.ClientViewSet)
router.register(r'reservation', views.ReservationViewSet)

urlpatterns = router.urls
