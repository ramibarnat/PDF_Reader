from django.http import HttpResponse, JsonResponse
from . import pdf_process
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['pdf_file']
        if uploaded_file.size < 7000000:
            processed_data = pdf_process.process_pdf(uploaded_file)
            return HttpResponse('post')
        else:
            return HttpResponse('file too large')
    else:
        return HttpResponse('not post')