from cassandra.cluster import Cluster

cluster = Cluster(contact_points=['172.17.0.3'], port=9042)
session = cluster.connect()
session.execute("""DROP KEYSPACE newkeyspace""")
session.execute("""CREATE KEYSPACE newkeyspace WITH replication = {'class' : 'SimpleStrategy', 'replication_factor':1};""")
session.execute("""USE newkeyspace""")
session.execute("""DELETE TABLE usuarios""")
session.execute("""CREATE TABLE usuarios (
  usrid int PRIMARY KEY,
  nombre text,
  ape1 text
);""")
session.execute("""INSERT INTO usuarios (usrid,nombre, ape1) VALUES (1, "Gabriel", "Orozco");""")

session.execute("""select * from usuarios;""")