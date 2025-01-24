from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from storage.models import AboutUs, Box, Order, Warehouse
from users.models import CustomUser

from .forms import DateRangeForm


# Create your views here.
def boxes(request):
    warehouses = Warehouse.objects.prefetch_related("boxes").all()
    for warehouse in warehouses:
        warehouse.free_boxes = warehouse.boxes.filter(status="свободен").count()
    box_categories = {
        "all": Box.objects.all(),
        "to3": Box.objects.filter(area__lte=3),
        "to10": Box.objects.filter(area__gt=3, area__lte=10),
        "from10": Box.objects.filter(area__gt=10),
    }

    context = {
        "user_auth": request.user.is_authenticated,
        "warehouses": warehouses,
        "box_categories": box_categories,
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
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            address = form.cleaned_data["address"]
            day_rent = (end_date - start_date).days

            one_day_price = float(request.GET.get("price")) / 30
            price_for_user = round(one_day_price * day_rent, 0)

            box_id = request.GET.get("box_id")
            box = Box.objects.get(pk=box_id)
            if request.user.is_authenticated:
                user = CustomUser.objects.get(email=request.user.email)
                order, created = Order.objects.get_or_create(
                    start_storage=start_date,
                    end_storage=end_date,
                    client=user,
                    box=box,
                    address=address,
                    price=price_for_user,
                )
                box.status = "занят"
                box.save()
                return redirect(
                    reverse("users:my-rent"),
                )

    form = DateRangeForm()
    return render(request, "order.html", {"form": form})


def get_boxes_by_warehouse(request, warehouse_id):
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
