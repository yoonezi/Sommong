find . -path "*.sqlite3" -delete &&\
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf &&\
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete &&\
python ./manage.py makemigrations &&\
python ./manage.py migrate &&\
python manage.py loaddata init.json

## somproject 폴더 들어가서 ../init_server.sh 실행