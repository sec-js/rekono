from rest_framework.routers import SimpleRouter
from targets.views import (TargetEndpointViewSet, TargetPortViewSet,
                           TargetViewSet)

router = SimpleRouter()
router.register('targets', TargetViewSet)
router.register('target-ports', TargetPortViewSet)
router.register('target-endpoints', TargetEndpointViewSet)

urlpatterns = router.urls
