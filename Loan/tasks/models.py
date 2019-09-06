from django.db import models


class Loan(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    summ_initial = models.IntegerField(max_length=5, db_column='Initial summ')


class BodyHistory(models.Model):
    history_date = models.DateField(db_column='History_date')
    body = models.IntegerField(max_length=5, db_column='Body')
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)


class DayCharge(models.Model):
    charge_date = models.DateField(db_column='Charge_date')
    summ = models.IntegerField(max_length=5, db_column='Summ')
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
