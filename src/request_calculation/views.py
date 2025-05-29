from django.core.validators import validate_email
from django.forms import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import RequestCalculation


@require_POST
def get_request_email(request):
    email = request.POST.get("EMAIL1")
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {"success": False, "errors": {"email": ["Неверный формат"]}}, status=400
        )
    RequestCalculation.objects.create(email=email)
    return JsonResponse({"success": True, "errors": {"email": ["Заявка отправлена"]}})
