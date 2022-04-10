from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render
from .forms import UploadFileForm
from musicpy import *
from musicpy.sampler import *
# Imaginary function to handle an uploaded file.
from .process import handle_uploaded_file


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        f = request.FILES['file']
        instr = int(request.POST['instr'])
        if instr >= 0:
            with open('in.mid', 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            if instr <= 127:
                a = read('in.mid')
                a.clear_program_change()
                a.change_instruments([instr])
                write(a, name='out.mid')
                file = open('out.mid', 'rb')
            elif instr == 200:
                inPiece = read("in.mid")
                test = sampler(1)
                test.load(0, 'MS/sf2/8Rock11e.sf2')
                test.export(inPiece,
                        mode='wav',
                        action='export',
                        filename='out.wav',
                        bpm=None,
                        export_args={},
                        show_msg=1)
                file = open('out.wav', 'rb')
        elif instr < 0:
            pass
        response = FileResponse(file)
        return response
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
