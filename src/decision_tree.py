from enum import Enum
import os
from bigtree import Node, find_full_path
import requests
from src.faq import get_faq_suggestions

#Primer nodo
root = Node("0", text="Bienvenido, por favor seleccione una opción: \n1-Consultar Incidente \n2-Crear Incidente \n3-Preguntas Frecuentes")
#Flujo consulta
node_1 = Node("1", text="Por favor digite el ID del usuario", field="userId", parent=root)
node_1_1 = Node("1", text="Por favor digite el ID del incidente", field="incidentId", parent=node_1)
node_1_1_1 = Node("1", text="Los detalles del incidente son: ", request=True, url_path="/incidents/mobile/search_incident", parent=node_1_1)

node_2 = Node("2", text="Por favor digite el ID del usuario", field="userId,id", parent=root)
node_2_1 = Node("1", text="Usuario ", request=True, field="skip", url_path="/incidents/mobile/get_user", parent=node_2)
#Flujo crear incidente
node_ci_1 = Node("1", text="Por favor seleccione el tipo de incidente  \n1-Peticion \n2-Queja \n3-Reclamo \n4-Sugerencia", field="type", parent=node_2_1)
node_ci_2 = Node("1", text="Por favor escriba una descripción del incidente", field="description", parent=node_ci_1)
node_ci_3 = Node("1", text="Por favor escriba la fecha del incidente ", field="date", parent=node_ci_2)
node_ci_4 = Node("1", text="Por favor escriba el nombre de la empresa ", field="company", parent=node_ci_3)
node_ci_5 = Node("1", text="", request=True, url_path="/incidents/mobile/create_incident", parent=node_ci_4)
#Flujo crear usuario
node_cu_1 = Node("2", text="Por favor escriba su nombre", field="name", parent=node_2_1)
node_cu_2 = Node("1", text="Por favor escriba su numero de teléfono", field="phone", parent=node_cu_1)
node_cu_3 = Node("1", text="Por favor escriba su correo electrónico", field="email", parent=node_cu_2)
node_cu_4 = Node("1", text="Por favor escriba el nombre de la empresa", field="company", parent=node_cu_3)
node_cu_5 = Node("1", text="Resultado de la solicitud: ", request=True, url_path="/incidents/mobile/create_user", parent=node_cu_4)
#Flujo FAQ
node_3 = Node("3", text="Por favor escriba una descripción corta del problema", field="question", parent=root)
node_3_1 = Node("1", text="Recomendaciones basadas en la descripción: \n", faq=True, parent=node_3)

def get_tree_node(node_path: str, json: any):
    if node_path == '':
        return root
    else:
        node = find_full_path(root, node_path)            
        if node is not None:
            message = node.get_attr('text')
            url_path = node.get_attr('url_path')
            req_status = 200
            if node.get_attr('request') == True:
                req_message, req_status = get_api_request(json, url_path)
                message += req_message
            elif node.get_attr('faq') == True:
                message += get_faq_suggestions(json["question"])
            return {
                    'message': message,
                    'field': node.get_attr('field'),
					'is_leaf': node.is_leaf,
                    'error': False,
                    'status': req_status 
                }
        else: 
            return {
                    'message': 'Selección inválida, por favor intente nuevamente',
                    'error': True,
                    'field': None,
					'is_leaf': None
                }

def get_api_request(json: any, url_path: str):
    try:
        url_base = 'http://incidents-microservice:5003'
        if os.getenv('INCIDENTS_API_URL'):
            url_base = os.getenv('INCIDENTS_API_URL')

        url = url_base + url_path

        if "get" in url_path:
            url = url + f"/{json['userId']}"
            response = requests.get(url, json=json)
            if response.status_code == 200:
                return "encontrado", response.status_code
            else:
                return "no encontrado", response.status_code
        else:
            response = requests.post(url, json=json)
            
        if response.status_code == 200 or response.status_code == 201:
            json_response = response.json()

            if 'type' in json_response and 'date' in json_response and 'solved' in json_response:
                solved = json_response.get('solved')
                date = json_response.get('date')
                incident_id = json_response.get('id')
                description = json_response.get('description')
                
                return f"\nID: {incident_id} \nResuelto: {solved} \nFecha: {date}\nDescripcion: {description}", response.status_code

            elif 'id' in json_response and 'name' in json_response and 'phone' in json_response:
                user_id = json_response.get('id')
                name = json_response.get('name')
                phone = json_response.get('phone')
                email = json_response.get('email')
                
                return f"\nUsuario creado: \nID: {user_id} \nNombre: {name} \nTelefono: {phone} \nEmail: {email}", response.status_code

            else:
                return f"Error: Unexpected response format from {url}", response.status_code

        else:
            return f"Error en la respuesta: {response.status_code}, {response.text}", response.status_code
    
    except Exception as e:
        return f"Error en solicitud a {url}, mensaje: {e}", 500

class IncidentType(Enum):
    Peticion = 1
    Queja = 2
    Reclamo = 3
    Sugerencia = 4