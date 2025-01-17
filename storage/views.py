from django.shortcuts import render

# Create your views here.
def boxes(request):
    return render(request, 'boxes.html')


def faq(request):
    return render(request, 'faq.html')

def index(request):
    return render(request, 'index.html')

def my_rent(request):
    return render(request, 'my-rent.html')

def my_rent_empty(request):
    return render(request, 'my-rent-empty.html')