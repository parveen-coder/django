from django.shortcuts import render
from django.http import HttpResponse,JsonResponse


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

def listdic(request):
    student_list = [
        {
            "id": 101,
            "name": "Rahul",
            "course": "B.Tech",
            "marks": 85
        },
        {
            "id": 102,
            "name": "Priya",
            "course": "BCA",
            "marks": 92
        },
        {
            "id": 103,
            "name": "Aman",
            "course": "B.Tech",
            "marks": 78
        }
    ]

    return render(request, "listdict.html", {"students": student_list})


def newdict(request):
    students=[ {
        "name": "Rahul",
        "subjects": ["Python", "Django"],
        "marks": [85, 90]
    },
    {
        "name": "Priya",
        "subjects": ["Java", "C++"],
        "marks": [88, 95]
    }]
    return render(request,'newdict.html', {"students":students})



students = [
    {"name": "Rahul", "rollno": 101, "marks": 85},
    {"name": "Priya", "rollno": 102, "marks": 92},
    {"name": "Aman", "rollno": 103, "marks": 78},
    {"name": "Neha", "rollno": 104, "marks": 88},
    {"name": "Rohit", "rollno": 105, "marks": 75},
]


def student_details(request, rollno):

    for student in students:
        if student["rollno"] == rollno:
            return render(request, "student.html",{"student": student})

    return render(request, "student/studentsp.html", {"student": None})

def studentdict(request, roll):
 
    Student=[{ "name":"Parveen", "rollno":23, "marks":92 },
    {"name":"Pavnoor","rollno":24, "marks":99 },
    {"name":"Pavjot", "rollno":29,"marks":98  }]

    for i in Student:
        if(i["rollno"]==roll):
            return render(request, 'studentdetail5.html', {"s": i})
    else:
        return render(request, 'studentdetail5.html')


# dynamic response->dynamic template 
   
def studentdict2(request, roll):
    Student=[{ "name":"Parveen", "rollno":23, "marks":92 },
    {"name":"Pavnoor","rollno":24, "marks":99 },
    {"name":"Pavjot", "rollno":29,"marks":98  }]
   
    for i in Student:
        if i["rollno"]==roll:
            return render(request, 'studentsp.html', {"i":i})
        else:
            return render(request,'studentsp.html')

# Template inheritance 

# def usertemplate(request):

#     return render(request,'newhome.html')



def homenew(request):
    return render(request, "users.html")


def student_listnew(request):
    students = [ {"rollno": 101, "name": "Rahul", "course": "B.Tech", "marks": 85},
                {"rollno": 102, "name": "Priya", "course": "BCA","marks": 92},
                {"rollno": 103, "name": "Aman", "course": "B.Tech", "marks": 78 },]

    return render(request, "students.html",{"students": students})


def aboutnew(request):
    return render(request, "about.html")

def divide(request):
    a = 10
    b = 2
    # result=a/b
    # return HttpResponse(result)

    try:
        result = a / b
        # return HttpResponse(result)
        return render(request, "result.html", {"result": result })

    except ZeroDivisionError:
        # return HttpResponse("Cannot divide by zero")
        return render(request, "result.html", { "error": "Cannot divide by zero"})


def userdetails(request, roll):
    user=[{"name":"Navi","age":39,"address":"Jalandhar"},
          {"name":"Pooja","age":32,"address":"Jalandhar"},
          {"name":"Bab","age":3,"address":"Jalandhar"}]
    for i in user:
        if(i["age"]==roll):
            return render(request,'userdetails.html',{'u':i})
    else:
        return render(request,'userdetails.html')


def calculate(request):
    # number = int(request.GET.get("number"))
    
    # result = 100 / number

    # return HttpResponse(result)

    try:

        number = int(request.GET.get("number"))

        result = 100 / number

        return render(request, "result1.html", { "number": number,"result": result})

    except ValueError:

        return render(request, "error.html", {"message": "Please enter a valid number."},status=400)

    except ZeroDivisionError:

        return render(request,"error.html",{"message": "Not possible to divide by zero."},status=400)
    
    except TypeError:
    
            return render(request, "error.html", {"message": "need to pass the number and value"},status=400)
    


def studentnew(request):
    name = "Rahul"
    age = 21

    print("Name:", name)
    print("Age:", age)

    return HttpResponse("rollno")


def studenttwo(request):

    name = "Rahul"
    age = 21

    # breakpoint()

    result = age + 10
    breakpoint()

    return HttpResponse(result)

def home3(request):
    name=request.GET.get('name')
    # name="Rohit"
    return render(request,'home.html',{"name":name})

def wednesday(request):
    d={"a":"34", "r":45}
    e=d["e"]
    return HttpResponse(e)
    # try:
        # return HttpResponse(e)
    # except KeyError:
    #     return HttpResponse("e is not defined ", status=500)

def adminpage(request):
    is_admin=True
    if not is_admin:
        return HttpResponse("you are not allowed", status=403)
    return HttpResponse("welcome User")

def wednes(request):
    a=10
    b=0
    result=a/b
    # print(result)
    return HttpResponse(result)
    # return HttpResponse(kt)