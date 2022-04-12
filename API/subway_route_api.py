from fastapi import FastAPI
import json
from calcul_itineraire import calcul_itineraire

app = FastAPI(title="Subway Route API",
                description="API to process the shortest route in the subway of Paris")

@app.get('/status')
async def get_status():
    '''Returns api status : 1 --> api running correctly'''
    return 1

@app.get('/shortest_route')
async def get_shortest_route(x_start: float, y_start: float, x_end: float, y_end: float):
    '''Returns the shortest route from point1 to point 2, in the subway of Paris'''
    return json.dumps(calcul_itineraire(x_start, y_start, x_end, y_end))