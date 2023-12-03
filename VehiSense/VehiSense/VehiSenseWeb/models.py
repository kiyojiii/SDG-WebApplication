from django.db import models
import datetime
import os

# Create your models here.
class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, null=True)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")
    
def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = f"{timeNow}_{old_filename}"  # Use string formatting
    return os.path.join('carbrands/', filename)

def vehicle_filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = f"{timeNow}_{old_filename}"  # Use string formatting
    return os.path.join('vehicles/', filename)


class Cartypes(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    status = models.CharField(max_length=100, null=True)

class Carbrand(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=filepath, null=True, blank=True)
    brand = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=100)
    status = models.CharField(max_length=100, null=True)

class Vehicle(models.Model):
    image = models.ImageField(upload_to=vehicle_filepath, null=True, blank=True)
    brand = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    enginetype = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    transmission = models.CharField(max_length=100)
    technology = models.CharField(max_length=100)
    mvfileno = models.CharField(max_length=100)
    plate = models.CharField(max_length=100)
    variant = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    mileage = models.CharField(max_length=100)
    engineno = models.CharField(max_length=100)
    chasisno = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    status = models.CharField(max_length=15, null=True)
    price = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class SDG(models.Model):
    country_code = models.CharField(max_length=3)
    country = models.CharField(max_length=255)
    year = models.IntegerField()
    sdg_index_score = models.FloatField()
    goal_1_score = models.FloatField()
    goal_2_score = models.FloatField()
    goal_3_score = models.FloatField()
    goal_4_score = models.FloatField()
    goal_5_score = models.FloatField()
    goal_6_score = models.FloatField()
    goal_7_score = models.FloatField()
    goal_8_score = models.FloatField()
    goal_9_score = models.FloatField()
    goal_10_score = models.FloatField()
    goal_11_score = models.FloatField()
    goal_12_score = models.FloatField()
    goal_13_score = models.FloatField()
    goal_14_score = models.FloatField()
    goal_15_score = models.FloatField()
    goal_16_score = models.FloatField()
    goal_17_score = models.FloatField()

class Goals(models.Model):
    goal_number = models.CharField(max_length=255)
    goal_name = models.CharField(max_length=255)
    goal_description = models.CharField(max_length=255)

class Country(models.Model):
    country_country_code = models.CharField(max_length=5)
    country_country_name = models.CharField(max_length=255)
    country_description = models.CharField(max_length=255)