from django.db import models
from django.conf import settings


# ======================================================
# Hotel Amenities
# ======================================================

class Amenity(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name


# ======================================================
# Hotel
# ======================================================

class Hotel(models.Model):

    STAR_CHOICES = [
        (1, "★"),
        (2, "★★"),
        (3, "★★★"),
        (4, "★★★★"),
        (5, "★★★★★"),
    ]

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hotels"
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    address = models.CharField(max_length=255)

    city = models.CharField(max_length=100)

    country = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    thumbnail = models.ImageField(
        upload_to="hotels/",
        blank=True,
        null=True
    )

    star_rating = models.IntegerField(
        choices=STAR_CHOICES,
        default=3
    )

    amenities = models.ManyToManyField(
        Amenity,
        blank=True
    )

    check_in_time = models.TimeField()

    check_out_time = models.TimeField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ======================================================
# Hotel Gallery Images
# ======================================================

class HotelImage(models.Model):

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(
        upload_to="hotels/gallery/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.hotel.name} Image"


# ======================================================
# Room Amenities
# ======================================================

class RoomAmenity(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ======================================================
# Room
# ======================================================

class Room(models.Model):

    STATUS_CHOICES = [
        ("available", "Available"),
        ("occupied", "Occupied"),
        ("maintenance", "Maintenance"),
    ]

    ROOM_TYPES = [
        ("standard", "Standard"),
        ("deluxe", "Deluxe"),
        ("suite", "Suite"),
        ("family", "Family"),
    ]

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    room_number = models.CharField(
        max_length=20
    )

    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES
    )

    description = models.TextField()

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    max_guests = models.PositiveIntegerField()

    total_beds = models.PositiveIntegerField()

    room_size = models.PositiveIntegerField(
        help_text="Square feet"
    )

    main_image = models.ImageField(
        upload_to="rooms/",
        blank=True,
        null=True
    )

    amenities = models.ManyToManyField(
        RoomAmenity,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["hotel", "room_number"]
        unique_together = ("hotel", "room_number")

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number}"


# ======================================================
# Room Gallery Images
# ======================================================

class RoomImage(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="rooms/gallery/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.room.room_number} Image"