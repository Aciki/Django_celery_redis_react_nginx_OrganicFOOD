import random
import string

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class FoodPublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(FoodPublishedManager, self)
            .get_queryset()
            .filter(published_status=True)
        )


class Food(TimeStampedUUIDModel):
    

   
    user = models.ForeignKey(
        User,
        verbose_name=_("Agent,Seller or Buyer"),
        related_name="agent_buyer",
        on_delete=models.DO_NOTHING,
    )

    title = models.CharField(verbose_name=_("Food Title"), max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    ref_code = models.CharField(
        verbose_name=_("Food Reference Code"),
        max_length=255,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        default="Default description...update me please....",
    )
    country = CountryField(
        verbose_name=_("Country"),
        default="MK",
        blank_label="(select country)",
    )
    city = models.CharField(verbose_name=_("City"), max_length=180, default="Skopje")
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=100, default="140"
    )
    street_address = models.CharField(
        verbose_name=_("Street Address"), max_length=150, 
    )
    
    
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.0
    )
    tax = models.DecimalField(
        verbose_name=_("Food Tax"),
        max_digits=6,
        decimal_places=2,
        default=0.5,
        help_text="5% Food tax charged",
    )
   

    

    

    cover_photo = models.ImageField(
        verbose_name=_("Main Photo"), default="/house_sample.jpg", null=True, blank=True
    )
    photo1 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo2 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo3 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo4 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    published_status = models.BooleanField(
        verbose_name=_("Published Status"), default=False
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)

    objects = models.Manager()
    published = FoodPublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "OrganiC FOOD"
        verbose_name_plural = "Organic"

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Food, self).save(*args, **kwargs)

    @property
    def final_food_price(self):
        tax_percentage = self.tax
        food_price = self.price
        tax_amount = round(tax_percentage * food_price, 2)
        price_after_tax = float(round(food_price + tax_amount, 2))
        return price_after_tax


class FoodViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("IP Address"), max_length=250)
    food = models.ForeignKey(
        Food, related_name="food_views", on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"Total views on - {self.food.title} is - {self.food.views} view(s)"
        )

    class Meta:
        verbose_name = "Total Views on Item"
        verbose_name_plural = "Total item Views"
