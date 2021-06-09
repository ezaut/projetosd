from django.db.models import fields
from django.forms import ModelForm

from .models import Livro, Autor

class LivroForm(ModelForm):
    class Meta:
        model = Livro
        fields = '__all__'

class AutorForm(ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'