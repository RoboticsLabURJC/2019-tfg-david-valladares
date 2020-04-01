from django.shortcuts import render

# Create your views here.

def upApp(request):
    return render(request, 'UploadArduino/index.html')