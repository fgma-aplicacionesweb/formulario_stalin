from django import template
from ..models import Direccion

register = template.Library()

@register.filter
def direccion_universidad(universidad_id):
    direccion = Direccion.objects.filter(id_uni=universidad_id).first()
    return direccion.nom_dir if direccion else ''
