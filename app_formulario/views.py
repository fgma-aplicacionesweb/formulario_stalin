from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator

from .models import PersonaRegistro, Estado, Municipio, Parroquia, Universidad, Direccion


def consultar_cedula(request):
    if request.method == "GET" and not request.GET.get('nacionalidad') and not request.GET.get('cedula'):
        estados = Estado.objects.all().order_by('nom_est')
        return render(request, 'datos.html', {'estados': estados})

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


@csrf_exempt
@require_POST
def guardar_datos(request):
    try:
        cedula = request.POST.get('cedula')

        if PersonaRegistro.objects.filter(cedula=cedula).exists():
            return JsonResponse({
                'success': False,
                'message': 'Esta cédula ya está registrada en el sistema',
                'duplicated': True
            })

        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        nacimiento = request.POST.get('nacimiento')
        lugar_nacimiento = request.POST.get('lugar_nacimiento')

        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')

        tipo_beca = request.POST.get('tipo_beca')
        carrera_cursada = request.POST.get('carrera_cursada')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        fecha_egreso = request.POST.get('fecha_egreso')
        titularidad = request.POST.get('titularidad')
        idiomas = request.POST.get('idiomas')
        ocupacion_actual = request.POST.get('ocupacion_actual')

        becario_internacional_en_venezuela = bool(request.POST.get('becario_internacional_en_venezuela'))
        becario_venezolano_en_venezuela = bool(request.POST.get('becario_venezolano_en_venezuela'))
        becario_venezolano_en_exterior = bool(request.POST.get('becario_venezolano_en_exterior'))

        estado_id = request.POST.get('estado')
        municipio_id = request.POST.get('municipio')
        parroquia_id = request.POST.get('parroquia')
        universidad_id = request.POST.get('universidad')

        estado = Estado.objects.get(id_est=estado_id) if estado_id else None
        municipio = Municipio.objects.get(id_mun=municipio_id) if municipio_id else None
        parroquia = Parroquia.objects.get(id_par=parroquia_id) if parroquia_id else None
        universidad = Universidad.objects.get(id_uni=universidad_id) if universidad_id else None

        if not all([cedula, nombre, apellido, telefono, email, direccion]):
            return JsonResponse({'success': False, 'message': 'Todos los campos obligatorios deben completarse'})

        registro = PersonaRegistro(
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=nacimiento or None,
            lugar_nacimiento=lugar_nacimiento,
            telefono=telefono,
            email=email,
            direccion=direccion,
            tipo_beca=tipo_beca,
            carrera_cursada=carrera_cursada,
            fecha_ingreso=fecha_ingreso or None,
            fecha_egreso=fecha_egreso or None,
            titularidad=titularidad,
            idiomas=idiomas,
            ocupacion_actual=ocupacion_actual,
            becario_internacional_en_venezuela=becario_internacional_en_venezuela,
            becario_venezolano_en_venezuela=becario_venezolano_en_venezuela,
            becario_venezolano_en_exterior=becario_venezolano_en_exterior,
            estado=estado,
            municipio=municipio,
            parroquia=parroquia,
            universidad=universidad,
            usuario_registro=request.user if request.user.is_authenticated else None
        )
        registro.save()

        return JsonResponse({'success': True, 'message': 'Datos guardados exitosamente'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})



# Endpoints AJAX
def get_municipios(request, estado_id):
    municipios = list(Municipio.objects.filter(id_est=estado_id).values('id_mun', 'nom_mun'))
    return JsonResponse(municipios, safe=False)

def get_parroquias(request, municipio_id):
    parroquias = list(Parroquia.objects.filter(id_mun=municipio_id).values('id_par', 'nom_par'))
    return JsonResponse(parroquias, safe=False)

def get_universidades(request, estado_id):
    universidades = list(Universidad.objects.filter(id_est=estado_id).values('id_uni', 'nomb_uni'))
    return JsonResponse(universidades, safe=False)

def get_direccion_universidad(request, universidad_id):
    try:
        direccion = Direccion.objects.filter(id_uni=universidad_id).first()
        if direccion:
            return JsonResponse({'id_dir': direccion.id_dir, 'nom_dir': direccion.nom_dir})
        else:
            return JsonResponse({'id_dir': None, 'nom_dir': ''})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def lista_personas(request):
    personas = PersonaRegistro.objects.select_related(
        'estado', 'municipio', 'parroquia', 'universidad'
    ).all().order_by('-fecha_registro')
    return render(request, 'lista_personas.html', {'personas': personas})

def lista_personas_ajax(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    queryset = PersonaRegistro.objects.select_related(
        'estado', 'municipio', 'parroquia', 'universidad'
    )

    if search_value:
        queryset = queryset.filter(
            Q(cedula__icontains=search_value) |
            Q(nombre__icontains=search_value) |
            Q(apellido__icontains=search_value) |
            Q(estado__nom_est__icontains=search_value) |
            Q(municipio__nom_mun__icontains=search_value) |
            Q(parroquia__nom_par__icontains=search_value) |
            Q(universidad__nomb_uni__icontains=search_value) |
            Q(tipo_beca__icontains=search_value) |
            Q(lugar_nacimiento__icontains=search_value) |
            Q(carrera_cursada__icontains=search_value) |
            Q(titularidad__icontains=search_value) |
            Q(idiomas__icontains=search_value) |
            Q(ocupacion_actual__icontains=search_value)
        )

    total_registros = queryset.count()
    queryset = queryset.order_by('-fecha_registro')[start:start + length]

    data = []
    for p in queryset:
        direccion_uni = ''
        if p.universidad:
            direccion = Direccion.objects.filter(id_uni=p.universidad.id_uni).first()
            if direccion:
                direccion_uni = direccion.nom_dir

        data.append([
            p.cedula,
            p.nombre,
            p.apellido,
            p.estado.nom_est if p.estado else '',
            p.municipio.nom_mun if p.municipio else '',
            p.parroquia.nom_par if p.parroquia else '',
            p.universidad.nomb_uni if p.universidad else '',
            direccion_uni,
            p.tipo_beca or '',
            p.lugar_nacimiento or '',
            p.carrera_cursada or '',
            p.fecha_ingreso.strftime('%d/%m/%Y') if p.fecha_ingreso else '',
            p.fecha_egreso.strftime('%d/%m/%Y') if p.fecha_egreso else '',
            p.titularidad or '',
            p.idiomas or '',
            p.ocupacion_actual or '',
            "Sí" if p.becario_internacional_en_venezuela else "No",
            "Sí" if p.becario_venezolano_en_venezuela else "No",
            "Sí" if p.becario_venezolano_en_exterior else "No",
            p.fecha_registro.strftime('%d/%m/%Y %H:%M')
        ])

    return JsonResponse({
        'draw': draw,
        'recordsTotal': total_registros,
        'recordsFiltered': total_registros,
        'data': data
    })
