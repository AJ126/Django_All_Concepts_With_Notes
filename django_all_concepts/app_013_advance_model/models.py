from django.db import models

# Create your models here.
# Abstract base class 
# if a few fields are common then, we can separate common fields in base model 
# and abstract this class into child classes
class base(models.Model):
    name = models.CharField(max_length=100)

class data(base):
    address = models.CharField(max_length=100)

class Userdata(base):
    contact = models.IntegerField()

# Multi Table Inheritance
class parenttable(models.Model):
    name = models.CharField(max_length=100)

class childtable(parenttable):
    address = models.CharField(max_length=100)

# multi level inheritance
class parent(models.Model):
    name = models.CharField(max_length=100)

class child(parent):
    info = models.CharField(max_length=100)

class son(child):
    details = models.CharField(max_length=100)

# Multiple Inheritance
class detailstest(models.Model):
    detail_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)

class info(models.Model):
    info_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100)

class test(detailstest, info):
    name = models.CharField(max_length=100)

# book manager
class bookManager(models.Manager):
    def showAllBooks(self):
        return self.all()

    def cheapBook(self):
        return self.filter(price__lt = 100)

    def expensiveBook(self):
        return self.filter(price__gt = 250)

class books(models.Model):
    book = models.CharField(max_length=100)
    price = models.IntegerField()

    # objects = models.Manager() # default manager
    objects = bookManager() # replaces default manager with custom manager
    custom_manager = bookManager() # custom manager 
    #(if you want to keep default manager then you can create custom manager with different name)


# proxy model
class proxyBook(books):
    class Meta:
        proxy = True
        ordering = ['price']