from django.db import models

# Create your models here.

class college_details(models.Model):
    Eamcet_Code=models.CharField(max_length=6,primary_key=True,blank=True)
    College_Name=models.CharField(max_length=100,blank=True)
    District=models.CharField(max_length=20,blank=True)
    Place=models.CharField(max_length=30,blank=True)
    Contact_No=models.CharField(max_length=10,null=True)
    Website=models.URLField(null=True)
    College_Type=models.CharField(max_length=5,null=True,blank=True)
    Coed=models.CharField(max_length=5,null=True,blank=True)
    Size=models.CharField(max_length=5,null=True,blank=True)
    Academics_Quality=models.CharField(max_length=5,null=True,blank=True)
    Placement_Rating=models.CharField(max_length=5,null=True,blank=True)
    Sports=models.CharField(max_length=5,null=True,blank=True)
    Hostel_B=models.CharField(max_length=5,null=True,blank=True)
    Hostel_G=models.CharField(max_length=5,null=True,blank=True)
    Bus_Facility=models.CharField(max_length=5,null=True,blank=True)
    Clubs=models.CharField(max_length=5,null=True,blank=True)
    Medical_Care=models.CharField(max_length=5,null=True,blank=True)
    NIRF=models.CharField(max_length=5,null=True,blank=True)
    NAAC=models.CharField(max_length=4,null=True)
    NBA=models.CharField(max_length=5,null=True,blank=True)


class cutoff(models.Model):
    Eamcet_Code=models.CharField(max_length=6,null=True)
    Course_Code=models.CharField(max_length=3,blank=True)
    Region=models.CharField(max_length=3,blank=True)
    District=models.CharField(max_length=20,blank=True)
    Place=models.CharField(max_length=30,blank=True)
    ocb=models.CharField(max_length=10,null=True,blank=True)
    ocg=models.CharField(max_length=10,null=True,blank=True)
    scb=models.CharField(max_length=10,null=True,blank=True)
    scg=models.CharField(max_length=10,null=True,blank=True)
    stb=models.CharField(max_length=10,null=True,blank=True)
    stg=models.CharField(max_length=10,null=True,blank=True)
    bcab=models.CharField(max_length=10,null=True,blank=True)
    bcag=models.CharField(max_length=10,null=True,blank=True)
    bcbb=models.CharField(max_length=10,null=True,blank=True)
    bcbg=models.CharField(max_length=10,null=True,blank=True)
    bccb=models.CharField(max_length=10,null=True,blank=True)
    bccg=models.CharField(max_length=10,null=True,blank=True)
    bcdb=models.CharField(max_length=10,null=True,blank=True)
    bcdg=models.CharField(max_length=10,null=True,blank=True)
    bcdb=models.CharField(max_length=10,null=True,blank=True)
    bcdg=models.CharField(max_length=10,null=True,blank=True)
    bceb=models.CharField(max_length=10,null=True,blank=True)
    bceg=models.CharField(max_length=10,null=True,blank=True)