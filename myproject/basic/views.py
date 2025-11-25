from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import StudentNew

# Create your views here.

def sample(request):
    return HttpResponse("hello akhiran")


def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status":"ok","db":"connected"})
    except Exception as e:
        return JsonResponse({"status":"error","db":str(e)})



@csrf_exempt
def addStudent(request):
    print(request.method)
    if request.method=="POST":
        data=json.loads(request.body)
        student=StudentNew.objects.create(
            name=data.get('name'),
            age=data.get('age'),
            email=data.get('email')
            )
        return JsonResponse({"status":"success","id":student.id},status=200)
    


    elif request.method=="GET":
        result=list(StudentNew.objects.values())
        print(result)
        return JsonResponse({"status":"ok","data":result},status=200)
    

    elif request.method=="PUT":
         data=json.loads(request.body)
         ref_id=data.get("id")      #getting id
         new_email=data.get("email")    #getting email
         existing=StudentNew.objects.get(id=ref_id) #fetched the object as per the id
        #  print(existing)
         existing.email=new_email   #updating with new email
         existing.save()
         updated_data=StudentNew.objects.filter(id=ref_id).values().first()

         return JsonResponse({"status":"data updated successfully","updated_data":updated_data},status=200)
    


    elif request.method=="DELETE":
        data=json.loads(request.body)
        ref_id=data.get("id")             #getting id
        get_deleted=StudentNew.objects.filter(id=ref_id).values().first()
        to_be_delete=StudentNew.objects.get(id=ref_id)
        to_be_delete.delete()
        return JsonResponse({"status":"success","message":"student record deleted successfully","deleted_data":get_deleted},status=200)
    return JsonResponse({"error":"use post method"},status=400)