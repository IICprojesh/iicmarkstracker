from .models import Student, Studentresult
import re

def verify_value_as_email(email):
    print(f"email validation: {email}")
    if email and not re.match(r"np\w+@iic.edu.np",email):
        return True, f"The provided value {email} in student email column is not valid"


def verify_student_from_sheet(student_email,year_sem):
    try:
        student_yearsem = Student.objects.filter(email=student_email)[0].year_sem
    except:
        student_yearsem = None

    if ((student_yearsem and not str(student_yearsem) == year_sem)):
        return True, f"Name of student {Student.objects.filter(email = student_email)[0].name} is not valid"

def validate_week(week_obj, subject_object,mcq_num):
    print(f"mcq_num: {mcq_num}")
    student_result = Studentresult.objects.filter(week=week_obj,subject=subject_object,mcq_num=mcq_num)
    print(f"student_result: {student_result}")
    if len(student_result)>0:
        return True, f"MCQ for week {week_obj.get_week_display()} has already been posted"
    

def overall_response_sheet_verification(student_email,year_sem):
    invalid_email = verify_value_as_email(student_email)
    if invalid_email:
        return invalid_email[0], invalid_email[1]
    invalid_student = verify_student_from_sheet(student_email,year_sem)
    if invalid_student:
        return invalid_student[0], invalid_student[1]
    