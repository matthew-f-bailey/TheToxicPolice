FROM python:3.8

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn", "app:server", "-b", ":8000" ]
