# [Assignment 7] CARDOC  


## 과제  안내

### 배포 주소  
http://3.144.122.195:8000/  

### Documentation API  
https://documenter.getpostman.com/view/16891318/UVC8CRFW  

## 1. 배경 및 공통 요구사항

<aside>
😁 **카닥에서 실제로 사용하는 프레임워크를 토대로 타이어 API를 설계 및 구현합니다.**

</aside>

- 데이터베이스 환경은 별도로 제공하지 않습니다.
 **RDB중 원하는 방식을 선택**하면 되며, sqlite3 같은 별도의 설치없이 이용 가능한 in-memory DB도 좋으며, 가능하다면 Docker로 준비하셔도 됩니다.
- 단, 결과 제출 시 README.md 파일에 실행 방법을 완벽히 서술하여 DB를 포함하여 전체적인 서버를 구동하는데 문제없도록 해야합니다.
- 데이터베이스 관련처리는 raw query가 아닌 **ORM을 이용하여 구현**합니다.
- Response Codes API를 성공적으로 호출할 경우 200번 코드를 반환하고, 그 외의 경우에는 아래의 코드로 반환합니다.

[Copy of Code](https://www.notion.so/08e67c3cdc8e471fb1aab50e5963fb05)

---

## 2. 사용자 생성 API

🎁 **요구사항**

- ID/Password로 사용자를 생성하는 API.
- 인증 토큰을 발급하고 이후의 API는 인증된 사용자만 호출할 수 있다.

```jsx
/* Request Body 예제 */
 { "id": "candycandy", "password": "ASdfdsf3232@" }
```

---

## 3. 사용자가 소유한 타이어 정보를 저장하는 API

🎁 **요구사항**

- 자동차 차종 ID(trimID)를 이용하여 사용자가 소유한 자동차 정보를 저장한다.
- 한 번에 최대 5명까지의 사용자에 대한 요청을 받을 수 있도록 해야한다. 즉 사용자 정보와 trimId 5쌍을 요청데이터로 하여금 API를 호출할 수 있다는 의미이다.

```jsx
/* Request Body 예제 */
[
  {
    "id": "candycandy",
    "trimId": 5000
  },
  {
    "id": "mylovewolkswagen",
    "trimId": 9000
  },
  {
    "id": "bmwwow",
    "trimId": 11000
  },
  {
    "id": "dreamcar",
    "trimId": 15000
  }
]
```

🔍 **상세구현 가이드**

- 자동차 정보 조회 API의 사용은 아래와 같이 5000, 9000부분에 trimId를 넘겨서 조회할 수 있다.
 **자동차 정보 조회 API 사용 예제 → 
📄** [https://dev.mycar.cardoc.co.kr/v1/trim/5000](https://dev.mycar.cardoc.co.kr/v1/trim/5000)
**📄** [https://dev.mycar.cardoc.co.kr/v1/trim/9000
📄](https://dev.mycar.cardoc.co.kr/v1/trim/9000) [https://dev.mycar.cardoc.co.kr/v1/trim/11000
📄](https://dev.mycar.cardoc.co.kr/v1/trim/11000) [https://dev.mycar.cardoc.co.kr/v1/trim/15000](https://dev.mycar.cardoc.co.kr/v1/trim/15000)
- 조회된 정보에서 타이어 정보는 spec → driving → frontTire/rearTire 에서 찾을 수 있다.
- 타이어 정보는 205/75R18의 포맷이 정상이다. 205는 타이어 폭을 의미하고 75R은 편평비, 그리고 마지막 18은 휠사이즈로써 {폭}/{편평비}R{18}과 같은 구조이다.
 위와 같은 형식의 데이터일 경우만 DB에 항목별로 나누어 서로다른 Column에 저장하도록 한다.

---

## 4. 사용자가 소유한 타이어 정보 조회 API

🎁 **요구사항**

- 사용자 ID를 통해서 2번 API에서 저장한 타이어 정보를 조회할 수 있어야 한다.


## 사용한 기술 스택

Back-end : <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;
<img alt="Python" src = "https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>&nbsp;
<p>
Tool : <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"/>
</p>

## 모델링  

![스크린샷 2021-11-29 오전 5 11 47](https://user-images.githubusercontent.com/78228444/143784529-ef9178f8-b388-43a5-ae43-cabebc1bc9c2.png)



## 파일 구조  
- `./cars`
  - `./migration`
  - `./__init__.py`
  - `./admin.py`
  - `./apps.py`
  - `./models.py`
  - `./tests.py`
  - `./urls.py`
  - `./views.py`
- `./config`
  - `./__init__.py`    
  - `./asgi.py`
  - `./settings.py`
  - `./urls.py`
  - `./wsgi.py`
- `./core`
  - `./migration`
  - `./__init__.py`
  - `./apps.py`
  - `./utils.py`
- `./users`
  - `./migration`
  - `./__init__.py`
  - `./admin.py`
  - `./apps.py`
  - `./models.py`
  - `./tests.py`
  - `./urls.py`
  - `./utils.py`
  - `./views.py`
- `./.gitignore`
- `./manage.py`
- `./README.md`
- `./requirements.txt`

## 구현기능  

### 회원가입 API
**endpoint** : `http://3.144.122.195:8000/users/signup`
- ```request``` : body

```python
{
    "id": "gnsxo9",
    "password": "!!!gnsxo9"
}
```
- ```로그인 성공시``` : status_code : 201

```python
- JSON
{
    "ID": "gnsxo9",
    "MESSAGE": "SUCCESS",
}
```

- ```회원가입 실패시``` : 
1. 비밀번호가 8자리이상 특수문자 포함 : 400, 
2. 키에러가 발생했을시 status_code : 400
```python
- JSON
{
    1: "MESSAGE":"NOT_PASSWORD_FORMAT",
    2: "MESSAGE": "KEY_ERROR"   
}

``` 

### 로그인 API
**endpoint** : `http://3.144.122.195:8000/users/login`

- ```request``` : body
```python
- JSON
{
    "id": "gnsxo9",
    "password": "!!!gnsxo9"
}
```
- ```로그인 성공시``` : status_code 200,
```python
- JSON
{
    "ID": "gnsxo9",
    "MESSAGE": "SUCCESS",
    "TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Imduc3hvMTMifQ.zUsJXhHvUVPzWbrs5k6fLuqTFkNN2b01w6_wRTACZEI"
}
``` 

- ```로그인 실패시``` : 
1. 일치하는 아이디 없을때 : 400,
2. 비밀번호와 아이디가 일치하지 않을때 : 400
3. 키에러 :400 
``` python
- JSON
{
    1. "MESSAGE": "INVALID_ID",
    2. "MESSAGE": "INVALID_USER",
    3. "MESSAGE": "KEY_ERROR"
}
```

### 타이어 생성 API
**endpoint** : `http://3.144.122.195:8000/cars`
- ```request``` : body
```python
[
    {
        "id": "gnsxo12",
        "trimId": 9000
    },
    {
        "id": "gnsxo13",
        "trimId": 14000
    },
    {
        "id": "gnsxo14",
        "trimId": 5000
    }
]
```

- ```타이어 생성 성공시``` : status 200,
``` python
- JSON
{
    "results": [
        {
            "USER": "gnsxo12",
            "MESSAGE": "SUCCESS"
        },
        {
            "USER": "gnsxo13",
            "MESSAGE": "SUCCESS"
        },
        {
            "USER": "gnsxo14",
            "MESSAGE": "SUCCESS"
        }
    ]
}
```
- ```타이어 중복된 타이어가 있을시``` : status 200, 
``` python
- JSON
{
    "results": [
        {
            "USER": "gnsxo12",
            "MESSAGE": "INVALID_TRIM"
        },
        {
            "USER": "gnsxo13",
            "MESSAGE": "INVALID_TRIM"
        },
        {
            "USER": "gnsxo14",
            "MESSAGE": "INVALID_TRIM"
        }
    ]
}
```

- ```요청이 5개 이상일시``` : status 400, 
``` python
- JSON
{
    "MESSAGE": "MANY_REQUESTS"
}
```

- ```키에러``` : status 400, 
``` python
- JSON
{
    "MESSAGE": "KEY_ERROR"
}
```

### 타이어 조회 API
**endpoint** : `http://3.144.122.195:8000/cars/tire?offset={offset}`
<p>
<b>header</b> : jwt
</p>

- ``` 조회 성공 시 ``` : status 200

```python
{
    "USER_TIRE": [
        {
            "name": "오피러스",
            "front_tire": {
                "width": 225,
                "aspect_ratio": 60,
                "wheel_size": 16
            },
            "rear_tire": {
                "width": 225,
                "aspect_ratio": 60,
                "wheel_size": 16
            }
        },
        {
            "name": "SM5",
            "front_tire": {
                "width": 205,
                "aspect_ratio": 65,
                "wheel_size": 16
            },
            "rear_tire": {
                "width": 205,
                "aspect_ratio": 65,
                "wheel_size": 16
            }
        },
        {
            "name": "캘리버",
            "front_tire": {
                "width": 215,
                "aspect_ratio": 60,
                "wheel_size": 17
            },
            "rear_tire": {
                "width": 215,
                "aspect_ratio": 60,
                "wheel_size": 17
            }
        }
    ]
}
```

- ```사용자의 정보에 저장된 타이어정보가 없을때``` : status 404,
``` python
{
  "MESSAGE": "NOT_FOUND"
}
```

# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 카닥에서 출제한 과제를 기반으로 만들었습니다.
