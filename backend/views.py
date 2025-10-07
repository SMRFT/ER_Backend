from django.shortcuts import render
from rest_framework.response import Response
from pymongo import MongoClient
from django.http import JsonResponse
import os
from dotenv import load_dotenv
from bson.json_util import dumps
from datetime import datetime
from .models import ERRegister,ERBilling
from .serializers import ERRegisterSerializer,ERBillingSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from datetime import date
from rest_framework import status
from django.utils.dateparse import parse_date
from pyauth.auth import HasRolePermission
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ERRegister, ERBilling
from .serializers import ERRegisterSerializer, ERBillingSerializer
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.http import HttpResponse
import pandas as pd



@csrf_exempt
@api_view(['POST'])
@permission_classes([HasRolePermission])
def erregister_patient(request):
    today = date.today()
    year = today.year

    # Determine financial year start
    if today.month <= 3:
        start_year = year - 1
    else:
        start_year = year

    prefix = f"ER0{str(start_year)[-2:]}"
    existing_ers = ERRegister.objects.filter(erNumber__startswith=prefix).order_by('-erNumber')

    if existing_ers.exists():
        try:
            last_number = int(existing_ers[0].erNumber.split("/")[-1])
        except (ValueError, IndexError):
            last_number = 0
        next_number = last_number + 1
    else:
        next_number = 1

    er_number = f"{prefix}/{str(next_number).zfill(6)}"

    data = request.data.copy()
    data['erNumber'] = er_number

    employee_id = data.get('auth-user-id')
    print("employee_id", employee_id)


    serializer = ERRegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save(
            created_date=datetime.now(),
            lastmodified_date=datetime.now(),
            created_by=employee_id,
            lastmodified_by=employee_id
        )

        return Response({
            "message": "Patient Registered Successfully",
            "erNumber": er_number
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
@permission_classes([HasRolePermission])
def get_patient_by_er_number(request):
    er_number = request.GET.get("erNumber")
    if not er_number:
        return Response({"error": "erNumber is required"}, status=400)

    try:
        patient = ERRegister.objects.get(erNumber=er_number)
        serializer = ERRegisterSerializer(patient)
        return Response(serializer.data, status=200)
    except ERRegister.DoesNotExist:
        return Response({"error": "Patient not found"}, status=404)



@api_view(['POST', 'GET'])
@permission_classes([HasRolePermission])
def get_doctor_list(request):
    
    mongo_url = os.getenv("GLOBAL_DB_HOST")
    client = MongoClient(mongo_url)
    db = client["ER"]
    collection = db["er_doctors"]

    doctors = list(collection.find({"is_active": True}))  # Filter only active doctors
    return JsonResponse(dumps(doctors), safe=False)


@api_view(['GET'])
@permission_classes([HasRolePermission])
def get_procedure_list(request):
    mongo_url = os.getenv("GLOBAL_DB_HOST")
    client = MongoClient(mongo_url)
    db = client["ER"]
    collection = db["er_procedurelist"]

    procedurelist = list(collection.find({}))  # Fetch all records
    return JsonResponse(dumps(procedurelist), safe=False)


@api_view(['GET'])
@permission_classes([HasRolePermission])
def get_ct_list(request):
    mongo_url = os.getenv("GLOBAL_DB_HOST")
    client = MongoClient(mongo_url)
    db = client["ER"]
    collection = db["er_ctlist"]

    ctlist = list(collection.find({}))  # Fetch all records
    return JsonResponse(dumps(ctlist), safe=False)


@api_view(['GET'])
@permission_classes([HasRolePermission])
def get_usg_list(request):
    mongo_url = os.getenv("GLOBAL_DB_HOST")
    client = MongoClient(mongo_url)
    db = client["ER"]
    collection = db["er_usglist"]

    usglist = list(collection.find({}))  # Fetch all records
    return JsonResponse(dumps(usglist), safe=False)


@api_view(['GET'])
@permission_classes([HasRolePermission])
def get_mri_list(request):
    mongo_url = os.getenv("GLOBAL_DB_HOST")
    client = MongoClient(mongo_url)
    db = client["ER"]
    collection = db["er_mrilist"]

    mrilist = list(collection.find({}))  # Fetch all records
    return JsonResponse(dumps(mrilist), safe=False)


@api_view(['GET'])
@permission_classes([HasRolePermission])
def get_ct_list(request):
    mongo_url = os.getenv("GLOBAL_DB_HOST")
    client = MongoClient(mongo_url)
    db = client["ER"]
    collection = db["er_ctlist"]

    ctlist = list(collection.find({}))  # Fetch all records
    return JsonResponse(dumps(ctlist), safe=False)


@api_view(['GET'])
@permission_classes([HasRolePermission])
def get_next_bill_number(request):
    current_year = datetime.now().year % 100
    next_year = (datetime.now().year + 1) % 100
    prefix = f"{current_year:02d}{next_year:02d}"

    # Get latest billNumber with this prefix
    latest_patient = (
        ERBilling.objects.filter(billNumber__startswith=prefix)
        .order_by('-billNumber')
        .first()
    )

    if latest_patient:
        try:
            last_number = int(latest_patient.billNumber.split('/')[-1])
        except (IndexError, ValueError):
            last_number = 0
    else:
        last_number = 0

    next_number = last_number + 1
    next_bill_number = f"{prefix}/{next_number:02d}"
    return Response({'billNumber': next_bill_number})


from datetime import datetime, timedelta
from django.utils.timezone import make_aware

@api_view(["GET"])
@permission_classes([HasRolePermission])
def get_er_patients_by_date(request):
    # Get date string from query parameters
    date_str = request.GET.get("date")

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return Response({"error": "Invalid or missing date. Format should be YYYY-MM-DD"}, status=400)

    start = make_aware(datetime.combine(selected_date, datetime.min.time()))
    end = make_aware(datetime.combine(selected_date, datetime.max.time()))

    patients = ERRegister.objects.filter(created_date__range=(start, end))
    serializer = ERRegisterSerializer(patients, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([HasRolePermission])
def er_billing(request):
    # Step 1: Generate bill number prefix as "2526"
    current_year = datetime.now().year % 100      # e.g., 2025 → 25
    next_year = (datetime.now().year + 1) % 100   # e.g., 2026 → 26
    prefix = f"{current_year:02d}{next_year:02d}" # e.g., "2526"

    # Step 2: Count existing records with that prefix
    existing_count = ERBilling.objects.filter(billNumber__startswith=prefix).count()
    next_number = existing_count + 1
    bill_number = f"{prefix}/{next_number:02d}"   # e.g., "2526/06"

    # ✅ Fix: copy request.data first
    data = request.data.copy()
    employee_id = data.get('auth-user-id')   # now safe to access

    # Step 3: Add metadata
    data['billNumber'] = bill_number
    data['created_by'] = employee_id
    data['lastmodified_by'] = employee_id
    data['created_date'] = datetime.now()
    data['lastmodified_date'] = datetime.now()

    serializer = ERBillingSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)

    

@api_view(['GET'])
@permission_classes([HasRolePermission])
def search_er_billing(request):
    er_number = request.GET.get('erNumber')
    if not er_number:
        return Response({"error": "erNumber parameter is required."}, status=400)

    billing_records = ERBilling.objects.filter(erNumber=er_number)
    if billing_records.exists():
        serializer = ERBillingSerializer(billing_records, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response({"message": "No billing record found for this ER number."}, status=404)



@api_view(['GET'])
@permission_classes([HasRolePermission])
def get_patients_by_date(request):
    bill_date_str = request.GET.get('billDate')
    if not bill_date_str:
        return Response({"error": "billDate parameter is required"}, status=400)

    try:
        bill_date = parse_date(bill_date_str)
        if not bill_date:
            return Response({"error": "Invalid billDate format"}, status=400)

        patients = ERBilling.objects.filter(billDate=bill_date)
        serializer = ERBillingSerializer(patients, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(["GET", "PATCH"])
@permission_classes([HasRolePermission])
def er_register_view(request):
    if request.method == "GET":
        date_str = request.GET.get("date")
        try:
            if date_str:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                date = datetime.now().date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        start = make_aware(datetime.combine(date, datetime.min.time()))
        end = make_aware(datetime.combine(date, datetime.max.time()))

        records = ERRegister.objects.filter(created_date__range=(start, end))
        serializer = ERRegisterSerializer(records, many=True)
        return Response(serializer.data)

    elif request.method == "PATCH":
        record_id = request.data.get("id")
        try:
            instance = ERRegister.objects.get(id=record_id)
        except ERRegister.DoesNotExist:
            return Response({"error": "Record not found"}, status=404)

        serializer = ERRegisterSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    





@api_view(['GET'])
@permission_classes([HasRolePermission])
def fetch_er_patient_bills(request):
    selected_date = request.GET.get('date')
    try:
        if selected_date:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        else:
            selected_date = datetime.today().date()

        patients = ERBilling.objects.filter(billDate=selected_date)
        serializer = ERBillingSerializer(patients, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    



@api_view(["GET"])
@permission_classes([HasRolePermission])
def get_er_reports(request):
    from datetime import datetime
    from django.utils.timezone import make_aware
    from django.contrib.auth.hashers import check_password


    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
        start = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
        end = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
        end = end.replace(hour=23, minute=59, second=59)
    else:
        # Default to today
        today = datetime.today().date()
        start = make_aware(datetime.combine(today, datetime.min.time()))
        end = make_aware(datetime.combine(today, datetime.max.time()))

    register_qs = ERRegister.objects.filter(created_date__range=(start, end))
    billing_qs = ERBilling.objects.filter(created_date__range=(start, end))

    return Response({
        "register": ERRegisterSerializer(register_qs, many=True).data,
        "billing": ERBillingSerializer(billing_qs, many=True).data,
    })




# views.py
import os
from pymongo import MongoClient
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Connect to MongoDB
mongo_url = os.getenv("GLOBAL_DB_HOST")
client = MongoClient(mongo_url)
db = client["ER"]
collection = db["er_billtype"]

@api_view(["GET"])
def billtype(request):
    try:
        # Fetch all documents from collection
        billtypes_cursor = collection.find({})

        # Convert cursor to list of dicts and convert _id to string
        billtypes = []
        for item in billtypes_cursor:
            item["_id"] = str(item["_id"])
            billtypes.append(item)

        return Response({"status": "success", "data": billtypes})

    except Exception as e:
        return Response({"status": "error", "message": str(e)})
