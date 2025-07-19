from django.db import models


class ERRegister(models.Model):  # ✅ FIXED
    erNumber = models.CharField(max_length=100, blank=True)
    patientname = models.CharField(max_length=255)
    dob = models.CharField(max_length=100, blank=True)
    age = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    permanentAddress = models.TextField(blank=True, null=True)
    aadhaarNumber= models.CharField(max_length=100,blank=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobilePhone = models.CharField(max_length=20, blank=True)
    alternativeNumber = models.CharField(max_length=20, blank=True, null=True)
    bloodGroup = models.CharField(max_length=5, blank=True, null=True)
    guardianName = models.CharField(max_length=255, blank=True, null=True)
    referredBy = models.CharField(max_length=255, blank=True, null=True)
    doctorName = models.CharField(max_length=255, blank=True, null=True)
    doctorFees = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    lastmodified_by = models.CharField(max_length=100, blank=True, null=True)
    lastmodified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

#ER form
class ERBilling(models.Model):
    erNumber = models.CharField(max_length=100, blank=True)
    patientname = models.CharField(max_length=200,blank=True)
    billNumber = models.CharField(max_length=100)
    doctorName = models.CharField(max_length=200,blank=True)
    billDate = models.DateField()
    billType = models.JSONField(blank=True, null=True)  
    age =  models.CharField(max_length=100,blank=True)
    gender = models.CharField(max_length=10,blank=True)
    dob =  models.CharField(max_length=100,blank=True)
    permanentAddress =  models.CharField(max_length=100,blank=True)
    mobilePhone = models.CharField(max_length=20,blank=True)
    totalAmount=  models.CharField(max_length=100,blank=True)
    discount=  models.CharField(max_length=100,blank=True)
    discountedAmount=  models.CharField(max_length=100,blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.billNumber
    