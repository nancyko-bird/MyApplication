from django.urls import path
from . import views
urlpatterns = [
    path("index/", views.index, name="ledgerindex"),
    path("ledger/<int:lid>", views.ledger, name="ledger"),
    path("addLedger/", views.add_ledger, name="add_ledger"),
    path("addAccount/<int:lid>", views.add_account, name="add_account"),
    path("searchLedger/", views.search_ledger, name="search_ledger"),
    path("searchAccount/", views.search_account, name="search_account"),
    path("deleteLedger/<int:pid>", views.delete_ledger, name="delete_ledger"),
    path("editLedger/<int:pid>", views.edit_ledger, name="edit_ledger"),
    path("deleteAccount/<int:lid>/<int:aid>", views.delete_account, name="delete_account"),
    path("editAccount/<int:lid>/<int:aid>", views.edit_account, name="edit_account"),
    path("test1/", views.test1, name="ledgertest"),
    # path("test2/", views.test2, name="test2"),

]
