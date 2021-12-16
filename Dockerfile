FROM tiangolo/uvicorn-gunicorn:python3.8

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir fastapi

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
EXPOSE 8888