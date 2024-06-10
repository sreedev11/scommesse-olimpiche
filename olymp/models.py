from django.db import models
from django.contrib.auth.models import User


class Registration(models.Model):
    password = models.CharField(max_length=200, null=True)
    bet_amt = models.CharField(max_length=200, null=True)
    user_role = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)



class Olympic_prediction(models.Model):
    gender = models.CharField(max_length=200, null=True)
    age = models.CharField(max_length=200, null=True)
    height = models.CharField(max_length=200, null=True)
    team = models.CharField(max_length=200, null=True)
    event = models.CharField(max_length=200, null=True)
    medal_status = models.CharField(max_length=200, null=True)
    olym_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True)


class Contact(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    message = models.CharField(max_length=200, null=True)


class Playss(models.Model):
    sport = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    country1 = models.CharField(max_length=200, null=True)
    final_result = models.CharField(max_length=200, null=True)


class Betting(models.Model):
    pred_coun = models.CharField(max_length=200, null=True)
    bet_playy = models.ForeignKey(Playss, on_delete=models.CASCADE, null=True, related_name='bett_to_plays')
    bet_reg = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, related_name = 'bett_to_regis')



class Betting_admin_amount(models.Model):
    amount = models.CharField(max_length=200, null=True)
    bet_playy_admin = models.ForeignKey(Playss, on_delete=models.CASCADE, null=True, related_name='bett_to_plays_admin')
    bet_reg_admin = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, related_name='bett_to_regis_admin')


class Betting_user_amount(models.Model):
    amount = models.CharField(max_length=200, null=True)
    bet_playy_user = models.ForeignKey(Playss, on_delete=models.CASCADE, null=True, related_name='bett_to_plays_user')
    bet_reg_user = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, related_name='bett_to_regis_user')





class Bankk(models.Model):
    amount = models.CharField(max_length=200, null=True)
    bank_reg = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True,related_name='bank_to_regis')