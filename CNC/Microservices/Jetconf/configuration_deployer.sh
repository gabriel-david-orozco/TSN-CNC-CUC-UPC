rm -r /home/jukebox-jetconf/yang-modules/ieee802-dot1q-tsn-types-upc-version@2018-02-15.yang
cp ieee802-dot1q-tsn-types-upc-version-v2@2018-02-15.yang /home/jukebox-jetconf/yang-modules/ieee802-dot1q-tsn-types-upc-version@2018-02-15.yang
rm /home/jukebox-jetconf/jetconf_jukebox/*.py
rm /home/jukebox-jetconf/tsn-example.json
cp tsn-example.json /home/jukebox-jetconf/
cp *.py /home/jukebox-jetconf/jetconf_jukebox/
rm /home/jetconf/data/example-config.yaml
cp configuration_files/example-config.yaml /home/jetconf/data/example-config.yaml
cd /home/jukebox-jetconf/jetconf_jukebox/
python3 -m pip uninstall jetconf_jukebox -y
python3 -m pip install /home/jukebox-jetconf/.
jetconf -c /home/jetconf/data/example-config.yaml
# you just leave it at the moment to start automizing the deploying process
