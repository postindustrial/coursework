from django.contrib.admin import site
from info.models import Student, Day, Week, Schedule, Group, Classes, Course, Major, Taught_Course, Teacher, Final, Building

site.register(Schedule)
site.register(Group)
site.register(Classes)
site.register(Course)
site.register(Teacher)
site.register(Final)
site.register(Building)
site.register(Major)
site.register(Taught_Course)
site.register(Student)
site.register(Day)
site.register(Week)