import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View

from users.models import User
from env          import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self,request):
        try: 
            data          = json.loads(request.body)
            hash_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

            if not re.search(r'^(?=(.*[A-Za-z]))(?=(.*[0-9]))(?=(.*[@#$%^!&+=.\-_*]))([a-zA-Z0-9@#$%^!&+=*.\-_]){8,}$', data['password']):
                return JsonResponse({'MESSAGE':'NOT_PASSWORD_FORMAT'}, status = 400)

            if User.objects.filter(id=data['id']).exists(): 
                return JsonResponse({'MESSAGE':'INVALID_ID'},status=400)

            User.objects.create(
                id       = data['id'],
                password = hash_password,
            )
            user = User.objects.get(id= data['id'])
            return JsonResponse({'ID':user.id, 'MESSAGE':'SUCCESS'},status=201)
        except KeyError: 
            return JsonResponse({'MESSAGE':'KEY_ERROR'},status=400)

class LoginView(View):
    def post(self,request):
        try :
            data = json.loads(request.body)

            if not User.objects.filter(id=data['id']).exists():
                return JsonResponse({'MESSAGE':'INVALID_ID'},status=400)

            user = User.objects.get(id= data['id'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)

                return JsonResponse({'ID': user.id, 'MESSAGE':'SUCCESS', 'TOKEN': access_token},status=200)

            return JsonResponse({'MESSAGE':'INVALID_USER'},status=400)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'},status=400)