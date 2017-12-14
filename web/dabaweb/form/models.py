#coding:utf-8
from django.db import models

# Create your models here.
class User(models.Model):
    uid = models.IntegerField(verbose_name=u'id',primary_key=True)
    name_link = models.ForeignKey('User_data')
    code_link = models.ForeignKey('Code_data')

    class Meta:
        verbose_name = u'主键管理'
        verbose_name_plural = verbose_name

class User_data(models.Model):
    name = models.CharField(max_length=30,verbose_name=u'名字',null=False,blank=False,primary_key=True)
    money = models.IntegerField(verbose_name=u'工资')

    class Meta:
        verbose_name = u'用户管理'
        verbose_name_plural = verbose_name

class Code_data(models.Model):
    code = models.IntegerField(verbose_name=u'工号',null=False,blank=False,primary_key=True)
    group = models.CharField(max_length=100,verbose_name=u'组名')

    class Meta:
        verbose_name = u'号码管理'
        verbose_name_plural = verbose_name