from django.db import models
from django.core import validators

# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    phone_number = models.BigIntegerField(
        validators=[validators.MinValueValidator(7000000000), validators.MaxValueValidator(9999999999)]
    )
    monthly_salary = models.IntegerField()
    approved_limit = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    

class Loan(models.Model):
    borrower = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.IntegerField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_payment = models.IntegerField(blank=True, null=True)
    emis_paid_on_time = models.IntegerField(default=0)
    date_of_approval = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.borrower.first_name + " " + self.borrower.last_name + " " + str(self.id)
    


