python3 -m pip uninstall /home/jukebox-jetconf/jetconf_jukebox/jetconf_jukebox
rm /home/jukebox-jetconf/jetconf_jukebox/*.py
cp *.py /home/jukebox-jetconf/jetconf_jukebox/
python3 -m pip install /home/jukebox-jetconf/.
jetconf -c /home/jetconf/data/example-config.yaml

rm -r /home/jukebox-jetconf/yang-modules/ieee802-dot1q-tsn-types-upc-version@2018-02-15.yang
cp /home/TSN-CNC-CUC-UPC/Yang_models/ieee802-dot1q-tsn-types-upc-version-v2@2018-02-15.yang /home/jukebox-jetconf/yang-modules/ieee802-dot1q-tsn-types-upc-version@2018-02-15.yang
# you just leave it at the moment to start automizing the deploying process
