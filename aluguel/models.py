from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import DateField
from django.urls.base import reverse
import uuid

# Create your models here.
class Genero(models.Model):
    nome = models.CharField(
        max_length=200,
        help_text="Insira o gênero ( Ficção Científica, Drama, Policial e etc.)"
        )
          
    def __str__(self):
        return self.nome

class Autor(models.Model):
      
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_nasc = models.DateTimeField(null=True, blank=True)
    data_falec = models.DateTimeField('Faleceu em:', null=True, blank=True)

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
  quantidade = models.IntegerField()
  genero = models.ManyToManyField('Genero')
  linguagem = models.CharField(max_length=30)
  ano = models.IntegerField()
  
  def get_genero(self):
        return "\n".join([p.generos for p in self.genero.all()])

  # Metadados
  class Meta:
      ordering = ['-titulo', 'autor', 'ano']

   # Métodos
  #def get_absolute_url(self):
  #    return reverse('livro_detalhe', args=[str(self.id)])

  def __str__(self):
      return self.titulo


 
#informações sobre um livro específico 
class InstanciaLivro(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  livro = models.ForeignKey('Livro', on_delete = models.SET_NULL, null = True)
  edicao = models.CharField(max_length=200)
  devolucao = models.DateField(null=True, blank=True)
  cliente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  
  @property
  def is_overdue(self):
      if self.devolucao and DateField.today() > self.devolucao:
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