FROM python:3.11-alpine

WORKDIR /etc/app/fieldwork-backup

RUN mkdir "/etc/app/fieldwork-backup/data" && \
    mkdir "/etc/app/fieldwork-backup/backup" && \
    mkdir "/etc/app/fieldwork-backup/settings" && \
    mkdir "/etc/app/fieldwork-backup/log"

COPY ../requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ../src  ./
