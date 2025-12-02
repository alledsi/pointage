"""
URL configuration for Pointage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name="accueil"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('arrivee', views.arrivee, name="arrivee"),
    path('depart/<int:id>', views.depart, name="depart"),
    path('annulerdepart/<int:id>', views.annulerdepart, name="annulerdepart"),
    path('pause/debut/<int:id>', views.debutpause, name="debutpause"),
    path('pause/fin/<int:id>', views.finpause, name="finpause"),
    path('annee', views.pannee, name="pannee"),
    path('mois', views.pmois, name="pmois"),
    path('semaine', views.psemaine, name="psemaine"),
    path('export_pannee', views.export_pannee, name="export_pannee"),
    path('export_pmois', views.export_pmois, name="export_pmois"),
    path('api/v1/pointage/app/all', views.json_pointage, name="json_pointage"),
    path('accounts/password_change/',
                 auth_views.PasswordChangeView.as_view(
                     #template_name='registration/password_change.html',  # Optionnel : pour utiliser un template personnalisé
                     success_url='/logout' # Optionnel : pour rediriger après le changement
                 ),
                 name='password_change'),
    #path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'), # Optionnel : page de succès

]
