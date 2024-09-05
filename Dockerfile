FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y tzdata

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]