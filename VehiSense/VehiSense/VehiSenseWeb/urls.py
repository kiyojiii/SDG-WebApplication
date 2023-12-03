from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('all_goals/', views.all_goals, name='all_goals'),
    path('add_goals/', views.add_goal, name='add_goals'),
    path('edit_goals/<int:goal_id>/', views.edit_goal, name='edit_goals'),
    path('delete_goals/<int:goal_id>/', views.delete_goal, name='delete_goals'),
    path('all_countries/', views.all_countries, name='all_countries'),
    path('add_country/', views.add_country, name='add_country'),
    path('edit_country/<int:country_id>/', views.edit_country, name='edit_country'),
    path('delete_country<int:country_id>/', views.delete_country, name='delete_country'),
    path('all_sdg/', views.all_sdg, name='all_sdg'),
    path('add_sdg/', views.add_sdg, name='add_sdg'),
    path('edit_sdg/<int:sdg_id>/', views.edit_sdg, name='edit_sdg'),
    path('view_sdg/<int:sdg_id>/', views.view_sdg, name='view_sdg'),
    path('delete_sdg/<int:sdg_id>/', views.delete_sdg, name='delete_sdg'),
    path('first_charts/', views.first_charts, name='first_charts'),
    path('second_charts/', views.second_charts, name='second_charts'),
    path('2022_result/', views.result_2022, name='2022_result'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
