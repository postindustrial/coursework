# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
import datetime

WEEKDAYS = (
    (0, u'Понедельник'),
    (1, u'Вторник'),
    (2, u'Среда'),
    (3, u'Четверг'),
    (4, u'Пятница'),
    (5, u'Суббота'),
    (6, u'Воскресенье'),
)

WEEKS = (
    (1, u'Нечетная неделя'),
    (2, u'Четная неделя'),
)

BEGIN_TIMES = (
    (1, u'8:00'),
    (2, u'9:45'),
    (3, u'11:30'),
    (4, u'13:35'),
    (5, u'15:20'),
    (6, u'17:05'),
    (7, u'18:50'),
)

END_TIMES = (
    (1, u'9:35'),
    (2, u'11:20'),
    (3, u'13:05'),
    (4, u'15:10'),
    (5, u'16:55'),
    (6, u'18:40'),
    (7, u'20:25'),
)

FINALS = (
    (1, u'Зачет'),
    (2, u'Экзамен'),
)

def weekday_processor(request):
    return ({'week_days': WEEKDAYS})

def datetime_processor(request):
    today = datetime.datetime.today()
    delta_days = (today - settings.SEMESTER_BEGIN).days
    current_week = 1 + (delta_days / 7) % 2
    context = {
        'today': datetime.datetime.today().weekday(),
        'tomorrow': (today.weekday() + 1) % 6,
        'current_week': current_week,
        'current_date': datetime.datetime.today(),
    }
    return (context)

class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        return self.model._default_manager.create(username=username)

class Major (models.Model):

    class Meta:
        verbose_name_plural = u'Специальности'

    name = models.CharField(verbose_name=u'Название специальности', max_length=100)
    code = models.CharField(verbose_name=u'Код специальности', max_length=10)

    def __unicode__(self):
        return self.name

class Group (models.Model):

    class Meta:
        verbose_name_plural = u'Группы'

    name = models.CharField(verbose_name=u'Название группы', max_length=7)
    major = models.ForeignKey(Major)

    def __unicode__(self):
        return self.name

class Student (AbstractUser):

    class Meta:
        verbose_name_plural = u'Студенты'

    patronymic = models.CharField(verbose_name=u'Отчество', max_length=20)
    group = models.CharField(verbose_name=u'Название группы', max_length=7)
    #USERNAME_FIELD = 'username'
    #REQUIRED_FIELDS = ['username']

    #objects = CustomUserManager()

    def is_authenticated(self):
        return True

    def get_group_name(self):
        return self.group

    def __unicode__(self):
        return self.last_name


class Building (models.Model):

    class Meta:
        verbose_name_plural = u'Строения'

    name = models.CharField(verbose_name=u'Название корпуса', max_length=4)

    def __unicode__(self):
        return self.name

class Teacher (models.Model):

    class Meta:
        verbose_name_plural = u'Преподаватели'

    last_name = models.CharField(verbose_name=u'Фамилия', max_length=25)
    initials = models.CharField(verbose_name=u'Инициалы', max_length=4)
    full_name = models.CharField(verbose_name=u'Имя и отчество', max_length=50)
    post = models.CharField(verbose_name=u'Должность', max_length=100)

    def __unicode__(self):
        return self.last_name + ' ' + self.initials


class Course (models.Model):

    class Meta:
        verbose_name_plural = u'Дисциплины'

    name = models.CharField(verbose_name=u'Название дисциплины', max_length=100)

    def __unicode__(self):
        return self.name


class TaughtCourse (models.Model):

    class Meta:
        verbose_name_plural = u'Преподаваемые курсы'

    name = models.ForeignKey(Course)
    group = models.ForeignKey(Group)
    teacher = models.ForeignKey(Teacher)
    hours = models.IntegerField(verbose_name=u'Количество часов')
    final = models.IntegerField(verbose_name=u'Завершение', choices=FINALS)

    def __unicode__(self):
        return self.name.name + ' ' + self.teacher.last_name


class Schedule (models.Model):

    class Meta:
        verbose_name_plural = u'Расписание'

    week = models.IntegerField(verbose_name=u'Неделя', choices=WEEKS)
    weekday = models.IntegerField(verbose_name=u'День недели', choices=WEEKDAYS)
    begin_time = models.IntegerField(verbose_name=u'Начало пары', choices=BEGIN_TIMES)
    end_time = models.IntegerField(verbose_name=u'Окончание пары', choices=END_TIMES)
    course = models.ForeignKey(TaughtCourse)
    room = models.CharField(verbose_name=u'Аудитория', max_length=10)
    building = models.ForeignKey(Building)

    def __unicode__(self):
        return self.course.group.name + ' ' + str(self.week) + ' ' + str(self.weekday) + ' ' + self.course.name.name

class Settings (models.Model):

    class Meta:
        verbose_name_plural = u'Настройки показа'

    student = models.ForeignKey(Student)
    schedule = models.ForeignKey(Schedule)

    def __unicode__(self):
        return self.student.last_name + ' ' + \
               self.schedule.course.group.name + ' ' + \
               str(self.schedule.week) + ' ' + \
               str(self.schedule.weekday) + ' ' + \
               self.schedule.course.name.name



# Create your models here.

