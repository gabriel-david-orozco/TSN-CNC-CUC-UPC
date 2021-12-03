FROM gabrielorozcoupc/glpk:latest
ENV PYTHONBUFFERED 1
WORKDIR /ILP
COPY ILP/requirements.txt ILP/requirements.txt
RUN pip install -r ILP/requirements.txt 
CMD python rabbitmq_queues/pre-ilp.py 
