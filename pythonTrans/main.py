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
    {"pattern": re.compile(r'\n\n'), "identifier": "empty_line"},
    {"pattern": re.compile(r'\n'), "identifier": "new_line"}
]

class MarkdownTokenizer:
    def __init__(self, text=None, read_from_file=False):
        self.text = text
        self.ast = Node(node_type="root", children=[])
        if read_from_file:
            self.text = self.read_markdown_file(read_from_file)

        self.tokenize(self.text, self.ast)

        self.prettify_ast(self.ast.get_children())

        print("Ast children: ", len(self.ast.get_children()))
        self.save_to_file(self.ast, "example.json")

    def tokenize(self, markdown_text, parent_node):
        pos = 0
        text_len = len(markdown_text)
        found_text = ""

        while pos < text_len:
            match, pattern_info = self.find_match(markdown_text, pos)
            if not match:
                found_text += markdown_text[pos]
                pos += 1
                continue
            
            if found_text:
                parent_node.add_child(TextNode(found_text))
                found_text = ""

            self.handle_match(match, pattern_info, parent_node)
            pos += match.end()

        if found_text:
            parent_node.add_child(TextNode(found_text))

    def find_match(self, text, pos):
        for pattern_info in patterns:
            match = pattern_info["pattern"].match(text[pos:])
            if match:
                return match, pattern_info
        return None, None

    def handle_match(self, match, pattern_info, parent_node):
        n = Node(node_type=f"node-{pattern_info['identifier']}", children=[])
        parent_node.add_child(n)
        if pattern_info['identifier'] not in ["empty_line", "new_line"]:
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

    def read_markdown_file(self, filename):
        with open(filename, 'r') as file:
            return file.read(1024)

if __name__ == "__main__":
    MarkdownTokenizer(read_from_file="example.md")

