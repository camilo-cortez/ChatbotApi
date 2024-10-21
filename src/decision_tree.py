from enum import Enum
import random
from bigtree import Node, find_full_path
import faker

#Primer nodo
root = Node("0", text="Bienvenido, por favor seleccione una opcion: \n1-Consultar \n2-Crear")
#Flujo consulta
node_1 = Node("1", text="Por favor digite su numero de identificacion", field="user_id", parent=root)
node_1_1 = Node("1", text="Por favor digite el ID del incidente", field="incident_id", parent=node_1)
node_1_1_1 = Node("1", text="Los detalles del incidente son: ", request=True, parent=node_1_1)

def get_tree_node(node_path: str):
    if node_path == '':
        return root
    else:
        node = find_full_path(root, node_path)            
        if node is not None:
            message = node.get_attr('text')
            if node.get_attr('request') == True:
                message += get_api_request()
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

def get_api_request():
    incident_type = random.choice(list(IncidentType)).name
    incident_description = faker.Faker().text(max_nb_chars=150)
    incident_date = faker.Faker().date_this_year()
    return f"\nTipo: {incident_type}, \nFecha: {incident_date}, \nDescripcion: {incident_description}"

class IncidentType(Enum):
    Peticion = 1
    Queja = 2
    Reclamo = 3
    Sugerencia = 4