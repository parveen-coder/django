from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from .forms import StudentForm
# from .forms import StudentDetails
from django.core.files.storage import FileSystemStorage
from .forms import RegisterStudent
from .forms import ExamForm
from .forms import Newform

from .models import Car, Student, Cloth
from .forms import CarForm, StudentFormNew, ClothForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required




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
    b = 1
    result=a/b
    # return HttpResponse(result)
    # return HttpResponse('result')

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
    # name = "Rahul"
    # age = 21

    # print("Name:", name)
    # print("Age:", age)

    return HttpResponse("user")


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

def student_form(request):
    form = ExamForm()
    if request.method=="GET":
       return render(request,"student/formstudent.html", {"form": form})

    elif request.method == "POST":
        # Process submitted form here
     
        name = request.POST.get("name")
        # name = request.POST["name"]
        email = request.POST.get("email")
        age = request.POST.get("age")

        print("Name:", name)
        print("Email:", email)
        print("Age", age)
        # return HttpResponse("form submitted")

    #     # print(request.POST)
        return render(request,"student/detailsstudent.html",{ "name": name, "email": email,"age": age})


def form23(request): 
    if request.method == "POST":

        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():

            # print(form.cleaned_data)

            # return HttpResponse("Form submitted")

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            age = form.cleaned_data["age"]
            image = form.cleaned_data["image"] 
            file = form.cleaned_data["file"]

            fs=FileSystemStorage()
            if(image):
                fs.save(image.name, image)

            if(image):
                fs.save(file.name, file)

            return render(
                            request,
                             "student/detailsstudent.html",
                             {
                                 "name": name,
                                 "email": email,
                                 "age": age,
                             }
                         )
             

    else:

        form = StudentFormNew()

    return render(
        request,
        "student/form2student.html",
        {"form": form}
    )

            


#  function to return the student form 
def studentadd(req):
  
    if req.method=="GET":
         return render(req,'student/studentrecord.html')

    if req.method=="POST":
            name=req.POST.get('name')
            email=req.POST.get('email')
            age=req.POST.get('age')
    
            print(name)
            print(email)
            print(age)

            return render(req,'student/showrecord.html',{'n':name, 'e':email, 'a':age})
        

def studentform(request):
    if(request.method=="POST"):
        # simple post method
        # name=request.POST.get('name')
        # age=request.POST.get('age')
        # email= request.POST.get('email')
        # country=request.POST.get('country')

        # fetch the data from django form
        form=RegisterStudent(request.POST, request.FILES)
        if form.is_valid():
            name=form.cleaned_data['name']
            age=form.cleaned_data['age']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            image = form.cleaned_data['image']
            file = form.cleaned_data['file']

            fs=FileSystemStorage()
            # if(image):
            #     fs.save(image.name, image)
                        
            # if(file):
            #     fs.save(file.name, file)

             # Save image
            if image:
            
                image_path = fs.save( 'images/' + image.name,image)
                image_url = fs.url(image_path)
            
            else:
                image_url = None
            
            
            # Save file
            if file:
            
                file_path = fs.save('files/' + file.name,file)
                file_url = fs.url(file_path)
            
            else:
                file_url = None
            

            print(name)
            print(age)
            print(email)
            print(country)
            print(image.name)
            print(file.name)
            print("IMAGE URL:", image_url)
            print("FILE URL:", file_url)

            return render(request, 'student/Registeredstudent.html', {'n':name, 'a':age, 'e':email, 'c':country, 'image_url': image_url,
                     'file_url': file_url})
            # return HttpResponse("Form submitted")
        else:
             # FORM IS INVALID
            print(form.errors)
            return render(request,'student/studentform.html',{'form': form})
    
    else:
            form=RegisterStudent()
            return render(request, 'student/studentform.html',{'form':form})
                    

    

def newform(request):
    if(request.method=="POST"):
        return HttpResponse("Data added successfully")
    else:
        form = Newform()
        return render(request,'student/formnew.html',{'form':form})



# READ: Display all cars
def car_list(request):
    cars = Car.objects.all()
    return render(request, 'student/car_list.html', {'cars': cars})


# CREATE: Add a new car
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()

    return render(request, 'student/car_form.html', {'form': form})

# VIEW: Display complete details of a car
def car_detail(request, id):
    car = get_object_or_404(Car, id=id)

    return render(
        request,
        'student/car_detail.html',
        {'car': car}
    )

# UPDATE: Edit an existing car
def car_update(request, id):
    car = get_object_or_404(Car, id=id)

    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)

        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm(instance=car)

    return render(request, 'student/car_form.html', {'form': form})


# DELETE: Delete an existing car
def car_delete(request, id):
    car = get_object_or_404(Car, id=id)

    if request.method == 'POST':
        car.delete()
        return redirect('car_list')

    return render(request, 'student/car_confirm_delete.html', {'car': car})

def stud_list(request):
    studs = Student.objects.all()
    return render(request, 'student/stud_list.html', {'studs': studs})

def stud_create(request):
    if request.method == 'POST':
            form = StudentFormNew(request.POST)
    
            if form.is_valid():
                form.save()
                return redirect('stud_list')
    else:
        form = StudentFormNew()
    return render(request, 'student/stud_form.html', {'form': form})

def stud_detail(request, id):
    stud = get_object_or_404(Student, id=id)
    print(stud.id)
    return render(request,'student/stud_detail.html',{'stud': stud} )



def stud_update(request, id):
    stud = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        form = StudentFormNew(request.POST, instance=stud)

        if form.is_valid():
            form.save()
            return redirect('stud_list')
    else:
        form = StudentFormNew(instance=stud)

    return render(request, 'student/stud_form.html', {'form': form})

def stud_delete(request, id):
    stud = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        stud.delete()
        return redirect('stud_list')

    return render(request, 'student/stud_confirm_delete.html', {'stud': stud})


def cloth_list(request):
    cloths=Cloth.objects.all()
    return render(request,'student/cloth_list.html',{'cloths':cloths})

def cloth_add(request):
    if(request.method=="POST"):
        form=ClothForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('cloth_list')
    else:
        form=ClothForm()
        return render(request, 'student/cloth_add.html', {'form':form})

def cloth_view(request, id):
    cloth=Cloth.objects.get(id=id)
    return render(request,'student/cloth_details.html', {'cloth':cloth})

def cloth_update(request, id):
    # cloth=Cloth.objects.get(id=id)
    cloth = get_object_or_404(Cloth, id=id)

    if request.method=="POST":
        form=ClothForm(request.POST, instance=cloth)
        if(form.is_valid()):
            form.save()
            return redirect('cloth_list')
    else:   
        form = ClothForm(instance=cloth)
    
        return render(request,'student/cloth_add.html',{'form':form})

def cloth_delete(request, id):
    cloth = get_object_or_404(Cloth, id=id)
    if request.method == 'POST':
            cloth.delete()
            return redirect('cloth_list')
    else:
        return render(request, 'student/cloth_confirm_delete.html', {'cloth': cloth})




def setcookie(request):

    response = render(request, 'student/home.html',{"c":"CookieSet"})

    response.set_cookie('username', 'Rahul')

    return response

def getcookie(request):

    u = request.COOKIES.get('username')

    return render(request, 'student/cookie.html',
                  {'u': u})

def deletecookie(request):

    response = render(request, 'student/home.html',{"c":"cookie deleted"})

    response.delete_cookie('username')

    return response



def setsession(request):

    request.session['username'] = 'Rahul'
    request.session['course'] = 'Django'

    return render(request, 'student/home.html', {"c":"session created"})

def getsession(request):

    username = request.session.get('username')
    course = request.session.get('course')

    return render(request, 'student/session.html', {
        'username': username,
        'course': course
    })

def deletesession(request):

    if 'username' in request.session:
        del request.session['username']

    username = request.session.get('username')
    course = request.session.get('course')

    return render(request, 'student/session.html', {
        'username': username,
        'course': course
    })

def clearsession(request):

    request.session.flush()

    return render(request, 'student/session.html')

def createuser(request):

    user = User.objects.create_user(
        username='Parveen',
        email='parveen@gmail.com',
        password='parveen123'
    )

    return render(request, 'student/home.html', {"c":"user created"})

def showusers(request):

    users = User.objects.all()

    return render(request, 'student/users.html',
                  {'users': users})

def updateuser(request):

    user = User.objects.get(username='Navjot')

    user.email = 'navjot@gmail.com'

    user.save()

    return redirect('alluser')

def deleteuser(request):

    user = User.objects.get(username='Navjot')

    user.delete()

    return redirect('alluser')

@login_required
def dashboard(request):

    return render(request, 'student/dashboard.html')