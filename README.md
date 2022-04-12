# Introduction
Ce projet met en place une base de données orientée graphe (Neo4J) pour modéliser le métro de Paris.

# Déploiement de la solution
Exécuter le fichier `setup.sh` en paramétrant, si besoin, l'adresse IP du conteneur Neo4J dans le sous-réseau créé par le docker compose.

Le docker compose crée 2 conteneurs :
- un pour la base Neo4J
- un pour l'api avec un endpoint pour calculer l'itinéraire le plus court entre 2 points géographiques

# Description
- Fichier `setup.sh` pour lancer les conteneurs et insérer les données dans Neo4J
- Fichier `docker-compose.yml`, utilisé dans le setup.sh, pour lancer les conteneurs de base de données et d'API
- Fichier `requirements.txt` : modules Python nécessaires pour exécuter le script d'insertion de données (`load_data_into_neo4j`)
- Fichier `exploration_graphe.cypher`: scripts pour explorer le graphe
- Dossier `Neo4j` : script Python et script Cypher pour insérer les données dans la base Neo4J
- Dossier `API`: script pour la fonction de calcul de l'itinéraire le plus court et script pour les endpoints de l'API. L'API peut être déployé via un conteneur docker (cf Dockerfile pour l'image du conteneur).

Tester l'API sur le swagger : http://127.0.0.1:8000/docs
Tester l'insertion des données dans Neo4J : http://127.0.0.1:7474/