# Sommoong

## 주의 사항
+ runserver 전에 반드시, 아래의 과정을 통해 DB 초기화를 시킬 것!
  + 1. db.sqlite3 삭제 (있다면)
  + 2. python manage.py makemigrations
  + 3. python manage.py migrate
  + 4. python manage.py loaddata init.json
    + 오류가 발생하지 않는다면, ```Installed 450 object(s) from 1 fixture(s)``` 라고 뜰 것!
+ init.json 에 DB 초기화에 필요한 계정, 동물, 보호소 등의 정보가 모두 포함되어있으므로, 별도로 craetesuperuser 를 하지 않아도, loaddata 하는 순간 자동으로 관리자 계정이 생성

+ 모든 계정의 비밀번호는 qppr1004 로 통일 (admin id 는 admin)

+ login 앱의 경로를 ```/login``` 에서 ```/member``` 로 임시 변경 (```somproject/urls.py``` 참고)
  + ```/login``` 을 최상위 경로로 사용하는 경우, 로그아웃에 대한 URL ```/login/logout``` 됨. 뭔가.. URL 이 난해해짐

+ 인증 문자 전송을 기능을 AWS SNS 사용하여 구현 