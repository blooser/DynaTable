from django.urls import path

from dynatablebackend import views

urlpatterns = [
    path("table", views.create_table),
    path("table/<int:id>", views.update_table_structure),
    path("table/<int:id>/row", views.add_table_row),
    path("table/<int:id>/rows", views.get_table_rows),
]
