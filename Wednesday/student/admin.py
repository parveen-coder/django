from django.contrib import admin
from .models import  Car, User, Cloth, Department, Employee

# Register your models here.
# admin.site.register(Student)
admin.site.register(Car)
admin.site.register(User)
admin.site.register(Cloth)
admin.site.register(Department)
admin.site.register(Employee)



# @admin.register(Department)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'dept_name')
#     search_fields = ('dept_name',)


# @admin.register(Employee)
# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'emp_name', 'email', 'dept')
#     search_fields = ('emp_name', 'email')
#     list_filter = ('dept',)
