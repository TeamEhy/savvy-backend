from rest_framework import routers
from main.views import ItemViewSet, CategoryViewSet, CartViewSet, ImageViewSet, cart_submit, upload_image
from django.conf.urls import url
from django.conf.urls.static import static

router = routers.SimpleRouter()
router.register(r'items', ItemViewSet, 'Items')
router.register(r'categories', CategoryViewSet, 'Categories')
router.register(r'images', ImageViewSet, 'Images')
router.register(r'cart', CartViewSet, 'Cart')
urlpatterns = router.urls

urlpatterns += [
	url(r'^image$', upload_image),
	# url(r'^image/(?P<id>[^/.]+)$', serve_image),
	url(r'^submit_cart/(?P<id>[^/.]+)/(?P<quantity>[^/.]+)$', cart_submit),
] + static('image/', document_root='/var/www/app/mysite')
