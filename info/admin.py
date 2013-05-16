from django.contrib.admin import site
from info.models import Student, Schedule, Group, Course, Major, TaughtCourse, Teacher, Building, Settings

site.register(Schedule)
site.register(Group)
site.register(Course)
site.register(Teacher)
site.register(Building)
site.register(Major)
site.register(TaughtCourse)
site.register(Student)
site.register(Settings)