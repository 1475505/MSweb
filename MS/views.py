from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render
from .forms import UploadFileForm
from musicpy import *
from musicpy.sampler import *
# Imaginary function to handle an uploaded file.
from .process import handle_uploaded_file
import matplotlib as plt


def Visualization(filepath):
    a = read(filepath)
    notes_set = {}  # 从C0到B8
    notes_list = []
    b = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', "A#", 'B']
    c = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for i in c:
        for j in b:
            z = j + str(i)
            notes_set[z] = 0
            notes_list.append(z)
    a1_notes = [1]
    for i in range(0, a.track_number):
        a1_notes = a1_notes + a[i].content.notes
        a1_notes = list(one for one in a1_notes if str(one) in notes_list)
    y = []
    m = len(a1_notes)
    for i in range(0, m):
        y.append(a1_notes[i].name + str(a1_notes[i].num))
    for i in y:
        notes_set[i] = notes_set[i] + 1
    d1 = list(notes_set.keys())
    d2 = list(notes_set.values())
    plt.figure(figsize=(32, 10))
    plt.bar(d1, d2)
    plt.savefig('notes_frequency.jpg', dpi=400, bbox_inches='tight')


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
