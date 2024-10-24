import hou

def create_node(node_type, name, posx = 0, posy = 0):
    
    obj = hou.node('/obj')
    node = obj.createNode(node_type, name)
    node.setPosition([posx, posy])
    return node
    
def connect_nodes(node_01, node_02):
    
    node_02.setInput(0, node_01)
    
    
null = create_node('null', 'INPUT', 0, 0)
geo = create_node('geo', 'bordel', 0, -2)
connect_nodes(null, geo)


# node layout children