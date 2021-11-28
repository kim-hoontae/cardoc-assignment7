import json, requests, re

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from users.models import User
from cars.models  import UserCar, Car, Tire, Position
from core.utils   import login_decorator

class CarView(View):
    def cardoc_api(self, trim_id):
        url = "https://dev.mycar.cardoc.co.kr/v1/trim/"
        response = requests.get(url + str(trim_id), timeout=3)

        return response.json()
        
    def get_car_info(self, trim_info, front_tire_info, rear_tire_info):
        front_tire, _ = Tire.objects.get_or_create(
            position_id  = Position.Type.FRONT.value,
            width        = front_tire_info[0],
            aspect_ratio = front_tire_info[1],
            wheel_size   = front_tire_info[2],
        )

        rear_tire, _ = Tire.objects.get_or_create(
            position_id  = Position.Type.REAR.value,
            width        = rear_tire_info[0],
            aspect_ratio = rear_tire_info[1],
            wheel_size   = rear_tire_info[2],
        )

        car, _ = Car.objects.get_or_create(
            name       = trim_info['modelName'],
            front_tire = front_tire,
            rear_tire  = rear_tire,
        )
        return car


    def post(self, request):
        try:
            datas = json.loads(request.body)
            results = []

            if len(datas) > 5:
                return JsonResponse({'MESSAGE' : 'MANY_REQUESTS'}, status=400)

            with transaction.atomic():
                for data in datas:
                    user      = User.objects.get(id=data['id'])
                    trim_info = self.cardoc_api(data['trimId'])

                    front_tire_info = re.split(r'[/,R]', trim_info['spec']['driving']['frontTire']['value'])
                    rear_tire_info  = re.split(r'[/,R]', trim_info['spec']['driving']['rearTire']['value'])

                    car = self.get_car_info(trim_info, front_tire_info, rear_tire_info)

                    if not UserCar.objects.filter(user_id=user.id, car_id=car.id).exists():
                        UserCar.objects.create(
                            user_id = user.id,
                            car_id  = car.id)
                                
                        results.append({'USER': user.id, 'MESSAGE':'SUCCESS'})
                    else:
                        results.append({'USER': user.id, 'MESSAGE':'INVALID_TRIM'})

            return JsonResponse({'results': results}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)


    @login_decorator
    def get(self, request):
        user = request.user

        OFFSET = int(request.GET.get('offset', 0))
        LIMIT  = int(request.GET.get('limit', 5))

        user_cars = UserCar.objects.select_related('car')\
            .filter(user_id=user.id)[OFFSET:OFFSET+LIMIT]

        user_tire = [
            {
                'name': user_car.car.name,
                'front_tire': {
                    'width'       : user_car.car.front_tire.width,
                    'aspect_ratio': user_car.car.front_tire.aspect_ratio,
                    'wheel_size'  : user_car.car.front_tire.wheel_size,
                },
                'rear_tire': {
                    'width'       : user_car.car.rear_tire.width,
                    'aspect_ratio': user_car.car.rear_tire.aspect_ratio,
                    'wheel_size'  : user_car.car.rear_tire.wheel_size,
                }
            }for user_car in user_cars]

        if not user_tire:
            return JsonResponse({'MESSAGE': 'NOT_FOUND'}, status=404)

        return JsonResponse({'USER_TIRE': user_tire}, status=200)