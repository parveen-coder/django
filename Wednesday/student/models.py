from django.db import models

# Create your models here.

class Student(models.Model):
    roll_no=models.IntegerField()
    name=models.CharField(max_length=100)
    marks=models.FloatField()

    def __str__(self):
        return self.name


class  User(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()
    
    def __str__(self):
        return self.name


class Car(models.Model):
    brand=models.CharField()
    price=models.IntegerField()
    color=models.CharField()
    model=models.IntegerField()

    def __str__(self):
        return self.brand


class Cloth(models.Model):
    name=models.CharField()
    color=models.CharField()
    price=models.IntegerField()

    def __str__(self):
        return self.name

class Stud(models.Model):
    roll_no=models.IntegerField()
    name=models.CharField(max_length=100)
    marks=models.FloatField()

    def __str__(self):
        return self.name

class Department(models.Model):
    dept_name = models.CharField(max_length=100)

    def __str__(self):
        return self.dept_name


class Employee(models.Model):
    emp_name = models.CharField(max_length=100)
    email = models.EmailField()
    dept = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.emp_name