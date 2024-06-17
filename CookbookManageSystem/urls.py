from django.urls import path
from . import views
urlpatterns = [
    path("index/", views.index, name="cbindex"),
    path("addRecord/", views.add_record, name="cb_add_record"),
    path("addIngredient/", views.add_ingredient, name="cb_add_ingredient"),
    path("cbsearch/", views.cbsearch, name="cb_search"),
    path("ingsearch/", views.ingsearch, name="ing_search"),
    path("deleteRecord/<int:cbid>", views.delete_record, name="cb_delete_record"),
    path("editRecord/<int:cbid>", views.edit_record, name="cb_edit_record"),
    path("test1/", views.test1, name="test1"),
    path("test2/", views.test2, name="test2"),

]
