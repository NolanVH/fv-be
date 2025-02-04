ARG python_image=python:3.11.2-alpine
ARG caddy_image=caddy:2.6.4-alpine

FROM $python_image as django-common
ENV DEBUG_DISABLE=True

WORKDIR /app
RUN apk add build-base
RUN apk add libffi-dev
RUN pip3 install gunicorn

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app/firstvoices

# intermediate stage to assemble static files for the caddy runtime stage
FROM django-common as static-collector
RUN ["python3", "manage.py", "collectstatic"]

# select with --target static-runtime at build time
FROM $caddy_image as static-runtime
COPY --from=django-common /app/Caddyfile /etc/caddy
COPY --from=static-collector /app/firstvoices/static /srv

# or django-runtime for the api server. this is last so that it's the default if no target specified
FROM django-common as django-runtime
EXPOSE 8000
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "firstvoices.wsgi:application"]

