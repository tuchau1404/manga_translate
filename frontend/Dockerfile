# syntax=docker/dockerfile:1
FROM python:3.7-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./input /code/input
EXPOSE 8501
CMD ["streamlit", "run", "./app/main.py"]