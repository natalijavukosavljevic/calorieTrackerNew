from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime
from django.db.models import Q
from django.utils import timezone

# Create your models here.


class Food(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    carbs = models.FloatField(max_length=200, null=True, blank=True)
    protein = models.FloatField(max_length=200, null=True, blank=True)
    fats = models.FloatField(max_length=200, null=True, blank=True)
    calories = models.IntegerField(null=True, blank=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name


class Consume(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  
    food = models.ForeignKey(
        Food, on_delete=models.CASCADE, null=True, blank=True
    )  
    quantity = models.IntegerField(default=100)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.owner.first_name + " " + str(self.id)

    @property
    def quantCarbs(self):
        return round(self.food.carbs * (self.quantity / 100), 2)

    @property
    def quantProteins(self):
        return round(self.food.protein * (self.quantity / 100), 2)

    @property
    def quantFats(self):
        return round(self.food.fats * (self.quantity / 100), 2)

    @property
    def quantCalories(self):
        return round(self.food.calories * (self.quantity / 100), 2)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    limitCalories = models.IntegerField(default=2500, null=True, blank=True)
    consumeSet = []

    def __str__(self):
        return f"{self.user.username} Profile"

    def ConsumeSetbyDate(self, chosenDateYear, chosenDateMonth, chosenDateDay):
        criterion1 = Q(owner__id=self.user.id)
        criterion2 = Q(
            created__year=chosenDateYear,
            created__month=chosenDateMonth,
            created__day=chosenDateDay,
        )

        self.consumeSet = Consume.objects.filter(criterion1 & criterion2) 

    @property
    def carbsSum(self):
        cSum = 0
        for consume in self.consumeSet:
            quantity = (consume.quantity) / 100
            cSum += consume.food.carbs * quantity
            print("consume food ", quantity)
        return round(cSum, 2)

    @property
    def proteinsSum(self):
        cSum = 0
        for consume in self.consumeSet:
            quantity = (consume.quantity) / 100
            cSum += consume.food.protein * quantity
        return round(cSum, 2)

    @property
    def fatsSum(self):
        cSum = 0
        for consume in self.consumeSet:
            quantity = (consume.quantity) / 100
            cSum += consume.food.fats * quantity
        return round(cSum, 2)

    @property
    def caloriesSum(self):
        cSum = 0
        for consume in self.consumeSet:
            quantity = (consume.quantity) / 100
            cSum += consume.food.calories * quantity
        return round(cSum, 2)
