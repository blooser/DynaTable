from django.urls import path

from dynatablebackend import views

urlpatterns = [
    path("table", views.create_table),
    path("table/<str:table_id>", views.update_table_structure),
    path("table/<str:table_id>/row", views.add_table_row),
    path("table/<str:table_id>/rows", views.get_table_rows),
]
