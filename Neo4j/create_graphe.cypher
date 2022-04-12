// Création des noeuds = stations
LOAD CSV WITH HEADERS FROM 'https://github.com/pauldechorgnat/cool-datasets/raw/master/ratp/stations.csv' AS row
CREATE (:Station {name_clean: row.nom_clean, 
                    name_station:row.nom_gare, 
                    location: point({x:toFloat(row.x), y:toFloat(row.y)}),
                    traffic: toInteger(row.Trafic), 
                    city: row.Ville,
                    line: toInteger(row.ligne)
});

// Création des liaisons train
LOAD CSV WITH HEADERS FROM 'https://github.com/pauldechorgnat/cool-datasets/raw/master/ratp/liaisons.csv' AS row
MATCH (s1: Station) WHERE s1.name_clean = row.start AND s1.line = toInteger(row.ligne)
MATCH (s2: Station) WHERE s2.name_clean = row.stop AND s2.line = toInteger(row.ligne)
MERGE (s1)-[:TRAIN {line: toInteger(row.ligne),
                    distance: distance(s1.location, s2.location),
                    time: (distance(s1.location, s2.location) / (40000/60))
                }]->(s2)

// Création des liaisons pied
MATCH (s1: Station)
MATCH (s2: Station)
WHERE distance(s1.location, s2.location) < 1000 AND
s1.name_clean <> s2.name_clean
MERGE (s1)-[r1:WALKING {distance: distance(s1.location, s2.location),
                        time: (distance(s1.location, s2.location) / (4000/60))
            }]->(s2)

// Création des correspondances
MATCH (s1:Station)
MATCH (s2:Station)
WHERE s1.name_clean = s2.name_clean AND 
s1.line <> s2.line
MERGE (s1)-[:CONNECTION {time:4}]->(s2)