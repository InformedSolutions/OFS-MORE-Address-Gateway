FROM python:3.5-slim
ENV PYTHONUNBUFFERED 1
ADD requirements.txt /source/
RUN mkdir /source/logs
WORKDIR /source
RUN pip install -r requirements.txt
ADD . /source/
RUN chmod +x /source/docker-entrypoint.sh
EXPOSE 8000
CMD ["/source/docker-entrypoint.sh"]