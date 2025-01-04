from django.shortcuts import render

# Create your views here.



def add_amazon_store(request):
    return render(request,'amazon_store_form.html')