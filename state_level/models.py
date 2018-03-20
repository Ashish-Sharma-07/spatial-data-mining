# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis.db import models
# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
class SummaryInfo(models.Model):
    distname = models.CharField(max_length=200, blank=True, null=True)
    block_name = models.CharField(max_length=200, blank=True, null=True)
    school = models.BigIntegerField(blank=True, null=True)
    teacher = models.BigIntegerField(blank=True, null=True)
    student = models.BigIntegerField(blank=True, null=True)
    toiletwater_b = models.BigIntegerField(blank=True, null=True)
    toiletwater_g = models.BigIntegerField(blank=True, null=True)
    toiletb_func = models.BigIntegerField(blank=True, null=True)
    urinals_b = models.BigIntegerField(blank=True, null=True)
    toiletg_func = models.BigIntegerField(blank=True, null=True)
    urinals_g = models.BigIntegerField(blank=True, null=True)
    handwash_count = models.BigIntegerField(blank=True, null=True)
    schcat_1 = models.BigIntegerField(blank=True, null=True)
    schcat_2 = models.BigIntegerField(blank=True, null=True)
    schcat_3 = models.BigIntegerField(blank=True, null=True)
    schcat_4 = models.BigIntegerField(blank=True, null=True)
    schcat_5 = models.BigIntegerField(blank=True, null=True)
    schcat_6 = models.BigIntegerField(blank=True, null=True)
    schcat_7 = models.BigIntegerField(blank=True, null=True)
    schcat_8 = models.BigIntegerField(blank=True, null=True)
    schcat_10 = models.BigIntegerField(blank=True, null=True)
    schcat_11 = models.BigIntegerField(blank=True, null=True)
    water_1 = models.BigIntegerField(blank=True, null=True)
    water_2 = models.BigIntegerField(blank=True, null=True)
    water_3 = models.BigIntegerField(blank=True, null=True)
    water_4 = models.BigIntegerField(blank=True, null=True)
    water_5 = models.BigIntegerField(blank=True, null=True)
    bndrywall_1 = models.BigIntegerField(blank=True, null=True)
    bndrywall_2 = models.BigIntegerField(blank=True, null=True)
    bndrywall_3 = models.BigIntegerField(blank=True, null=True)
    bndrywall_4 = models.BigIntegerField(blank=True, null=True)
    bndrywall_5 = models.BigIntegerField(blank=True, null=True)
    bndrywall_6 = models.BigIntegerField(blank=True, null=True)
    bndrywall_7 = models.BigIntegerField(blank=True, null=True)
    bndrywall_8 = models.BigIntegerField(blank=True, null=True)
    schmgt_1 = models.BigIntegerField(blank=True, null=True)
    schmgt_2 = models.BigIntegerField(blank=True, null=True)
    schmgt_3 = models.BigIntegerField(blank=True, null=True)
    schmgt_4 = models.BigIntegerField(blank=True, null=True)
    schmgt_5 = models.BigIntegerField(blank=True, null=True)
    schmgt_6 = models.BigIntegerField(blank=True, null=True)
    schmgt_7 = models.BigIntegerField(blank=True, null=True)
    schmgt_8 = models.BigIntegerField(blank=True, null=True)
    schmgt_97 = models.BigIntegerField(blank=True, null=True)
    schmgt_98 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'summary_info'
