# syntax=docker/dockerfile:1
FROM python:3.7
WORKDIR /code
RUN apt-get update

RUN apt-get install -y libmagickwand-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip uninstall -y opencv-python  
RUN pip uninstall -y opencv-contrib-python
RUN pip install --no-cache-dir opencv-contrib-python-headless
COPY ./app /code/app
COPY ./models /code/models
COPY ./input /code/input
COPY ./output /code/output
COPY ./fonts /code/fonts
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]