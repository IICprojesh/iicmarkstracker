from .models import Studentresult, Student, YearSemester, Subjects

def verify_excel(filename):
    extension = filename.split(".")[-1]
    return True if extension=="xlsx" else False

def get_marks_on_all_subjects_of_students(student_id, year_sem):
    student = Student.objects.filter(student_id = student_id)[0] 
    year_sem = YearSemester.get_model_object_from_string(year_sem)
    total_student_marks = Studentresult.objects.filter(student=student,year_sem=year_sem)
    print(f"total_student_marks: {total_student_marks}")
    # get all subjects
    subjects = Subjects.objects.filter(course = student.course,term = year_sem).values("subject_name")
    print(f"subjects: {subjects}")
    subjects = [value for subject in subjects for _, value in subject.items()]
    # sort the subjects
    subjects = sorted(subjects)

    # get all the weeks numberr of mcq that has completed
    mcq_weeks = Studentresult.objects.filter(year_sem = year_sem)
    mcq_weeks = {mcq.week for mcq in mcq_weeks}


    # mcq_weeks = sorted(mcq_weeks.items(),key =lambda x: x[1])
    print(f"mcq_weeks sorted: {mcq_weeks}")
    v = list(mcq_weeks)[0]
  

    marks_dict = dict()
    for mark in total_student_marks:
        if mark.week in marks_dict:
            marks_dict[mark.week].append((mark.subject.subject_name,mark.marks))
        else:
            marks_dict[mark.week] = [(mark.subject.subject_name,mark.marks)]
    print(marks_dict)


    # add all the remaining weeks marks of that student  as absent
    for week in mcq_weeks:
        if week not in marks_dict:
            marks_dict[week] = []
        marks_info = marks_dict[week]
        subject_marks_included = [subject for subject,_ in marks_info]
        for subject in subjects:
            if subject not in subject_marks_included:
                marks_dict[week].append([subject,"NA"])

    marks_dict = sorted(marks_dict.items(),key=lambda x: (int(x[0].week)))
    sorted_marks_dict = {}
    for week, subject_marks in marks_dict:
        sorted_marks = sorted(subject_marks,key = lambda x: x[0])
        sorted_marks_dict[week] = sorted_marks
    subjects.insert(0,"WEEK")
    return sorted_marks_dict, subjects




    
    





    