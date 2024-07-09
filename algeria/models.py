from django.db import models

class Wilaya(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name_ascii = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name_ascii

class Daira(models.Model):
    name_ascii = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, related_name='dairas')

    def __str__(self):
        return self.name_ascii

class Commune(models.Model):
    id = models.IntegerField(primary_key=True)
    name_ascii = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    daira = models.ForeignKey(Daira, on_delete=models.CASCADE, related_name='communes')

    def __str__(self):
        return self.name_ascii
