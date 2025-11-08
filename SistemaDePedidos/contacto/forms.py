from django import forms

CATEGORIAS = [
    ("mantenimiento", "Mantenimiento"),
    ("actualizacion", "Actualización"),
    ("consulta", "Consulta"),
    ("soporte", "Soporte técnico"),
    ("armado", "Armado de PC"),
    ("otro", "Otro"),
]
class FormularioContacto(forms.Form):
    nombre=forms.CharField(label="Nombre", required=True)
    email=forms.CharField(label="Email", required=True)
    categoria = forms.ChoiceField(choices=CATEGORIAS, label="Categoría", required=True)
    contenido=forms.CharField(label="Contenido", widget=forms.Textarea)