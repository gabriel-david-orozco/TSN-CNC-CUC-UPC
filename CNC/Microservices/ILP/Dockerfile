FROM gabrielorozcoupc/glpk:latest
ENV PYTHONBUFFERED 1
WORKDIR /ILP
COPY ILP/requirements.txt requirements.txt
RUN bash -c 'source /root/miniconda3/bin/activate base && pip install -r /ILP/requirements.txt'
RUN pip install -r /ILP/requirements.txt
CMD python rabbitmq_queues/pre-ilp.py 
