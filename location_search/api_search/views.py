import requests
from django.shortcuts import render
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt


def format_location(location):
    loc = location[0]
    """Helper function to format location strings."""
    if not isinstance(loc, str):
        return "Invalid location format"

    parts = loc.split('/')
    if len(parts) < 2:
        return loc  # Return as-is if not enough parts

    place = parts[-1].strip()  # Last part (e.g., "Jaipur (Rv)")
    parent_location = parts[-2].strip()  # Second last part (e.g., "Mayabunder")

    # Return the formatted string: "Jaipur (Mayabunder)"
    return f"{place} ({parent_location})"


# @csrf_exempt
def search_view(request):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        keywords = request.GET.get('keywords', '')
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 100))

        if not keywords:
            return JsonResponse({"error": "No keywords provided"}, status=400)

        try:
            # Make the request to the Flask API
            response = requests.get(f'http://192.168.1.13:5000/search', params={
                'keywords': keywords,
                'page': page,
                'limit': limit,
            })

            if response.status_code == 200:
                data = response.json()  # Fetch the raw data from Flask API
                # print(data['data'][0])
                # Format the locations before sending to frontend
                formatted_data = [format_location(item) for item in data['data']]
                # print(formatted_data)
                # print(data['has_more'])
                return JsonResponse({'data': formatted_data, 'has_more': data['has_more']}, safe=False)

            return JsonResponse({"error": "Error fetching data from Flask API"}, status=500)

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return JsonResponse({"error": "Failed to connect to Flask API"}, status=500)

    return render(request, 'api_search/search.html')
