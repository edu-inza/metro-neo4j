from neo4j import GraphDatabase
import os

# driver = GraphDatabase.driver('bolt://0.0.0.0:7687',
#                               auth=('neo4j', 'neo4j'))

db_api_address = "127.0.0.1"
if (os.environ.get('NEO4J_ADDRESS')):
    db_api_address = os.environ.get('NEO4J_ADDRESS')

driver = GraphDatabase.driver('bolt://{neo4j_address}:7687'.format(neo4j_address=db_api_address),
                              auth=('neo4j', 'neo4j'))

# deleting data to clean data base
print('Deleting previous data')

query = '''
MATCH (n) 
DETACH DELETE n
'''

with driver.session() as session:
    print(query)
    session.run(query)

print('done') 

# inserting data
print('Inserting Stations')

query = '''
LOAD CSV WITH HEADERS FROM 'https://github.com/pauldechorgnat/cool-datasets/raw/master/ratp/stations.csv' AS row
CREATE (:Station {name_clean: row.nom_clean, 
                    name_station:row.nom_gare, 
                    location: point({x:toFloat(row.x), y:toFloat(row.y)}),
                    traffic: toInteger(row.Trafic), 
                    city: row.Ville,
                    line: toInteger(row.ligne)
});
'''

with driver.session() as session:
    print(query)
    session.run(query)

print('done')

print('Inserting Train Relations')

query = '''
LOAD CSV WITH HEADERS FROM 'https://github.com/pauldechorgnat/cool-datasets/raw/master/ratp/liaisons.csv' AS row
MATCH (s1: Station) WHERE s1.name_clean = row.start AND s1.line = toInteger(row.ligne)
MATCH (s2: Station) WHERE s2.name_clean = row.stop AND s2.line = toInteger(row.ligne)
MERGE (s1)-[:TRAIN {line: toInteger(row.ligne),
                    distance: distance(s1.location, s2.location),
                    time: (distance(s1.location, s2.location) / (40000/60))
                }]->(s2)
'''

with driver.session() as session:
    print(query)
    session.run(query)

print('done')

print('Inserting Walking Relations')

query = '''
MATCH (s1: Station)
MATCH (s2: Station)
WHERE distance(s1.location, s2.location) < 1000 AND
s1.name_clean <> s2.name_clean
MERGE (s1)-[r1:WALKING {distance: distance(s1.location, s2.location),
                        time: (distance(s1.location, s2.location) / (4000/60))
            }]->(s2)
'''

with driver.session() as session:
    print(query)
    session.run(query)

print('done')

print('Inserting Connection Relations')

query = '''
MATCH (s1:Station)
MATCH (s2:Station)
WHERE s1.name_clean = s2.name_clean AND 
s1.line <> s2.line
MERGE (s1)-[:CONNECTION {time:4}]->(s2)
'''

with driver.session() as session:
    print(query)
    session.run(query)

print('done')