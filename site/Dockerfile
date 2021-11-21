FROM python:latest


ADD ./ /site/
WORKDIR /site/

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]