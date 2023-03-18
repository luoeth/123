
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Ptt, name='Ptt'),
    path('blocktempo', views.Blocktempo, name='Blocktempo'),
    path('abmedia', views.Abmedia, name='Abmedia'),
    path('defi', views.Defi, name='Defi'),
    path('nft', views.Nft, name='Nft'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)