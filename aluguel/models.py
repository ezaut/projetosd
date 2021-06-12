from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import DateField
from django.urls.base import reverse
import uuid

# Create your models here.
class Genero(models.Model):
    genero = models.CharField(
        max_length=200,
        help_text="Insira o gênero ( Ficção Científica, Drama, Policial e etc.)"
        )
          
    def __str__(self):
        return self.genero

class Autor(models.Model):
      
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_nasc = models.DateField(null=True, blank=True)
    data_falec = models.DateField('Faleceu em:', null=True, blank=True)

    class Meta:
        ordering = ['sobrenome', 'nome']

    def get_absolute_url(self):
        return reverse('autor_detalhe', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.sobrenome, self.nome)


#salva informações gerais sobre a biblioteca 
class Livro(models.Model):
  titulo = models.CharField(max_length=200, null=False)
  autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
  isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
  edicao = models.CharField(max_length=200)
  quantidade = models.IntegerField()
  genero = models.ManyToManyField('Genero')
  linguagem = models.CharField(max_length=30)
  ano = models.IntegerField()
  descricao = models.TextField()
  
    # Metadados
  class Meta:
      ordering = ['-titulo', 'autor']

  def get_genero(self):
        return ', '.join([genero.genero for genero in self.genero.all()])

  get_genero.short_description = 'Genero'

   # Métodos
  def get_absolute_url(self):
      return reverse('livro_detalhe', args=[str(self.id)])

  def __str__(self):
      return self.titulo


 
#informações sobre um livro específico 
class InstanciaLivro(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  livro = models.ForeignKey('Livro', on_delete = models.SET_NULL, null = True)
  devolucao = models.DateField(null=True, blank=True)
  cliente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  
  

  @property
  def is_overdue(self):
      if self.devolucao and date.today() > self.devolucao:
          return True
      return False

  STATUS_EMPRESTIMO = (
    ('m', 'Manutenção'),
    ('e', 'Emprestado'),
    ('d', 'Disponível'),
    ('r', 'Reservado'),
  )

  status = models.CharField( 
    max_length=1,
    choices=STATUS_EMPRESTIMO,
    blank = True,
    default = 'm',
    help_text = 'Disponibilidade do livro',
  )

  def get_queryset(self):
        return InstanciaLivro.objects.filter(cliente=self.request.username).filter(status__exact='e').order_by('devolucao')
  
  class Meta:
        ordering = ['devolucao']
        permissions = (("can_mark_returned", "Set book as returned"),)
  
  def __str__(self):
        return '{0} ({1})'.format(self.id, self.livro.titulo)
  
  
#salva informações sobre o pedido de um cliente
class Pedido(models.Model):
  #qual cliente fez o pedido
  cliente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

  #o cliente pediu qual livro
  livro = models.ForeignKey(Livro, null= True, on_delete = models.CASCADE)

  #data do pedido
  dataPedido = models.DateTimeField(auto_now_add=True, blank=True)

  #valor do pedido
  valor = models.CharField(max_length=100)

  def __str__(self):
    return self.id

#salva informações sobre a entrega do pedido
class OrdemDeEntrega(models.Model):

  #entrega do pedido. uma entrega se relaciona com um pedido e vice-versa
  pedido = models.OneToOneField(Pedido, null= True, on_delete=models.CASCADE)
  
  #def dataEntrega():
  # return pedido.dataPedido + datetime.timedelta(days=1)

  def __str__(self):
    return self.id