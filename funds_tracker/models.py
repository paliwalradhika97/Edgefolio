from django.db import models

# Create your models here.
 
class Fund(models.Model):
    name = models.CharField(max_length=200)
    strategy = models.CharField(max_length=200)
    aum = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    inception_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


 