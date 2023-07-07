from django.db import models


class Musician(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Album(models.Model):
    artist = models.ForeignKey('Musician', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    release_date = models.DateField()

    def __str__(self):
        return self.name


class Song(models.Model):
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    track = models.IntegerField()
    title = models.CharField(max_length=30)
    lyrics = models.TextField()
    writers = models.ManyToManyField('Musician')

    def __str__(self):
        return self.title

