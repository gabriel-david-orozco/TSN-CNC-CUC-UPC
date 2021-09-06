from cassandra.cluster import Cluster

# cluster = Cluster(contact_points=['172.17.0.3'], port=9042)
# session = cluster.connect()
# session.execute("""DROP KEYSPACE newkeyspace""")
# session.execute("""CREATE KEYSPACE newkeyspace WITH replication = {'class' : 'SimpleStrategy', 'replication_factor':1};""")
# session.execute("""USE newkeyspace""")
# #session.execute("""DROP TABLE usuarios""")
# session.execute("""CREATE TABLE usuarios (
#   usrid int PRIMARY KEY,
#   nombre text,
#   ape1 text
# );""")
# session.execute("""INSERT INTO usuarios (usrid, nombre, ape1) VALUES (1, 'Gabriel', 'Orozco');""")

# session.execute("""select * from usuarios;""")

class Cassandra_connecion():
  def __init__(self) :
      self.cluster = Cluster(contact_points=['172.17.0.2'], port=9042)
      self.session = self.cluster.connect()
      try :
        self.session.execute("""CREATE KEYSPACE cassandra_namespace \
      WITH replication = {'class' : 'SimpleStrategy', 'replication_factor':1};""")
      except :
        pass 
  def table_creator(self, table_name):
    self.session.execute("""USE cassandra_namespace""")
    droping_string = '"""DROP TABLE ' + table_name + '"""'
    try:
      self.session.execute(droping_string)
    except :
      pass
    creating_string = '"""CREATE TABLE' + table_name + '( usrid int PRIMARY KEY, nombre text,ape1 text);"""'
    self.session.execute(creating_string)
 
cassandra = Cassandra_connecion()
cassandra.table_creator("Topology")