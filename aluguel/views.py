from .models import Autor, Livro, InstanciaLivro
from django.shortcuts import redirect, render
from .form import AutorForm, LivroForm

# Create your views here.

def index(request):
  num_livros = Livro.objects.all().count
  num_instancias = InstanciaLivro.objects.all().count()
  num_instancias_disponiveis = InstanciaLivro.objects.filter(status__exact='d').count()
  num_autores = Autor.objects.count()

  # Number of visits to this view, as counted in the session variable.
  num_visitas = request.session.get('num_visitas', 1)
  request.session['num_visitas'] = num_visitas+1

  context = {
    'num_livros': num_livros,
    'num_instancias': num_instancias,
    'num_instancias_disponiveis': num_instancias_disponiveis,
    'num_autores': num_autores,
    'num_visitas': num_visitas
    }
  return render(request, 'index.html', context=context)

def autorList(request):
  autores = Autor.objects.all()
  return render(request, 'listar_autores.html', {'autores': autores})

def autorcreate(request):
  autores = Autor.objects.all()
  form = AutorForm()
  data = {'autores': autores, 'form': form}
  return render(request, 'autor_form.html', data)

def autor_novo(request):
  form = AutorForm(request.POST or None)
  if form.is_valid():
    form.save()
  return redirect('listar_autores.html')

def autorUpdate(request):
  pass


def autorDelete(request):
  pass

def livroList(request):
  livros = Livro.objects.all()
  return render(request, 'listar_livros.html', {'livros': livros})

def livroCreate(request):
  form = LivroForm(request.POST or None)

  if form.is_valid():
        form.save()
        return redirect('livroList')
  return render(request, 'livro_form.html', {'form': form})
  
def livroUpdate(request):
  pass

def livroDelete(request):
  pass

def livroDetalhe(request):
  pass

def alugadosList(request):
  pass

def meusListView(request):
  pass


