from django.db import models

class SessionYearModel(models.Model):
    session_start_year = models.DateField()
    session_end_year = models.DateField()

    def __str__(self):
        return f"{self.session_start_year}- {self.session_end_year}"


class Courses(models.Model):
    course_name = models.CharField(max_length=255,primary_key=True)


    def __str__(self):
        return self.course_name


class YearSemester(models.Model):
    YEAR = [
        ("ONE","One"),
        ("TWO","Two"),
        ("THREE","Three")
    ]
    SEMESTER = [
        ("FIRST","First"),
        ("SECOND","Second")
    ]
    year = models.CharField(max_length=15,choices=YEAR)
    sem = models.CharField(max_length=30,choices=SEMESTER)


    def get_model_object_from_string(mystr):
        str_lists = mystr.split()
        year = str_lists[1]
        semester = str_lists[3]

        return YearSemester.objects.filter(year = year,sem=semester)[0]

    def __str__(self):
        return f"Year {self.year} of {self.sem} semester"

class MCQ_WEEK(models.Model):
    WEEK = [
        ("FIRST","First"),
        ("SECOND","Second"),
        ("THIRD","Third"),
        ("FOUR","Four"),
        ("FIVE","Five"),
        ("SIX","Six"),
        ("SEVEN","Seven"),
        ("EIGHT","Eight"),
        ("NINE","Nine"),
        ("TEN","Ten"),
        ("ELEVEN","Eleven"),
        ("TWELVE","Twelve"),
    ]
    week = models.CharField(max_length=20,choices=WEEK)


    def __str__(self):
        return self.week


class Subjects(models.Model):
    subject_name = models.CharField(max_length=255)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE)
    term = models.ForeignKey(YearSemester, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.subject_name} of term {self.term}"


class Student(models.Model):
 
    student_id = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=4)
    year_sem = models.ForeignKey(YearSemester,on_delete=models.CASCADE,default = None)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,default = None)
    email = models.CharField(max_length=100,default="no email")
    is_active = models.BooleanField(default = True)


    def __str__(self):
        return self.name

class Studentresult(models.Model):
   
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    marks = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    week = models.ForeignKey(MCQ_WEEK,on_delete=models.DO_NOTHING)
    

    def __str__(self):
        return f"{self.student}-{self.subject}{self.marks}"



