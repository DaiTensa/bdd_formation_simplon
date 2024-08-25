FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8501

# Start both the backend and Streamlit dashboard
CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501", "--server.address", "0.0.0.0"]

# docker build -t dashboardsimplon .
# docker run --rm --env-file .env -p 8501:8501 -v $(pwd):/dashboard dashboardsimplon
# docker run --rm --env-file .env -p 8501:8501 dashboardsimplon