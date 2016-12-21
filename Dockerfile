FROM django:1.9-python2

RUN apt-get update && apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY production-entrypoint.sh entrypoint.sh wait-for-postgres.sh /usr/bin/

RUN chmod ugo+x /usr/bin/entrypoint.sh /usr/bin/wait-for-postgres.sh /usr/bin/production-entrypoint.sh

EXPOSE 8000

CMD "/usr/bin/entrypoint.sh"

COPY . /usr/src/app
VOLUME /usr/src/app
