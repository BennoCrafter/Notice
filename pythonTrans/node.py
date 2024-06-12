class Node:
    def __init__(self, node_type, span=None, children=[] ):
        self.children = children
        self.type = node_type
        self.span = span

    def add_child(self, node):
        self.children.append(node)
        return
    
    def get_children(self):
        return self.children
    
    def get_last_child(self):
        return self.children[-1]

    def to_dict(self):
        return {
            'type': self.type,
            'children': [children.to_dict() if isinstance(children, Node) else {'type': 'TextNode', 'content': children.get_content()} for children in self.children],
            'span': self.span
        }
    
class TextNode(Node):
    def __init__(self, content, span):
        super().__init__(node_type='TextNode')
        self.content = content
        self.span = span

        
    def get_content(self):
        return self.content
    
    def set_content(self, new_content):
        self.content = new_content

    def to_dict(self):
        return {
            'type': 'TextNode',
            'content': self.content,
            'span': self.span
        }

    