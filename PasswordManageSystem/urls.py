from django.urls import path
from . import views
urlpatterns = [
    path("index/", views.index, name="pmindex"),
    path("addRecord/", views.add_record, name="pm_add_record"),
    path("search/", views.search, name="pm_search"),
    path("deleteRecord/<int:pid>", views.delete_record, name="pm_delete_record"),
    path("editRecord/<int:pid>", views.edit_record, name="pm_edit_record"),
    path("test1/", views.test1, name="test1"),
    path("test2/", views.test2, name="test2"),

]
