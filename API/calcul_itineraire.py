from neo4j import GraphDatabase
import os

# driver = GraphDatabase.driver('bolt://0.0.0.0:7687',
#                               auth=('neo4j', 'neo4j'))
db_api_address = "127.0.0.1"
if (os.environ.get('NEO4J_ADDRESS')):
    db_api_address = os.environ.get('NEO4J_ADDRESS')

driver = GraphDatabase.driver('bolt://{neo4j_address}:7687'.format(neo4j_address=db_api_address),
                              auth=('neo4j', 'neo4j'))

def calcul_itineraire(x_depart, y_depart, x_arrivee, y_arrivee):
    clean_points()
    creation_points_depart_arrivee(x_depart, y_depart, x_arrivee, y_arrivee)
    return calcul_chemin_plus_court()

def calcul_chemin_plus_court():
    query = '''
    MATCH (start:Point {name_station: 'depart'})
    MATCH (end:Point {name_station: 'arrivee'})
    CALL gds.alpha.shortestPath.stream({
    nodeQuery: 'MATCH (n) RETURN id(n) as id',
    relationshipQuery: 'MATCH (n1)-[r]-(n2) RETURN id(r) as id, id(n1) as source, id(n2) as target, r.time as time',
    startNode: start,
    endNode: end,
    relationshipWeightProperty: 'time'
    })
    YIELD nodeId, cost
    RETURN gds.util.asNode(nodeId).name_station AS nom_station, gds.util.asNode(nodeId).line AS ligne, cost AS duree
    '''

    with driver.session() as session:
        result = session.run(query).data()
        return result

def creation_points_depart_arrivee(x_depart, y_depart, x_arrivee, y_arrivee):
    queries = [
    '''
    CREATE (:Point {{location: point({{x: toFloat({x_depart}), y: toFloat({y_depart})}}), name_station: 'depart'}});
    '''.format(x_depart=x_depart, y_depart=y_depart),
    '''
    CREATE (:Point {{location: point({{x: toFloat({x_arrivee}), y: toFloat({y_arrivee})}}), name_station: 'arrivee'}});
    '''.format(x_arrivee=x_arrivee, y_arrivee=y_arrivee),
    '''
    MATCH (p: Point)
    MATCH (s: Station)
    WHERE distance (p.location, s.location) < 1000
    CREATE (p)-[r1:TMP_WALKING {distance: distance(p.location, s.location),
                        time: (distance(p.location, s.location) / (4000/60))
            }]->(s)-[r2:TMP_WALKING {distance: distance(s.location, p.location), time: (distance(s.location, p.location) / (4000/60))
            }]->(p);
    '''
    ]

    with driver.session() as session:
        for q in queries:
            session.run(q)

def clean_points():
    queries = [
    '''
    MATCH ()-[r:TMP_WALKING]-()
    DETACH DELETE(r)
    ''',
    '''
    MATCH (p:Point)
    DETACH DELETE(p);
    '''
    ]

    with driver.session() as session:
        for q in queries:
            session.run(q)

    
#Tests
# départ : BIRHAKEIM
# arrivée : CLUNYLASORBONNE
# x_depart = 647853.8595
# y_depart = 6861779.4605
# x_arrivee = 651882.3097
# y_arrivee = 6861422.9819

# départ : proche BIRHAKEIM
# arrivée : proche CLUNYLASORBONNE
# x_depart = 647850.8595
# y_depart = 6861782.4605
# x_arrivee = 651880.3097
# y_arrivee = 6861425.9819

# calcul_itineraire(x_depart, y_depart, x_arrivee, y_arrivee)