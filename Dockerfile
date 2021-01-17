FROM python:3.7

WORKDIR /usr/src/app

COPY . .

# gcsfuse for mounting a Google Cloud Storage bucket
RUN mkdir -p uploads

# FIXME: As soon as mz-bokeh-package becomes a pypi package, we no longer need to apt install git.
RUN echo "deb http://packages.cloud.google.com/apt gcsfuse-jessie main" \
    | tee /etc/apt/sources.list.d/gcsfuse.list \
 && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
 && apt update \
 && apt -y install gcsfuse git \
 && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

EXPOSE 5006

ENV PYTHONPATH=.

CMD bokeh serve --prefix $ROUTE_PREFIX --disable-index-redirect --num-procs=4 --port=5006 --address=0.0.0.0 --auth-module=/usr/local/lib/python3.7/site-packages/mz_bokeh_package/auth.py --allow-websocket-origin=$BOKEH_APPS_DOMAIN --glob dashboards/*.py dashboards/**
