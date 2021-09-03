from cassandra.cluster import Cluster

cluster = Cluster(contact_points=['172.17.0.3'], port=9042)
session = cluster.connect()
session.execute("""CREATE KEYSPACE mikeyspace WITH replication = {'class' : 'SimpleStrategy', 'replication_factor':1};""")