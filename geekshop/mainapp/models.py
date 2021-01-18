from django.db import models


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='имя')
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True, db_index=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(verbose_name='имя продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True, verbose_name='картинка')
    product_file = models.FileField(upload_to='custom_files', blank=True, verbose_name='картинка')
    short_desc = models.CharField(verbose_name='краткое описание продукта', max_length=60, blank=True)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    is_active = models.BooleanField(verbose_name='активна', default=True, db_index=True)

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')

    def __str__(self):
        return f"{self.name} ({self.category.name})"
