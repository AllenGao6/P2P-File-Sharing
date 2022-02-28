from node import Node


def register_node(node_list, ip_addr, port):
    for node in node_list:
        if node.check_ip(ip_addr):
            return node

    node = Node(ip_addr, port)

    node_list.append(node)
    
    return node



