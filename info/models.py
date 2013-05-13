# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User



class Major (models.Model):

    class Meta:
        verbose_name_plural = u'Специальности'

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

class Group (models.Model):

    class Meta:
        verbose_name_plural = u'Группы'

    name = models.CharField(max_length=7)
    major = models.ForeignKey(Major)

    def __unicode__(self):
        return self.name

class Student (models.Model):

    class Meta:
        verbose_name_plural = u'Студенты'

    user = models.OneToOneField(User)
    username = models.CharField(max_length=50)
    last_login = models.DateTimeField(blank=True)
    is_active = models.BooleanField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    group = models.ForeignKey(Group)
    invite_key = models.CharField(max_length=20)

    people = models.Manager()

    def __unicode__(self):
        return self.last_name

class Classes (models.Model):

    class Meta:
        verbose_name_plural = u'Занятия'

    begin_time = models.CharField(max_length=5)
    end_time = models.CharField(max_length=5)

    def __unicode__(self):
        return self.begin_time

class Building (models.Model):

    class Meta:
        verbose_name_plural = u'Строения'

    name = models.CharField(max_length=4)

    def __unicode__(self):
        return self.name

class Teacher (models.Model):

    class Meta:
        verbose_name_plural = u'Преподаватели'

    last_name = models.CharField(max_length=25)
    initials = models.CharField(max_length=4)
    full_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.last_name + ' ' + self.initials

class Final (models.Model):

    class Meta:
        verbose_name_plural = u'Завершение'

    form = models.CharField(max_length=20)

    def __unicode__(self):
        return self.form

class Course (models.Model):

    class Meta:
        verbose_name_plural = u'Дисциплины'

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Taught_Course (models.Model):

    class Meta:
        verbose_name_plural = u'Преподаваемые курсы'

    name = models.ForeignKey(Course)
    group = models.ForeignKey(Group)
    teacher = models.ForeignKey(Teacher)
    hours = models.IntegerField()
    final = models.ForeignKey(Final)

    def __unicode__(self):
        return self.name.name + ' ' + self.teacher.last_name

class Day (models.Model):
    name = models.CharField(max_length=12)

    class Meta:
        verbose_name_plural = u'Дни недели'

    def __unicode__(self):
        return self.name

class Week (models.Model):
    name = models.CharField(max_length=14)

    class Meta:
        verbose_name_plural = u'Недели'

    def __unicode__(self):
        return self.name

class Schedule (models.Model):

    class Meta:
        verbose_name_plural = u'Расписание'

    week = models.ForeignKey(Week)
    day = models.ForeignKey(Day)
    time = models.ForeignKey(Classes)
    course = models.ForeignKey(Taught_Course)
    room = models.CharField(max_length=10)
    building = models.ForeignKey(Building)

    def __unicode__(self):
        return self.course.group.name + ' ' + self.week.name + ' ' + self.day.name + ' ' + self.course.name.name



# Create your models here.

