from cassandra.cluster import Cluster

class Cassandra_connecion():
  def __init__(self) :
      self.cluster = Cluster(contact_points=['localhost'], port=9042)
      self.session = self.cluster.connect()
      try :
        self.session.execute("""CREATE KEYSPACE cassandra_namespace \
      WITH replication = {'class' : 'SimpleStrategy', 'replication_factor':1};""")
      except :
        pass 
  
# This method receives the values in a list, each element is the value, the type and if it is or not Foreign key
# E.g., columns = ["usrid text PRIMARY KEY"," nombre text", " ape1 text"]
  def table_creator(self, table_name, columns):
    self.session.execute("""USE cassandra_namespace""")
    try:
      self.session.execute("DROP TABLE " + table_name)
    except :
      print("The table does not exit, creating ")
    special_characters = "']["
    for element in special_characters:
      columns = str(columns).replace(element, "")
    self.session.execute("CREATE TABLE " + table_name + "( " + str(columns) + ");")

# This method receives the values as a dictionary where the key are the names of the columns in the table
#and the values are the values to give
# E.g., filling_values = {"usrid": "1", "nombre": "Gabriel", "ape1": "Orozco"}

  def insert_in_table(self, table_name, keyed_values):
    special_characters = "]["
    values = str(list(keyed_values.values()))
    for element in special_characters:
      values = values.replace(element, "")
    keys = ", ".join(keyed_values.keys())
    self.session.execute("INSERT INTO " + table_name + " (" + keys + ") VALUES ("+ values +");")
  
  def find_in_table(self, table_name, element="*"):
    query_result = self.session.execute("select " + element + " from " + table_name + ";")
    row = query_result.one()
    return row


# cassandra = Cassandra_connecion()
# columns = ["usrid text PRIMARY KEY"," nombre text", " ape1 text"]
# filling_values = {"usrid": "1", "nombre": "Gabriel", "ape1": "Orozco"}
# cassandra.table_creator("Topology", columns)
# cassandra.insert_in_table("Topology", filling_values)
# print(cassandra.find_in_table("Topology") )