# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

FROM python:3.8-slim-buster

RUN apt update -y && apt install awscli -y
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt


# Run app.py when the container launches
CMD ["uvicorn", "app:fastapi_app", "--host", "0.0.0.0", "--port", "8080"]
