import re
import json
from node import Node, TextNode

# Define regex patterns
patterns = [
    {"pattern": re.compile(r'^(#{1,6})\s+(.*)', re.MULTILINE), "identifier": "header"},
    {"pattern": re.compile(r'^(\*|\-|\+|\d+\.)\s+(.*)', re.MULTILINE), "identifier": "list"},
    {"pattern": re.compile(r'^> ?(.*)', re.MULTILINE), "identifier": "block_quote"},
    {"pattern": re.compile(r'(\*\*(.*?)\*\*)', re.MULTILINE), "identifier": "bold"},
    {"pattern": re.compile(r'\*(.*?)\*', re.MULTILINE), "identifier": "italic"},
    {"pattern": re.compile(r'\[(.*?)\]\((.*?)\)', re.MULTILINE), "identifier": "link"},
    {"pattern": re.compile(r'\n'), "identifier": "new_line"},
]

class MarkdownTokenizer:
    def __init__(self, text):
        self.text = text
        self.ast = Node(node_type="root", children=[])
        self.tokenize(self.text, self.ast)
        self.prettify_ast(self.ast.get_children())
        print(len(self.ast.get_children()))
        self.save_to_file(self.ast, "example.json")

    def tokenize(self, markdown_text, parent_node):
        pos = 0
        text_len = len(markdown_text)
        found_text = ""

        while pos < text_len:
            match, pattern_info = self.find_match(markdown_text, pos)
            if match:
                if found_text:
                    parent_node.add_child(TextNode(found_text.strip()))
                    found_text = ""

                if match.group() == "\n":
                    parent_node.add_child(Node("node-new_line"))
                    pos += 1
                else:
                    self.handle_match(match, pattern_info, parent_node)
                    pos += match.end()
            else:
                found_text += markdown_text[pos]
                pos += 1

        if found_text:
            parent_node.add_child(TextNode(found_text.strip()))

    def find_match(self, text, pos):
        for pattern_info in patterns:
            match = pattern_info["pattern"].match(text[pos:])
            if match:
                return match, pattern_info
        return None, None

    def handle_match(self, match, pattern_info, parent_node):
        n = Node(node_type=f"node-{pattern_info['identifier']}", children=[])
        parent_node.add_child(n)
        self.tokenize(match.group(2) if len(match.groups()) > 1 else match.group(0), n)

    def prettify_ast(self, children, level=0):
        for node in children:
            if isinstance(node, TextNode):
                print(" " * level * 2 + "TextNode:", node.get_content())
            else:
                print(" " * level * 2 + f"Node ({node.type}):")
                self.prettify_ast(node.get_children(), level + 1)

    def save_to_file(self, ast, filename):
        with open(filename, 'w') as f:
            json.dump(ast.to_dict(), f, indent=4)

# Example usage
sec = """
# Header first
something else **other** wow
## other header
- nice **very** cool
[this](http://example.com)
"""

MarkdownTokenizer(sec)