class Node:
    def __init__(self, node_type, childs=[], content=None):
        self.childs = childs
        self.type = node_type
        self.content = content

    def add_child(self, node):
        self.childs.append(node)
        return
    
    def get_childs(self):
        return self.childs
    
    def get_last_child(self):
        return self.childs[-1]

    def to_dict(self):
        return {
            'type': self.type,
            'content': self.content,
            'childs': [child.to_dict() if isinstance(child, Node) else {'type': 'TextNode', 'content': child.get_content()} for child in self.childs]
        }
    
class TextNode:
    def __init__(self, content):
        self.content = content

    def get_content(self):
        return self.content
    
    def set_content(self, new_content):
        self.content = new_content

    def to_dict(self):
        return {
            'type': 'TextNode',
            'content': self.content
        }

    