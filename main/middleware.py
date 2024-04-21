from django.http import HttpResponseForbidden
from django.core.cache import cache


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем IP-адрес пользователя или другую уникальную строку для идентификации
        client_ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_X_REAL_IP')

        # Устанавливаем ключ для кэша, используя IP-адрес и префикс
        cache_key = f'throttle_{client_ip}'

        # Получаем текущее количество запросов из кэша
        request_count = cache.get(cache_key, 0)

        # Проверка на превышение лимита запросов
        if request_count >= 1000:  # Примерно 1000 запросов в час
            return HttpResponseForbidden('Превышен лимит запросов')

        # Увеличиваем счетчик запросов и сохраняем его в кэше
        cache.set(cache_key, request_count + 1, 3600)  # Сохраняем на час

        # Пропускаем запрос дальше по стеку middleware
        response = self.get_response(request)

        return response
