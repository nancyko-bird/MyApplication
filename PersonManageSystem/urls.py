from django.urls import path
from . import views
urlpatterns = [
    path("index/", views.index, name="personindex"),
    path("addRecord/", views.add_record, name="add_record"),
    path("search/", views.search, name="search"),
    path("deleteRecord/<int:personid>", views.delete_record, name="person_delete_record"),
    path("editRecord/<int:personid>", views.edit_record, name="edit_record"),
    path("test1/", views.test1, name="test1"),
    path("test2/", views.test2, name="test2"),

]