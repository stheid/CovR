FROM tiangolo/uwsgi-nginx:python3.8
COPY . /app
RUN pip install -r /app/requirements.txt
