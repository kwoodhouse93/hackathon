FROM django:1.9-python2

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

COPY entrypoint.sh /usr/bin/entrypoint.sh

RUN chmod ugo+x /usr/bin/entrypoint.sh

EXPOSE 8000

CMD "/usr/bin/entrypoint.sh"
