from django.db import models
from django.urls import reverse

from manager.models import Customer, Service, Employee


# Create your models here.

class Treatment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    consultant = models.ForeignKey(Employee, related_name='consultant', on_delete=models.CASCADE, null=True)
    expert = models.ForeignKey(Employee, related_name='expert', on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Employee, related_name='doctor', on_delete=models.CASCADE, null=True)
    done = models.BooleanField(default=False)
    date_apply = models.DateField(max_length=10)
    date_end = models.DateField(max_length=10, null=True)
    note = models.CharField(max_length=128)

    def __str__(self):
        return self.service.name

    def get_absolute_url(self):
        return reverse("action:treatment_overview", kwargs={"pk": self.pk})

    class Meta:
        db_table = 'Treatment'


class TreatmentProcessImages(models.Model):
    treat = models.IntegerField()
    treat_pro = models.IntegerField()
    thumb = models.ImageField(blank=True, null=True, upload_to='Treatments')

    class Meta:
        db_table = 'TreatmentProcessImages'


class TreatmentProcess(models.Model):
    tag = models.IntegerField()
    date = models.DateField(max_length=10)
    status = models.TextField(max_length=128)
    tmp_thumb = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.tag)

    def get_absolute_url(self):
        return reverse("action:treatment_append", kwargs={'pk': self.pk})

    class Meta:
        db_table = 'TreatmentProcess'


class Consulting(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    consultor = models.ForeignKey(Employee, related_name='consultor', on_delete=models.CASCADE)
    date = models.DateField(max_length=10)
    request = models.CharField(max_length=128)
    medicalhistory = models.CharField(max_length=128, null=True)
    health = models.CharField(max_length=128, null=True)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("action:consultant_view", kwargs={'pk': self.pk})

    class Meta:
        db_table = 'Consulting'
