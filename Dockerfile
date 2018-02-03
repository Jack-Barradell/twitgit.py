FROM  tiangolo/uwsgi-nginx-flask:python3.6
COPY requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY ./app /app


# TODO: Set envs here

EXPOSE 80
EXPOSE 443
