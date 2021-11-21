FROM python:latest


ADD ./ /site/
WORKDIR /site/

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]