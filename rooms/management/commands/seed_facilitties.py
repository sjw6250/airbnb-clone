from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):

    help = "This command creates facilities"

    def handle(self, *args, **options):
        facilities = [
            "facility1",
            "facility2",
            "facility3",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS("facilities created"))
