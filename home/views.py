from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
# from bs4 import BeautifulSoup
from django.contrib import messages





from .excel_parser import (parse_excel_and_add_student_to_database,
                            parse_excel_to_add_student_marks_to_database
)
from .models import Courses, YearSemester , Subjects, MCQ_WEEK, Student, MCQNums
from .helper import verify_excel, get_marks_on_all_subjects_of_students
from .generate_excel_sheet import parse_html


# Create your views here.
def home(request):
    if request.method=="POST":
        print("inside post requst")
        print(f"request: {request.POST}")
        excelfile = request.FILES["excelfile"]
        course = request.POST.get("course")
        yearsem = request.POST.get("yearsem")
        course_object = Courses.objects.get(course_name = course)
        year_semester_object = YearSemester.get_model_object_from_string(yearsem)

        print(f"course_object: {course_object}")
        print(f"year_semester_object: {year_semester_object}")
        parse_excel_and_add_student_to_database(excelfile,course_object,year_semester_object)
        messages.info(request, f"Sucessfully added student of {yearsem} into database")
        return redirect("home:add_students")
        
    courses = Courses.objects.all()
    terms = YearSemester.objects.all()
    
    context = {"courses":courses,"terms":terms}
    return render(request,'index.html',context)

def insert_marks(request):
    """
    view function to add marks of students from the 
    excel to the database
    """
    if request.method=="POST":
        """
        this if statement is used to check if the request is ajax or not and handel the ajax requst if 
        it is like that
        """
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            post_data = json.load(request)['post_data']
            year_sem = YearSemester.get_model_object_from_string(post_data["year_sem"])
            subjects = Subjects.objects.filter(course=post_data["course"],term=year_sem).values("subject_name")
            subjects_lists = [value for subject in subjects for key,value in subject.items()]
            return JsonResponse({"subjects":subjects_lists})
        """
        this code content is used to handel the normal post request except ajax request
        """
        course = request.POST.get("course")
        year_sem = request.POST.get("yearsem")
        subject =request.POST.get("subject")
        week = request.POST.get("week")
        excelfile = request.FILES["excelfile"]

        print(f"subject name inside viwes: {subject}")


        # validate the excel file
        try:
            is_excel = verify_excel(str(excelfile))
            if not is_excel:
                raise Exception
            
        except Exception:
            return "is not a valid excel file"
        

        is_error, msg = parse_excel_to_add_student_marks_to_database(excelfile,course,year_sem,subject,week)
        if is_error:
            messages.warning(request,msg)
            print(msg)
        else:
            messages.success(request,msg)

        return redirect("home:insert_marks")



    courses = Courses.objects.all()
    year_sems = YearSemester.objects.all()
    weeks = MCQ_WEEK.objects.all()

    context = {"courses":courses,"year_sems":year_sems,"weeks":weeks}
    return render(request,'insert_marks.html',context)


"""
View function to get the result from the database
"""
def get_results(request):
    if request.method=="POST":
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            post_data = json.load(request)['post_data']
            print(f"post_data: {post_data}")
            student_name, student_term = post_data.get("name"),post_data.get("ysem")
            student_term = YearSemester.get_model_object_from_string(student_term)
            print(f"student_term: {student_term}")
            student_ids = Student.objects.filter(name__icontains=student_name,year_sem=student_term).values("student_id")
            print(f"student_ids",student_ids)
            student_ids = [value for student in student_ids for key, value in student.items()]
            return JsonResponse({"ids":student_ids})
        
        # logic to handle general post request
        year_sem = request.POST.get("yearsem")
        student_id  =request.POST.get("london_id")
        print(f"year_sem: {year_sem}")
        print(f"student_id: {student_id}")
        context = dict()
        context["name"] = Student.objects.filter(student_id = student_id)[0].name
        context["student_id"] = student_id
        context["year_sem"] = year_sem


        # logic to get marks acquired marks of student from database
        sorted_marks, headings = get_marks_on_all_subjects_of_students(student_id, year_sem)
        context["sorted_marks"] = sorted_marks
        context["headings"] = headings
        

        return render(request,"display_marks.html",context)


    year_sems = YearSemester.objects.all()
    context = {"terms":year_sems}
    return render(request,"student_marks_extraction_form.html",context)


def download_and_send_excel(request):
    if request.method=="POST":
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            html_content = request.body.decode('utf-8')
            workbook = parse_html(html_content)
            print(f"workbook: {workbook}")
            print(f"workbook type: {type(workbook)}")
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=mcq_results.xlsx'
            workbook.save(response)
            print(f"sucessfully created excel file")

            return response
            # return HttpResponse(str(soup))
