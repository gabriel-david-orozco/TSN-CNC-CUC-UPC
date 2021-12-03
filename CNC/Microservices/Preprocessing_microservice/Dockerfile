FROM python:3.9
ENV PYTHONBUFFERED 1
WORKDIR /preprocessing
COPY Preprocessing_microservice/requirements.txt /preprocessing/requirements.txt
COPY Preprocessing_microservice/utilities/wait-for-it.sh /preprocessing/utilities/wait-for-it.sh
RUN pip install -r requirements.txt 
CMD python /preprocessing/rabbitmq_queues/jet-pre.py & python /preprocessing/rabbitmq_queues/top-pre.py 