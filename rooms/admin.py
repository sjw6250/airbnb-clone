from django.contrib import admin
from django.utils.html import mark_safe
from . import models


# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, object):
        return object.rooms.count()

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}"/>')

    get_thumbnail.short_description = "Thumbnail"


# 사진 등록을 등록 리스트에서
class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    # 사진 등록을 등록 리스트에서
    inlines = (PhotoInline,)

    """Room Admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        (
            "Spaces",
            {
                "fields": (
                    "guests",
                    "beds",
                    "bedrooms",
                    "baths",
                ),
            },
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        (
            "More About Spaces",
            {
                "classes": ("collapse",),
                "fields": (
                    "amenities",
                    "facilities",
                    "house_rules",
                ),
            },
        ),
        ("Spaces", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    ordering = ("name", "price")

    list_filter = (
        "instant_book",
        "host__superhost",
        "host__gender",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    # 아이디 리스트가 줄줄이 안나오고 팝업에서 선택할 수 있게
    raw_id_fields = ("host",)

    search_fields = ("=city", "^host__username")

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, object):
        return object.amenities.count()

    def count_photos(self, object):
        return object.photos.count()
