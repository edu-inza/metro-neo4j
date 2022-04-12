//nombre de correspondances par station
MATCH (s1:Station)-[r:CONNECTION]->(s2:Station)
RETURN COUNT(DISTINCT r) AS nb_correspondances, s1.name_station
//-> tableau correspondance, station : par ex: "Arts et Métiers" : 2

//nombre de stations à moins de 2 km de la station `LADEFENSE`
MATCH (s1:Station {name_clean: 'LADEFENSE'})
MATCH (s2:Station)
WHERE distance(s1.location, s2.location) < 2000
RETURN COUNT(DISTINCT s2.name_clean) AS nb_stations
//-> 3

//temps pour aller en métro de `LADEFENSE`à `CHATEAUDEVINCENNES`
MATCH (s1:Station {line:1})-[r:TRAIN {line:1}]->(s2:Station {line:1}) 
RETURN SUM(r.time) as temps_train
//-> 49.4 min : on considère qu'on fait la ligne 1 de terminus à terminus

//temps pour aller à pied de `LADEFENSE`à `CHATEAUDEVINCENNES`
MATCH (s1:Station {name_clean: 'LADEFENSE'})
MATCH (s2:Station {name_clean: 'CHATEAUDEVINCENNES'})
RETURN (distance(s1.location, s2.location) / (4000/60)) as temps_pied
//-> 239.97 min

//est-il plus rapide de faire un changement à `SAINTLAZARE` pour aller de `MONTPARNASSEBIENVENUE` à `GABRIELPERI` ?
//- calcul du chemin le plus court
MATCH (start:Station {name_clean: 'MONTPARNASSEBIENVENUE', line:13})
MATCH (end:Station {name_clean: 'GABRIELPERI'})
CALL gds.alpha.shortestPath.stream({
  nodeQuery: 'MATCH (n) RETURN id(n) as id',
  relationshipQuery: 'MATCH (n1)-[r]->(n2) RETURN id(r) as id, id(n1) as source, id(n2) as target, r.time as time',
  startNode: start,
  endNode: end,
  relationshipWeightProperty: 'time'
})
YIELD nodeId, cost
RETURN gds.util.asNode(nodeId), cost
//-> le plus court chemin = ligne 13 sans changement à St Lazare : 14.63min

//combien de stations se trouvent dans un rayon de 10 stations par train autour de `SAINTLAZARE` ?
MATCH (s1:Station {name_clean: 'STLAZARE'})
MATCH p = (s1)-[:TRAIN *10]->(s2:Station)
RETURN COUNT(DISTINCT s2.name_clean) as nb_stations_10_stations
//-> 36

//combien de stations se trouvent dans un rayon de 20 min par train autour de `SAINTLAZARE` ?
MATCH (s1:Station {name_clean: 'STLAZARE'})
MATCH (s1)-[r:TRAIN]->(s2)
WHERE r.time < 20
RETURN COUNT(s2.name_clean) as nbre_stations_20_min
//-> 7