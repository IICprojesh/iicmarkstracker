from django.contrib import admin
from .models import (
    SessionYearModel,
    Courses,
    Subjects,
    Student,
    Studentresult,
    YearSemester,
    MCQ_WEEK

)

# Register your models here.

admin.site.register([SessionYearModel,YearSemester,Courses,Subjects,Student,Studentresult,MCQ_WEEK])
