FROM python:3.9-slim-buster

WORKDIR /usr/src/app

# installing python requirements
COPY requirements.dev.txt ./
RUN pip install --no-cache-dir -r requirements.dev.txt
RUN pip3 install tox
RUN pip3 install wheel

RUN pip3 install tox
RUN pip3 install wheel
# Copying all to the container
COPY . .
RUN ["python","setup.py","sdist","bdist_wheel"]

ENV FLASK_APP=main.py
ENV FLASK_ENV=development
CMD ["flask", "run", "--host=0.0.0.0"]
