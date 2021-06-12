"""sal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views
from .views import (autorDelete, autorList, autor_novo, autorcreate, autorDetalhe,
                    index, livroCreate, livroDelete, 
                    livroDetalhe, livroList, livroUpdate, autorDelete, autorUpdate, 
                    meusListView, alugadosList)

app_name = 'aluguel'

urlpatterns = [
    path('', views.index, name='index'),
    path('livros/', views.livroList, name='listar_livros'),
    path('livro/<int:pk>', views.livroDetalhe, name='livro_detalhe'),
    path('autores/', autorList, name='listar_autores'),
    path('autor/<int:pk>', views.autorDetalhe, name='autor_detalhe'),
]


urlpatterns += [
    path('meus_livros/', views.meusListView, name='meus_livros'),
    path('alugados/', views.alugadosList, name='alugados'), 
]


# Add URLConf for librarian to renew a book.
urlpatterns += [
    #path('livro/<uuid:pk>/renovacao/', views.renew_book_librarian, name='renovacao-livro'),
]


# Add URLConf to create, update, and delete authors
urlpatterns += [
    path('autor/create/', views.autorcreate, name='autor_create'),
    path('autor/create/autor_novo/', views.autor_novo, name='autor_novo'),
    path('autor/<int:pk>/update/', views.autorUpdate, name='autor_update'),
    path('autor/<int:pk>/delete/', views.autorDelete, name='autor_delete'),
]

# Add URLConf to create, update, and delete books
urlpatterns += [
    path('livro/create/', views.livroCreate, name='livro_create'),
    path('livro/<int:pk>/update/', views.livroUpdate, name='livro_update'),
    path('livro/<int:pk>/delete/', views.livroDelete, name='livro_delete'),
]
