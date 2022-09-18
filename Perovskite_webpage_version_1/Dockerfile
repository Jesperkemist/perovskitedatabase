# Build:
#  docker build -t perovskite-webpage:$(git rev-parse HEAD) -t perovskite-webpage:latest .
# Run:
#  docker run -it --rm -p 8080:8080 perovskite-webpage:latest

FROM python:3.8-slim

WORKDIR perovskite-webpage

# FIXME: the version of the itsdangerous package is fixed due to a bug in the latest version
#        check whether the website works without fixing the version and, if so, remove it from the next line
RUN pip install flask==2.2.2 waitress==2.1.2 itsdangerous==2.1.2

COPY . ./Perovskite_webpage_version_1

ENV FLASK_APP=Perovskite_webpage_version_1
ENV FLASK_ENV=production

EXPOSE 8080

ENTRYPOINT ["waitress-serve", "--call", "Perovskite_webpage_version_1:create_app"]
