from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse

# Create your views here.
def user11(request):
     name="Rabaab"
     id=12
     return render(request,'user/user.html',{"n":name,"i":id})

def htmlres(request):
    print(request)
    print(request.method)
    return HttpResponse("<h1>Hello</h1")

def jsonres(request):
    json={
        "name":"Rabaab",
        "age":3
    }
    return JsonResponse(json)

def userdetails(request):
    name="Rabaab"
    age=3
    roll=5
    print(name,age,roll)
    # return HttpResponse(name,age,roll)
    # return HttpResponse(name+","+str(age)+" "+str(roll))
    return HttpResponse(f'User name is : {name}, having age {age} and rollno {roll}')

def user1(request):
    print(request)
    name=request.GET.get('name')
    age=request.GET.get('age')
    return HttpResponse(f"hello {name} having age {age}")


def user2(request, name,id):
        print(request)
        return HttpResponse(f"Hello, {name} and {id}")

def user90(request,id):
        print(request)
        return HttpResponse(f"Hello,  {id}")

def user91(request,id):
        print(request)
        return HttpResponse(f"Hello,  {id}")

def user92(request,id):
        print(request)
        return HttpResponse(f"Hello,  {id}")

def user6(request, name):
        print(request)
        return HttpResponse(f"Hello,  and {name}")

def user7(request, name):
        print(request)
        return HttpResponse(f"Hello,  and {name}")

def user97(request, name):
        print(request)
        return HttpResponse(f"Hello,  and {name}")

def user34(request, id, name):
        print(request)
        return HttpResponse(f"Hello,   {id} and {name}")


def userlist(request):
      list=["Raman", "Aman", "Nitu", "Parveen"]
      return render(request, 'user/student.html',{'li':list})

     #  l1="<h1>Students Names</h1>"
     #  l1+="<table border='1'>"
     #  l1+="<tr><th>Name</th><tr>"
     #  for i in list:
     #       l1+=f"<tr><td>{i}</td></tr>"
     
     #  l1+="</table>"

     #  return HttpResponse(l1)
      




     # list={"Raman", "Aman", "Nitu", "Parveen"}
     # return HttpResponse(list)
     # return HttpResponse(str(list))
      return HttpResponse(f"{list}")
      return HttpResponse(str(list))

def userdict(request):
     dict={"name":"Rabaab","age":67,"rollno":12}
     values="<h1>Student Table</h1>"
     values+="<table border='1'>"
     values+="<tr>"
     for key in dict.keys():
          values+=f"<th>{key}</th>"
     values+="</tr>"

     values+="<tr>"
     for value in dict.values():
               values+=f"<td>{value}</td>"
     values+="</tr>"

     values+="</table>"

     return HttpResponse(values)







     for key, value in dict.items():
          values+=f"{key}:{value} <br>"

     return HttpResponse(values)

     return HttpResponse(f'{dict['name']}')
     return JsonResponse(dict)
     return HttpResponse(str(dict))


def list1(request):
     list=["Raman", "Aman", "Neetu","Pavneet","Noor"]
     html="<h1>Students Names</h1>"
     html+="<table border='1'>"
     html+="<tr><th>Names</th></tr>"
     for i in list:
          html+=f"<tr><td>{i}</td></tr>"
    
     html+="</table>"
     return HttpResponse(html)
    #  return HttpResponse(list)
     return HttpResponse(str(list))

def set1(request):
     tuple=reverse('tuple')
     set1={"Raman", "Aman", "Neetu","Pavneet","Noor"}
     display="set details <br>"
     display+=f"{set1}"
     display+=f"<br><a href={tuple}>Display Tuple</a>"
     return HttpResponse(display)
     return HttpResponse(str(set1))


def tuple1(request):
     tuple1=("Raman", "Aman", "Neetu","Pavneet","Noor")
    #  return HttpResponse(tuple1)
     return HttpResponse(str(tuple1))

def dict1(request):
     dict1={"name":"Parneet", "age":39}
     result=""
     for key, value in dict1.items():
        result+=f'{key} : {value} <br>'
     return HttpResponse(result)
     return JsonResponse(dict1)
     return HttpResponse(str(dict1))

def list2(request):
   
     list2=[1,"Pavneet", 89]
     html=f"<h1>Sno of student is : {list2[0]}</h1>"
     html+=f"<h2>Sno of student is : {list2[1]}</h2>"
     html+=f"<h3>Sno of student is : {list2[2]}</h3>"
     return HttpResponse(html)

def list1(request):
     first=reverse('first')
     list=["Raman", "Aman", "Neetu","Pavneet","Noor"]
     html="<h1>Students Names</h1>"
     html+="<table border='1'>"
     html+="<tr><th>Names</th></tr>"
     for i in list:
          html+=f"<tr><td>{i}</td></tr>"

    
     html+="</table>"
     html+=f"<a href={first}>List2</a>"
     return HttpResponse(html)

def list3(request):
     students=[ [1,"Pooja",34], 
                [2,"Rohit",89], 
                [3,"Naman",56]   ]
     return render(request,'user/student2.html',{'li':students})
     # html="<h1>Students Details</h1>" 
     # html+="<table border='1'>"
     # html+="<tr><th>Sno</th><th>Name</th><th>Roll no</th></tr>"
     # for student in students:
     #      html+=f"<tr><td>{student[0]}</td><td>{student[1]}</td><td>{student[2]}</td></tr>"
     # html+="</table'>"

     # return HttpResponse(html)


def mylist(request):
    list=[[1,"Raman",23],[2,"Naman",67], [3,"Aman",89], [4, "Neetu",90],[5,"Pooja",20]]
    # return HttpResponse(str(list))
    # return HttpResponse(f'{list}')
    # return HttpResponse(list)

    html="<h1>Students Names</h1>"
    html+="<table border='1'>"
    html+="<tr><th>Sno</th><th>Name</th><th>Roll no</th></tr>"
    for i in range(len(list)):
         html+="<tr>"
         for j in range(len(list[i])):
            html+=f"<td>{list[i][j]}</td>"
         html+="</tr>"
    html+="</table>"
    return HttpResponse(html)


def myset(request):
    set={"Raman","Naman", "Aman","Neetu","Pooja"}
    return HttpResponse(str(set))
    # return HttpResponse(f'{set}')
    # return HttpResponse(set)

def mytuple(request):
    tuple=("Raman","Naman", "Aman","Neetu","Pooja")
    return HttpResponse(str(tuple))
    # return HttpResponse(f'{tuple}')
    # return HttpResponse(tuple)

def mydict(request):
     dict={"name":"Parveen", "roll":23}


     return render(request,'user/student3.html',{'d':dict})
    #  return HttpResponse(dict)
    #  return HttpResponse(str(dict))
    #  return HttpResponse(f"{dict}")
    #  return JsonResponse(dict)
    #  return HttpResponse(f'{dict['name']}')
     result=""
     for key, value in dict.items():
        result+=f'{key} : {value} <br>'
     return HttpResponse(result)


def listdict(request):
     students=[
          {"name":"Raman","age":30,"rollno":12},
          {"name":"Pooja","age":29,"rollno":13},
          {"name":"Rabaab","age":22,"rollno":14}
          ]

     details=""
     details+="  <h1>Student details</h1>"
     details+=" <table border='1'>"
     details+=" <tr><th>Name</th><th>Age</th><th>Roll no</th></tr>"
     for student in students:
          details+=f"<tr><td>{student['name']}</td><td>{student['age']}</td><td>{student['rollno']}</td></tr>"
     details+="  </table>"


     return HttpResponse(details)

def dictlist(request):
     list=[
          {"name":"Aman","age":12,"rollno":2},
          {"name":"Raman","age":18,"rollno":5},
          {"name":"Naman","age":23,"rollno":9}
     ]

     display="<h1>students Details</h1>"
     display+="<table border='1'>"
     display+="<tr><th>Name</th><th>Age</th><th>Roll no</th></tr>"
     for student in list:
          display+=f"<tr><td>{student['name']}</td><td>{student['age']}</td><td>{student['rollno']}</td></tr>"
     display+=" </table>"
     return HttpResponse(display)
     # return HttpResponse("""<h1>students Details</h1>
     # <table border='1'>
     # <tr><th>Name</th><th>Age</th><th>Roll no</th></tr>
     # </table>""")


def monday(request, id,name):
     return HttpResponse(f"Hello {id}")