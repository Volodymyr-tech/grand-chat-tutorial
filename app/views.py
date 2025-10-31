from django.middleware.csrf import get_token
import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

import secrets

def get_csrf(request):
    return JsonResponse({}, headers={'X-CSRFToken': get_token(request)})


@require_POST
def login_view(request):
    credentials = json.loads(request.body)
    username = credentials.get('username')
    password = credentials.get('password')

    if not username or not password:
        return JsonResponse({'detail': 'provide username and password'}, status=400)

    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({'detail': 'invalid credentials'}, status=400)

    login(request, user)
    return JsonResponse({'user': {'id': user.pk, 'username': user.username}})


@require_POST
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'must be authenticated'}, status=403)

    logout(request)
    return JsonResponse({})





@require_GET
@login_required
def get_connection_token(request):
    """
    Возвращает временный connection-token для авторизованного пользователя.
    """
    token = secrets.token_urlsafe(32)  # или логика генерации реального токена
    return JsonResponse({'connection_token': token})


@require_GET
@login_required
def get_subscription_token(request):
    """
    Возвращает временный subscription-token для авторизованного пользователя.
    """
    token = secrets.token_urlsafe(32)
    return JsonResponse({'subscription_token': token})
