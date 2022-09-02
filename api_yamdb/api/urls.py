from django.urls import include, path
from rest_framework.routers import DefaultRouter


from users.views import (
    send_confirmation_code,
    get_jwt_token,
    UsersViewSet,
    UserDetailPach
)
from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
)


router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet, basename='users')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/auth/signup/', send_confirmation_code),
    path('v1/auth/token/', get_jwt_token),
    path('v1/users/me/', UserDetailPach.as_view()),
    path('v1/', include(router_v1.urls)),
]
