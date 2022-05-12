# Universal API Gateway

![ugw-block-diagram drawio](https://user-images.githubusercontent.com/17728233/167995708-1b7e8029-c83d-41cb-8a75-517a6ace54f9.png)


## DockerImage For Linux/Mac

```docker
FROM tiangolo/uvicorn-gunicorn:python3.8

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir fastapi

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
```

## DockerImage For Raspberry PI

```docker
FROM python:3.7

RUN pip install fastapi uvicorn
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir fastapi

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app

EXPOSE 8050
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8050"]
```

### requirements.txt

```text
mysql-connector==2.1.7
requests
pydantic
```

## How to run in Linux/Mac

```docker
docker build -t uniapigw ./ --no-cache
```

```docker
docker run -d -p 8888:80 -v $(pwd):/app --name uniapigw uniapigw /start-reload.sh
```

## How to run in Raspberry PI

```docker
docker build -t uniapigw ./ --no-cache
```

```docker
docker run -d --name uniapigw -p 8888:8888 uniapigw
```
