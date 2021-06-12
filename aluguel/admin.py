from django.contrib import admin
from .models import (Livro, InstanciaLivro, Autor, Genero,
                     Pedido, OrdemDeEntrega)


# Register your models here.

class LivrosInline(admin.TabularInline):
    model = Livro

class InstanciaLivroInline(admin.TabularInline):
    model = InstanciaLivro
    extra = 0

class PedidoInline(admin.TabularInline):
    model = Pedido

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'get_genero', 'linguagem', 'edicao', 'quantidade', 'ano')
    list_filter = ('titulo', 'autor')
    inlines = [InstanciaLivroInline]

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('sobrenome', 'nome', 'data_nasc', 'data_falec')
    fields = ['nome', 'sobrenome', ('data_nasc', 'data_falec')]
    inlines = [LivrosInline]

@admin.register(InstanciaLivro)
class InstanciaLivroAdmin(admin.ModelAdmin):
    list_display = ('livro', 'status', 'cliente', 'devolucao', 'id')
    list_filter = ('status', 'devolucao')

    fieldsets = (
        (None, {
            'fields': ('livro', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'devolucao', 'cliente')
        }),
    )

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('dataPedido', 'valor', 'pago')
    list_filter = ('dataPedido', 'pago')
    

admin.site.register(Genero)
admin.site.register(OrdemDeEntrega)