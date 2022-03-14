# syntax=docker/dockerfile:1.2
#
# Build command (local build):
#
#  DOCKER_BUILDKIT=1 docker build -t dashboards:latest --build-arg build_type=local --ssh default .
#
# Build arguments
#  - build_type, if set to "local", then the dashboard will run without various additional parameters
#        that are specific to a production build.
#
# To run locally:
#
#  docker run -it --rm --network host dashboards:latest
#
# The parameter --network host attaches the dashboard to your localhost, meaning the dashboard can now be
# accessed on the default port 5006. Furthermore, the dashboard is able to communicate to other services
# running on localhost. If you have an instance of the database running on localhost this can now be used.

FROM python:3.7

# Can be overridden by --build-arg build_type=local
ARG build_type=production

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip

# Install nodejs
ENV NODEJS_VERSION=v14.17.3

RUN wget https://nodejs.org/dist/$NODEJS_VERSION/node-$NODEJS_VERSION-linux-x64.tar.xz \
    && tar -xf node-$NODEJS_VERSION-linux-x64.tar.xz -C /opt \
    && rm node-$NODEJS_VERSION-linux-x64.tar.xz
ENV PATH=/opt/node-$NODEJS_VERSION-linux-x64/bin:${PATH}

# gcsfuse for mounting a Google Cloud Storage bucket
RUN mkdir -p uploads

RUN echo "deb http://packages.cloud.google.com/apt gcsfuse-jessie main" \
    | tee /etc/apt/sources.list.d/gcsfuse.list \
 && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
 && apt update \
 && apt -y install gcsfuse git \
 && rm -rf /var/lib/apt/lists/*

# removed --no-cache-dir
RUN pip install -r requirements.txt

EXPOSE 5006

# this will add the working directory to sys path to add the modules package
ENV PYTHONPATH=.

# Construct base run command.
RUN printf "bokeh serve dashboards/[!_]** " > ./run_dashboards.sh

# Add additional arguments for non-local builds.
RUN if test "$build_type" != "local"; then \
        echo "--prefix \$ROUTE_PREFIX" \
             "--disable-index-redirect" \
             "--num-procs=4" \
             "--port=5006" \
             "--address=0.0.0.0" \
             "--auth-module=/usr/local/lib/python3.7/site-packages/mz_bokeh_package/utilities/auth.py" \
             "--allow-websocket-origin=\$BOKEH_APPS_DOMAIN" >> ./run_dashboards.sh; \
    fi

# This is the main executable including minimal arguments to run.
CMD ["/bin/bash", "run_dashboards.sh"]
