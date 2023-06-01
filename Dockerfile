FROM ubuntu:20.04

RUN apt-get update && apt-get install -y --no-install-recommends tesseract-ocr

RUN apt-get install -y wget build-essential libncursesw5-dev libssl-dev \
libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

RUN apt-get install -y python3 python3-distutils

RUN set -xe \
    && apt-get update -y \
    && apt-get install -y python3-pip

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["household_accounts/app.py"]
