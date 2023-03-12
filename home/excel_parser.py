import openpyxl
from .models import Student, Studentresult, Subjects, YearSemester, Courses, MCQ_WEEK
from .validate_excel_sheet import overall_response_sheet_verification, validate_week


#     print("inside verify_student_from_sheet")
#     print(f"student_email: {student_email}")
#     print(f"year_sem: {year_sem}")
#     try:
#         student_yearsem = Student.objects.filter(email=student_email)[0].year_sem
#     except:
#         student_yearsem = None
#     print(f"student: {student_yearsem}")
#     print(f"year_sem: {year_sem}")

#     if ((student_yearsem and not str(student_yearsem) == year_sem)):
#         print("found some invalid student")
#         print(f"Name of student {Student.objects.filter(email = student_email)[0].name} is not valid")
#         return True


def get_student_object_and_marks_of_student(row):
    print("inside get_student_object_and_marks_of_student")
    print(f"row: {row}")
    email,mark = row
    print(f"email: {email}")
    try:
        student = Student.objects.filter(email=email)[0]
    except Exception:
        student  = None
    return student,mark

def get_subject_object(subject,course,year_sem):
    course = Courses.objects.filter(course_name=course)[0]
    term = YearSemester.get_model_object_from_string(year_sem)
    print(f"course: {course}")
    print(f"term: {term}")
    print(f"subject: {subject}")
    subject_object = Subjects.objects.filter(subject_name=subject,course=course,term=term)[0]
    print(f"subject_object: {subject_object}")
    return subject_object


def parse_excel_and_add_student_to_database(excel_file,course_obj,yearsem_obj):
    print("inside parse excel")
    workbook = openpyxl.load_workbook(excel_file,read_only=True)
    ws = workbook.active

    model_objects = []
    for index, row in enumerate(ws.values):
        print(f"rows at top: {row[1:]}")
        if index==0:
            continue

        elif not row[1:][1]==None:
            student_id,email, name, section = row[1:]
            section = section.lower()
            model_objects.append(Student(student_id = student_id,email=email, name=name,section=section,year_sem=yearsem_obj,course = course_obj))


        else:
            print(f"new rows for length 1: {row[1:]}")
            student_id= row[1:][0]
            name,section = row[1:][2:]
            section = section.lower()
            model_objects.append(Student(student_id = student_id,name=name,section=section,year_sem=yearsem_obj,course = course_obj))

    # code to bulk create the objects
    Student.objects.bulk_create(model_objects)
    print("sucessfully created the student rows")


def parse_excel_to_add_student_marks_to_database(excelfile,course,year_sem,subject,week):
    model_objects = []
    # get the student object from the email id of student
    # get the subject object from subject value
    # get marks from excel file
    # week object from week
    workbook = openpyxl.load_workbook(excelfile,read_only=True)
    ws = workbook.active
    total_number_of_questions = 0
    subject = get_subject_object(subject,course,year_sem)
    print(f"subject saa: {subject}")
    week_object = MCQ_WEEK.objects.filter(week=week)[0]
    invalid_week = validate_week(week_object,subject)
    if invalid_week:
        return invalid_week[0], invalid_week[1]
    print(f"week_object: {week_object}")
    for index, row in enumerate(ws.values):
        if index==0:
            total_number_of_questions = len(row[5:])
            continue
        else:
            # create a function that verifies if the excel sheet contains the student that and the student also belong to same subject or not
            print(f"row_1: {row[1]}")
            student_email = row[1]
            is_invalid_sheet= overall_response_sheet_verification(student_email,year_sem)
            if is_invalid_sheet:
                return is_invalid_sheet[0], is_invalid_sheet[1]

            student,mark = get_student_object_and_marks_of_student(row[1:3])
            if student == None:
                continue
            print(f"total number of questions: {total_number_of_questions}")
            mark_in_percentage = round((mark/total_number_of_questions)*100,2)
            # creating a student object from all the extracted information
            student_yearsem = Student.objects.filter(email=student_email)[0].year_sem
            model_objects.append(Studentresult(student=student,subject=subject,marks=mark_in_percentage,week=week_object,year_sem=student_yearsem))

    Studentresult.objects.bulk_create(model_objects)
    return False, "Sucessfully added marks from response to database"
           
           






        
            


           


