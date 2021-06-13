#FROM nginx:latest
FROM python:latest
#RUN apt-get update -y && apt-get install -y python3-pip

#WORKDIR /usr/share/nginx/html



COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install uwsgi


COPY . .

#COPY nginx.conf /etc/nginx/nginx.conf
CMD [ "python", "./main.py" ]
#CMD [ "uwsgi",  "--http-socket", "0.0.0.0:8079", "--module", "main:app", "--processes", "2", "--threads",  "4" ]

