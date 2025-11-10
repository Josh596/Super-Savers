# syntax=docker/dockerfile:1

FROM python:3.8.16

ARG BUILD_ENVIRONMENT=local

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD admin

# Set the WORKDIR 
WORKDIR /app

# install dependencies  
RUN pip install --upgrade pip

# COPY ./requirements .


# Copy the files
COPY . .

RUN pip install -r requirements.txt


# Expose port 8000
EXPOSE 8000

# Start the server
# Start the server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# CMD sh -c 'while !</dev/tcp/db/5432; do sleep 1; done; \
#     python manage.py makemigrations && \
#     python manage.py migrate && \
#     python manage.py createsuperuser --noinput \
#         --email admin@example.com \
#         --username admin \
#         --password adminpassword && \
#     python manage.py runserver 0.0.0.0:8000'