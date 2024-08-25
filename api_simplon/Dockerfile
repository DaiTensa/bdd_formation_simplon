FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# docker build -t apisimplon .
# docker run --rm --env-file .env  -p 8000:8000 -v $(pwd):/app apisimplon
# docker run --rm --env-file .env  -p 8000:8000 apisimplon