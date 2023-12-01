# syntax=docker/dockerfile:1
FROM python
WORKDIR /weatherBridge
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=get_handler.py
EXPOSE 8080
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080", "--no-reload" ]
