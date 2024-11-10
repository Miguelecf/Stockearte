from django.shortcuts import render

def index(request):
    response = None
    if request.method == "POST":
        # Procesamiento del CSV
        # Aquí agregas el código para manejar el archivo y obtener la respuesta
        response = "Respuesta del servidor"
    return render(request, 'csv_mass_import.html', {'response': response})
