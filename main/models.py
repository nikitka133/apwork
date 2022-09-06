from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

ROLE = (
    ('fr', 'Фрилансер'),
    ('em', 'Работодатель'),
)


class AdvUser(AbstractUser):
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Учетная запись активна?")
    role = models.CharField(choices=ROLE, default='Фрилансер', verbose_name="Роль участия", max_length=20)
    phone = PhoneNumberField(blank=False, unique=True, verbose_name='Номер телефона', default='+7',
                             max_length=12)
    balance = models.PositiveIntegerField(blank=True, default=0)
    point = models.SmallIntegerField(default=20, verbose_name='Ворк')


class Job(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    expired_date = models.DateField(null=True, verbose_name='Дедлайн', blank=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Работодатель')
    executor = models.ForeignKey(AdvUser, on_delete=models.PROTECT, related_name='executor',
                                 null=True, verbose_name='Исполнитель')
    min_price = models.PositiveIntegerField(blank=True, verbose_name='Минимальная оплата')
    max_price = models.PositiveIntegerField(blank=False, null=False, verbose_name='Максимальная оплата')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    processing = models.BooleanField(default=False, verbose_name='В работе')
    offer = models.PositiveIntegerField(blank=True, default=0)
    category = models.ForeignKey('SubCategory', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работа'


class Proposal(models.Model):
    sender = models.ForeignKey(AdvUser, on_delete=models.PROTECT, related_name='send')
    employer = models.ForeignKey(AdvUser, on_delete=models.PROTECT, )
    accepted = models.BooleanField(default=False)
    job = models.ForeignKey(Job, on_delete=models.PROTECT)
    message = models.TextField(null=False, max_length=300, verbose_name='Сообщение работодателю')
    price = models.PositiveIntegerField(verbose_name='Цена фрилансера')


class SubCategory(models.Model):
    tittle_sub_cat = models.CharField(max_length=50, verbose_name='Подкатегория')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    slug_sub_cat = models.SlugField(unique=True, verbose_name='URL', max_length=150, primary_key=True)

    def __str__(self):
        return self.tittle_sub_cat

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Category(models.Model):
    title_cat = models.CharField(max_length=50, verbose_name='Категория')
    slug_cat = models.SlugField(unique=True, verbose_name='URL', max_length=100)

    def __str__(self):
        return self.title_cat

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Chat(models.Model):
    path = models.CharField(unique=True, verbose_name='Файл чата', max_length=250)
    name_chat = models.CharField(unique=True, verbose_name='Название файла чата', max_length=150)
    job_name = models.CharField(max_length=100, verbose_name='Название работы для чата')
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.job_name
