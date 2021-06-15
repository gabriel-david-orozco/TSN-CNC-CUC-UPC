python3 -m pip uninstall /home/jukebox-jetconf/jetconf_jukebox/jetconf_jukebox
rm /home/jukebox-jetconf/jetconf_jukebox/*.py
cp *.py /home/jukebox-jetconf/jetconf_jukebox/
python3 -m pip install /home/jukebox-jetconf/jetconf_jukebox/.
jetconf -c /home/jetconf/data/example-config.yaml
# you just leave it at the moment to start automizing the deploying process
