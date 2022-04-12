# build API docker image
cd $PWD/API
docker image build . -t route_api:1.0.0

# start docker containers
docker-compose up -d

# install requirements to insert data in Neo4J
pip install -r requirements.txt

# insert data in Neo4j
NEO4J_ADDRESS='subway_routes_neo4j'
python3 $PWD/Neo4j/load_data_into_neo4j.py