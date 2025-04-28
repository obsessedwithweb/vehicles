from django.db import models


class Vehicle(models.Model):
    class VehicleChoices(models.TextChoices):
        CAR = ('car', 'Car')
        BICYCLE = ('bicycle', 'Bicycle')
        TRUCK = ('truck', 'Truck')

    name = models.CharField(max_length=100, null=False, blank=False)
    type = models.CharField(max_length=10, choices=VehicleChoices.choices)
    description = models.TextField()
    price = models.PositiveIntegerField()
    # stock = models.PositiveIntegerField(default=1, null=False, blank=False)
    image = models.ImageField(upload_to=f'vehicles/', null=True, blank=True)

    def save(self, *args):
        self.image.name = f"{self.type}/{self.image.name}"
        print(f"{self.image.name}")
        print(f"{self.image.url}")
        super().save(*args)

    def __str__(self):
        return self.name


class Advertises(models.Model):
    # title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='adv/', null=True, blank=True)

    def __str__(self):
        return self.image.name


class Blog(models.Model):
    class BlogCategory(models.TextChoices):
        MOTORS = 'motors', 'Motors'
        CARS = 'cars', 'Cars'
        BICYCLES = 'bicycles', 'Bicycles'
        TRUCKS = 'trucks', 'Trucks'

    title = models.CharField(max_length=100, null=False, blank=False)
    category = models.CharField(max_length=10, choices=BlogCategory.choices)
    date = models.DateField(auto_now_add=True, null=False, blank=False)
    image = models.ImageField(upload_to=f'blog/', null=True, blank=True)


class Services(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=f'service/', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title
