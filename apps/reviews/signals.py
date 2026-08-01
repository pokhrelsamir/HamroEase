from django.db.models import Avg
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Review


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_hotel_rating(sender, instance, **kwargs):
    hotel = instance.hotel

    reviews = hotel.reviews.all()

    hotel.total_reviews = reviews.count()

    hotel.average_rating = (
        reviews.aggregate(
            average=Avg("rating")
        )["average"] or 0
    )

    hotel.save(
        update_fields=[
            "average_rating",
            "total_reviews",
        ]
    )