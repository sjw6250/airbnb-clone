from django.db import models
from django.db.models.deletion import CASCADE
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models
import users


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    pass

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facility Model Definition"""

    pass

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    pass

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):
    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    country = CountryField(blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=140, blank=True, null=True)
    guests = models.IntegerField(blank=True, null=True)
    beds = models.IntegerField(blank=True, null=True)
    bedrooms = models.IntegerField(blank=True, null=True)
    baths = models.IntegerField(blank=True, null=True)
    check_in = models.TimeField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User",
        related_name="rooms",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    room_type = models.ForeignKey(
        "RoomType",
        related_name="rooms",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    # save override, "saver" 치면 자동 생성 (설치된 Extention django snippets 가 자동생성)
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0
