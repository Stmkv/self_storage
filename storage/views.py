from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from storage.models import AboutUs, Warehouse

from .forms import DateRangeForm


# Create your views here.
def boxes(request):
    warehouses = Warehouse.objects.prefetch_related("boxes").all()
    for warehouse in warehouses:
        warehouse.free_boxes = warehouse.boxes.filter(status="свободен").count()
    context = {
        "user_auth": request.user.is_authenticated,
        "warehouses": warehouses,
        "boxes": boxes,
        "warehouse": warehouse,
    }
    return render(request, "boxes.html", context)


def faq(request):
    about_us_data = AboutUs.objects.prefetch_related("texts").all()
    context = {
        "user_auth": request.user.is_authenticated,
        "about_us_data": about_us_data,
    }
    return render(request, "faq.html", context)


def index(request):
    context = {
        "user_auth": request.user.is_authenticated,
    }
    if request.user.is_authenticated:
        context["user"] = request.user
    return render(request, "index.html", context)


def my_rent(request):
    return render(request, "my-rent.html")


def my_rent_empty(request):
    return render(request, "my-rent-empty.html")


def order(request):
    form = DateRangeForm()
    return render(request, "order.html", {"form": form})


def get_boxes_by_warehouse(request, warehouse_id):
    print(warehouse_id)
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    boxes = warehouse.boxes.filter(status="свободен")

    data = [
        {
            "id": box.id,
            "number": box.number,
            "box_type": box.get_box_type_display(),
            "price_per_month": box.price_per_month,
            "status": box.get_status_display(),
        }
        for box in boxes
    ]

    return JsonResponse({"warehouse": warehouse.address, "boxes": data})
