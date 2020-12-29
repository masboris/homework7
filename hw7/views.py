import hashlib
import random
from io import BytesIO

from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
from django.shortcuts import render, HttpResponse, redirect

from homework7 import settings
from hw7.models import User

# Create your views here.

def register(request):

macbook = 'test macbook2'
pc = 'pc'
    token = request.COOKIES.get('token', 'none')


    if token == 'none':
        if request.method == 'GET':
            return render(request, 'register.html')
        else:

            received_code = request.POST.get('code')
            stored_code = request.session.get('verify_code')

            username = str(request.POST.get('username')).lower()

            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'msg': 'Username already exists, try another one'})

            if received_code!= stored_code:
                return render(request, 'register.html', {'msg': 'Verify Code is wrong, try again.'})
            else:


                password = request.POST.get('password')
                ip = request.META.get("REMOTE_ADDR")
                icon = request.FILES.get('icon')

                user = User()
                user.username = username
                user.password = password
                token = generate_token(ip, user.username)
                user.user_token = token
                user.user_icon = icon
                user.save()

                response = redirect('/home')
                response.set_cookie('token', token)

                return response

    else:
        user = User.objects.get(user_token=token)
        return render(request, 'home.html', {'user': user, 'msg': 'You are logged in!'})



def login(request):

    token = request.COOKIES.get('token', 'none')

    if token == 'none':
        if request.method == 'GET':
            return render(request, 'login.html')
        else:
            ip = request.META.get("REMOTE_ADDR")
            username = str(request.POST.get('username')).lower()
            password = request.POST.get('password')
            login_token = generate_token(ip, username)

            try:
                user = User.objects.get(username=username, password=password, user_token=login_token)

            except:
                return render(request, 'login.html', {'msg': "Username or password is incorrect, try again."})

            else:
                response = redirect('/home')
                response.set_cookie('token', user.user_token)
                return response

    else:
        user = User.objects.get(user_token=token)
        return render(request, 'home.html', {'user': user, 'msg': 'You are logged in!'})


def home(request):

    token = request.COOKIES.get('token', 'none')

    if token == 'none':
        return redirect('/login')
    else:
        user = User.objects.get(user_token=token)
        return render(request, 'home.html', {'user':user, 'msg': 'You are logged in!'})

def generate_token(ip, name):
    return hashlib.md5((ip+name).encode('utf-8')).hexdigest()



def logout(request):
    response = redirect('/login')
    response.delete_cookie('token')
    return response

def getCode(request):
    mode = 'RGB'
    size = (200,100)
    red = get_color()
    green = get_color()
    blue = get_color()
    color = (red,green,blue)
    image = Image.new(mode=mode, size=size, color=color)
    imagefont = ImageFont.truetype(settings.FONT_PATH,80)
    imageDraw = ImageDraw(image)

    verify_code = generate_code()
    request.session['verify_code'] = verify_code

    for i in range(4):
        fill = (get_color(),get_color(),get_color())
        imageDraw.text(xy=(50*i, 0), text=verify_code[i], font=imagefont,fill=fill)


    for i in range(200):
        fill = (get_color(),get_color(),get_color())
        xy = (random.randrange(201),random.randrange(101))
        imageDraw.point(xy=xy,fill=fill)


    fp = BytesIO()
    image.save(fp,'png')
    return HttpResponse(fp.getvalue(), content_type='image/png')

def get_color():
    return random.randrange(256)

def generate_code():
    source = 'qwrtyutiyuiopasdffghjghjlzxcbvvbnm132447686780IUHVOINJZWAE'
    code = ''
    for i in range(4):
        code += random.choice(source)

    return code
