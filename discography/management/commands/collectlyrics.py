from django.core.management.base import BaseCommand
from discography.models import Song


class Command(BaseCommand):
    help = "Collect song lyrics for lyrics bot"

    def add_arguments(self, parser):
        parser.add_argument(
            "--min-length",
            type=int,
            default=40,
            help="Specifies the minimum length of each lyrics segment"
        )
        parser.add_argument(
            "--max-length",
            type=int,
            default=140,
            help="Specifies the maximum length of each lyrics segment"
        )
        parser.add_argument(
            "-o", "--output", help="Specifies file to which the output is written."
        )

    def handle(self, *args, **options):
        min_length = options["min_length"]
        max_length = options["max_length"]
        output = options["output"]
        with open(output, "wt") as file:
            for song in Song.objects.all():
                for segment in song.lyrics.replace("\r", "").split("\n\n"):
                    if min_length <= len(segment) <= max_length:
                        file.write(f"{segment}\n\n")
