from bigtree import Node, find_full_path

#Primer nodo
root = Node("0", text="Bienvenido, por favor seleccione una opcion: \n1-Crear \n2-Consultar")
#Flujo consulta
node_1 = Node("1", text="Por favor digite su numero de identificacion", field="user_id", parent=root)
node_1_1 = Node("1_1", text="Por favor digite el ID del incidente", field="incident_id", parent=node_1)

def get_tree_node(node_path: str):
    if node_path == '':
        return root
    else:
        node = find_full_path(root, node_path)
        if node is not None:
            return {
                    'message': node.get_attr('text'),
                    'field': node.get_attr('field'),
					'is_leaf': node.is_leaf
                }