from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, 'jychat/index.html')

def enter_room(request, room_name):
    return render(request, 'jychat/room.html', {
        'room_name' : room_name,
    })