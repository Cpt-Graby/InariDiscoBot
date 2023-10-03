FROM python:3.11.5-alpine3.18

ADD main.py settings.py scoreTraker.py requirements.txt ./
RUN mkdir logs
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "./main.py"]
