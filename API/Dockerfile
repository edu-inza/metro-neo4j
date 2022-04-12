FROM ubuntu:latest
ADD requirements.txt calcul_itineraire.py subway_route_api.py ./
RUN apt-get update && apt-get install python3-pip -y && pip install -r requirements.txt
ENV NEO4J_ADDRESS='127.0.0.1'
EXPOSE 8000
CMD uvicorn subway_route_api:app --host 0.0.0.0