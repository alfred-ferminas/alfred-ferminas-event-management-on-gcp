from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    # path("", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("", views.index, name="home"),
    path("events", views.events),
    path("notification", views.notifications),
    path("signin", views.signin),
    path("signup", views.signup),
    path("thanks", views.thanks),
    path("contactus", views.contactus),  
    path("myevents",views.myevents, name="myevents"),
    path("signout", views.signout),
    path("myevents/<int:myid>", views.deleteevent),
    path("myevents/d-<int:myid>",views.notify),
    path("myevents/saverecord/e-<int:myid>",views.saverecord)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

