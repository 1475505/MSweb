from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render
from .forms import UploadFileForm
from musicpy import *
# Imaginary function to handle an uploaded file.
from .process import handle_uploaded_file


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        f = request.FILES['file']
        with open('in.mid', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        instr = int(request.POST['instr'])
        a = read('in.mid')
        a.clear_program_change()
        a.change_instruments([instr])
        write(a, name='out.mid')
        file = open('out.mid', 'rb')
        response = FileResponse(file)
        return response
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
