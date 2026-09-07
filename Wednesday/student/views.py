from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse

# Create your views here.

def home(request, name,id):
    print(request)
    # name="Ram"
    # id=12
    # return HttpResponse("<h1>Hello welcome</h1>")
    return render(request,'file1.html',{"n":name,"id":id})
    # return render(request,'home.html',{"name1":"Raman"})

def user(request):
    return HttpResponse("hello")

def json1(request):
    student={
        'name':"Naman",
        'age':12
    }
    return JsonResponse(student)

def user1(request):
    return HttpResponse("<h1>Hello How are you?</h1>")

def user2(request):
    name="Rabaab"
    rollno=123
    # return HttpResponse(name + " " + str(rollno))
    return HttpResponse(f'<p>Name of the student is : {name} <br> Roll no of student is : {rollno}</p>')

def user3(request):
    name=request.GET.get('name')
    age=request.GET.get('age')
    return HttpResponse(f'<p>Name of the student is : {name} <br> Roll no of student is : {age}</p>')


def user4(request,id,name):
    return HttpResponse(f'user name : {name} and {id}')

def user7(request, name):
    return HttpResponse(name)

def studentlist(request):
    student_list = ["Rahul", "Priya", "Aman", "Neha"]
    return render(request, 'student.html',{"li": student_list})
    # html = "<h1>Student List</h1>"
    # html += "<table border='1'>"
    # html += "<tr><th>Name</th></tr>"

    # for student in student_list:
    #     html += f"<tr><td>{student}</td></tr>"

    # html += "</table>"

    # return HttpResponse(html)

def studentlist1(request):
    studentlist=[ [1,"Raman",21], [2,"Aman",34], [4,"Neetu",45]]
    return render(request,'student1.html',{'s':studentlist})
    html="<h1>Student List</h1>"
    html+="<table border=1>"
    html+="<tr>"
    html+="<th>Sno</th>"
    html+="<th>Name</th>"
    html+="<th>Roll no</th>"
    html+="</tr>"

    for student in studentlist:
        html+="<tr>"
        html+=f"<td>{student[0]}</td>"
        html+=f"<td>{student[1]}</td>"
        html+=f"<td>{student[2]}</td>"
        html+="</tr>"
    html+="</table>"

    return HttpResponse(html)

def linkuse(request):
   
    student_1 = reverse('student')

    # return HttpResponse(
    #     f'<a href="{student_url}">Student List</a>'
    # )
    return HttpResponse(
        f'<a href="{student_1}">Student List</a>'
    )

students = ["Rahul", "Priya", "Aman", "Neha"]

def studentindex(request, id):
    return HttpResponse(students[id])

def regexp(request,id):
    return HttpResponse(f"student ID is : {id}")


def html1(request,name):
    print(request)
    name1=name
    return render(request, 'user.html',{"n":name})

def listdata(request):
    list=[[1,"Ram",99],
          [2,"Sham", 96],
          [3,"Raman",92]
          ]
    name="Parneet"
    age=3
    return render(request,'list.html',{"li":list,'n':name,'r':age})

def userdict(request):
     dict={"name":"Rabaab","age":67,"rollno":12}
     return render(request,'studentdict.html',{"d":dict})