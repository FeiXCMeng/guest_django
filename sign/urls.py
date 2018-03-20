from django.conf.urls import url
from sign import views_if

urlpatterns = {
    # ex : /api/add_event
    url(r'^add_event', views_if.add_event, name='add_event'),
    # ex : /api/get_event_list
    url(r'^get_event_list', views_if.get_event_list, name='get_event_list'),
}
