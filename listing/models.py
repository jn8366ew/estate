from django.db import models
from django.utils.timezone import now


class Listing(models.Model):

    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale'
        FOR_RENT = 'For Rent'

    class HomeType(models.TextChoices):
        HOUSE = 'House'
        CONDO = 'Condo'
        APARTMENT = 'Apartment'

    realtor = models.EmailField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    sale_type = models.CharField(max_length=10, choices=SaleType.choices, default=SaleType.FOR_SALE)
    home_type = models.CharField(max_length=10, choices=HomeType.choices, default=HomeType.HOUSE)
    main_photo = models.ImageField(upload_to='listings/')
    photo_1 = models.ImageField(upload_to='listings/')
    photo_2 = models.ImageField(upload_to='listings/')
    photo_3 = models.ImageField(upload_to='listings/')
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)

    # for deleting files in media storage
    def delete(self):
        self.main_photo.storage.delete(self.main_photo.name)
        self.photo_1.storage.delete(self.photo_1.name)
        self.photo_2.storage.delete(self.photo_2.name)
        self.photo_3.storage.delete(self.photo_3.name)

        # delete all values of an object
        super().delete()

    def __str__(self):
        return self.title




