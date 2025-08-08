from django.shortcuts import render
import requests
import json
from django.http import JsonResponse

def consultar_cedula(request):
    if request.method == "GET" and not request.GET.get('nacionalidad') and not request.GET.get('cedula'):
        # Renderiza el formulario si no hay parámetros
        return render(request, 'datos.html')

    nacionalidad = request.GET.get('nacionalidad')
    cedula = request.GET.get('cedula')

    if not nacionalidad or not cedula:
        return JsonResponse({'error': "Se requieren los parámetros 'nacionalidad' y 'cedula'."}, status=400)

    url = "https://comunajoven.com.ve/api/cedula"
    params = {'nacionalidad': nacionalidad, 'cedula': cedula}
    headers = {
        'Authorization': 'Bearer faa3dc480981bbfb734839367d2c9367',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = json.loads(response.content.decode('utf-8-sig'))
        return JsonResponse(data, status=200, safe=True)
    except requests.exceptions.HTTPError as e:
        return JsonResponse({'error': f"Error HTTP al consultar la API: {e}"}, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
