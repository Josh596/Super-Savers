from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required,user_passes_test
from django.forms import inlineformset_factory
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'ecom/index.html')