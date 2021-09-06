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
  
  
  def table_creator(self, table_name, columns):
    self.session.execute("""USE cassandra_namespace""")
    try:
      self.session.execute("DROP TABLE " + table_name)
    except :
      print("The table does not exit, creating ")
    special_characters = "']["
    for element in special_characters:
      print("entering 1 time", element)
      columns = str(columns).replace(element, "")
    self.session.execute("CREATE TABLE " + table_name + "( " + str(columns) + ");")

  def insert_in_table(self, table_name, keyed_values):
    special_characters = "]["
    values = keyed_values
    for element in special_characters:
      values = str(list(values.values())).replace(element, "")
    keys = ", ".join(keyed_values.keys())
    print(keys, values)
    self.session.execute("INSERT INTO " + table_name+ " (" + keys + ") VALUES ("+ values +");")

cassandra = Cassandra_connecion()
columns = ["usrid text PRIMARY KEY"," nombre text", " ape1 text"]
filling_values = {"usrid": "1", "nombre": "Gabriel", "ape1": "Orozco"}
cassandra.table_creator("Topology", columns)
cassandra.insert_in_table("Topology", filling_values)