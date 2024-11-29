import requests
from django.http import JsonResponse

# Configure the Flask API URL (PC 1)
FLASK_API_URL = 'http://192.168.1.15:5000/extract_text'

def extract_text_via_flask(request):
    if request.method == 'POST' and request.FILES.get('file'):
        pdf_file = request.FILES['file']
        files = {'file': pdf_file}

        try:
            # Forward the request to the Flask server
            response = requests.post(FLASK_API_URL, files=files)
            return JsonResponse(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Connection error', 'details': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
