from django.db import models


class Poll(models.Model):
    question = models.CharField(max_length=100)
    option_a = models.CharField(max_length=15)
    option_b = models.CharField(max_length=15)
    option_c = models.CharField(max_length=15)
    option_d = models.CharField(max_length=15)
