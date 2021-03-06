FROM python:3.9-slim-buster
ENV MONGO_CONTAINER="mongo"
ENV REDIS_CONTAINER="redis"
ENV FLASK_APP=main.py
ENV FLASK_ENV=development
WORKDIR /usr/src/app

# installing python requirements
COPY requirements.dev.txt ./
RUN pip install --no-cache-dir -r requirements.dev.txt

# Copying all to the container
COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]