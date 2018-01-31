from django.db import models
from django.contrib.auth.models import User
from abc import ABCMeta, abstractmethod

# Create your models here.


class SaleInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_price(self):
        pass


class Client(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Category(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(max_length=255, null=True, blank=True)

    # parent category
    parent = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'


class Item(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField()
    image = models.ImageField(max_length=255)
    price = models.PositiveIntegerField()

    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Наименование товара'
        verbose_name_plural = 'Наименования товаров'


class CartItem(models.Model, SaleInterface):
    item = models.ForeignKey(Item)
    quantity = models.IntegerField()
    price = models.PositiveIntegerField(null=True, blank=True)

    def get_price(self):
        return self.quantity * self.item.price

    def get_title(self):
        return self.__str__()

    def __str__(self):
        return self.item.title

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'


class Cart(models.Model, SaleInterface):
    client_owner = models.ForeignKey(Client, null=True)
    cart_items = models.ManyToManyField(CartItem)

    def get_owner(self):
        if self.client_owner is None:
            return 'No owner yet'
        return self.client_owner.user.username

    def get_price(self):
        return sum(c.get_price() for c in self.cart_items.all())

    def __str__(self):
        return ' '.join(['Корзина', str(self.id)])

    class Meta:
        verbose_name = 'Корзине'
        verbose_name_plural = 'Корзины'


class Order(models.Model, SaleInterface):
    cart = models.ForeignKey(Cart)
    date = models.DateTimeField()

    def get_price(self):
        return self.cart.get_price()

    def __str__(self):
        return str(self.date.date())


class Message(models.Model):
    telephone = models.CharField(max_length=10, null=False)
    message = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(null=False)

    def __str__(self):
        return self.message