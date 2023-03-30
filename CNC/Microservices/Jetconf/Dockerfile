FROM gabrielorozcoupc/jetconf:v4
ENV PYTHONBUFFERED 1
WORKDIR /Jetconf
RUN rm -r /home/jukebox-jetconf/yang-modules/ieee802-dot1q-tsn-types-upc-version@2018-02-15.yang
COPY ieee802-dot1q-tsn-types-upc-version-v2@2018-02-15.yang /home/jukebox-jetconf/yang-modules/ieee802-dot1q-tsn-types-upc-version@2018-02-15.yang
RUN python3 -m pip uninstall jetconf_jukebox -y
RUN rm /home/jukebox-jetconf/jetconf_jukebox/*.py
COPY Jetconf/*.py /home/jukebox-jetconf/jetconf_jukebox/
RUN python3 -m pip install /home/jukebox-jetconf/.
#RUN jetconf -c /home/jetconf/data/example-config.yaml
#COPY Jetconf/requirements.txt Jetconf/requirements.txt
#RUN pip install -r Jetconf/requirements.txt 
#CMD python rabbitmq_queues/pre-ilp.py 
