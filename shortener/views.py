import string
import random
import json
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import URL

def generate_short_url():
    """
    generate a random and unique new short URL.
    """
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choices(characters, k=6))
        if not URL.objects.filter(short_url=short_url).exists():
            break
    return short_url

@csrf_exempt
def create_url(request):
    """
    create a new short URL for the given long URL.
    checks if the request methos is POST, then get the long URL from the request body.
    then generate short URL, and create new object in the DB (SQLite) and return the new URL.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            long_url = data.get('url')
            if not long_url:
                return JsonResponse({'error': 'please insert URL'}, status=400)
            short_url = generate_short_url()
            URL.objects.create(long_url=long_url, short_url=short_url)
            return JsonResponse({'short_url': f'http://localhost:8000/s/{short_url}'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def redirect_url(request, short_url):
    """
    redirect to the long URL with the given short URL and hit counter.
    the function checks if the short URL is exist, if yes it will return it and count ++ the hit_count
    """
    url = get_object_or_404(URL, short_url=short_url)
    url.hit_count += 1
    url.save()
    return redirect(url.long_url)
