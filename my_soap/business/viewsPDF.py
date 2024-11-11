from django.shortcuts import render
from django.http import HttpResponse
from .pdf_service import generate_pdf

def index(request):
    response = None
    if request.method == "POST":
        title = request.POST.get('title', 'Reporte de Productos')

        # Generar el PDF con los datos obtenidos
        pdf_file = generate_pdf(title)

        if pdf_file:
            # Crear respuesta HTTP con el archivo PDF generado
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="reporte_productos.pdf"'
        else:
            response = HttpResponse("Error al generar el PDF.", status=500)

    return render(request, 'pdf.html', {'response': response})
