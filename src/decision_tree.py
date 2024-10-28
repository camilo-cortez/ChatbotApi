from enum import Enum
import os
import random
from bigtree import Node, find_full_path
import faker
from flask import jsonify
import requests

#Primer nodo
root = Node("0", text="Bienvenido, por favor seleccione una opcion: \n1-Consultar \n2-Crear")
#Flujo consulta
node_1 = Node("1", text="Por favor digite su numero de identificacion", field="user_id", parent=root)
node_1_1 = Node("1", text="Por favor digite el ID del incidente", field="incident_id", parent=node_1)
node_1_1_1 = Node("1", text="Los detalles del incidente son: ", request=True, parent=node_1_1)

def get_tree_node(node_path: str, user_id: str, incident_id: str):
    if node_path == '':
        return root
    else:
        node = find_full_path(root, node_path)            
        if node is not None:
            message = node.get_attr('text')
            if node.get_attr('request') == True:
                message += get_api_request(user_id, incident_id)
            return {
                    'message': message,
                    'field': node.get_attr('field'),
					'is_leaf': node.is_leaf,
                    'error': False
                }
        else: 
            return {
                    'message': 'Selección inválida, por favor intente nuevamente',
                    'error': True,
                    'field': None,
					'is_leaf': None
                }

def get_api_request(user_id: str, incident_id: str):
    
    url = os.getenv('INCIDENTS_API_URL')
    data = {
        "user_id": user_id,
        "incident_id": incident_id
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        json_response = response.json()
        incident_type = json_response.get('type')
        date = json_response.get('date') 
        channel = json_response.get('channel') 
        description = json_response.get('description')
        
        return jsonify({
            "Tipo": incident_type,
            "Fecha": date,
            "Canal": channel,
            "Descripcion": description
        })
    
    #If api not working, return mock values
    incident_type = random.choice(list(IncidentType)).name
    incident_description = faker.Faker().text(max_nb_chars=150)
    incident_date = faker.Faker().date_this_year()
    return f"\nTipo: {incident_type}, \nFecha: {incident_date}, \nDescripcion: {incident_description}"

class IncidentType(Enum):
    Peticion = 1
    Queja = 2
    Reclamo = 3
    Sugerencia = 4