FROM python:latest

LABEL authors="Yevhenii"

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.main
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
