FROM python:3.8.5

WORKDIR /usr/src/app



COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install gunicorn

COPY . .

ENV FLASK_APP=main



CMD ["python", "main.py"]
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "main:app"]


