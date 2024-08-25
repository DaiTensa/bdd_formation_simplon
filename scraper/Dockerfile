FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

# Start both the backend and Streamlit dashboard
CMD ["python", "start.py"]


# Build the image
# docker build -t scrapingimage .
# docker run --rm --env-file .env -v $(pwd):/SCRAPER scrapingimage
# docker run --rm --env-file .env scrapingimage