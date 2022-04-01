def handle_uploaded_file(f):
    print(f.name)
    with open('in.mid', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)