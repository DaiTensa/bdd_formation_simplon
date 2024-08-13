FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8000
EXPOSE 8501

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# Start both the backend and Streamlit dashboard
CMD ["bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload & cd .. & streamlit run dashboard.py --server.port 8501"]

# docker run --rm -p 8000:8000 -p 8501:8501 -v $(pwd):/app apisimplon