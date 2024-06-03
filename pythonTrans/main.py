import re
import json
from node import Node, TextNode


header_re = re.compile(r'^(#{1,6})\s+(.*)', re.MULTILINE)
list_re = re.compile(r'^(\*|\-|\+|\d+\.)\s+(.*)', re.MULTILINE)
block_quote_re = re.compile(r'^> ?(.*)', re.MULTILINE)

bold_re = re.compile(r'(\*\*(.*?)\*\*)', re.MULTILINE)

italic_re = re.compile(r'\*(.*?)\*', re.MULTILINE)
link_re = re.compile(r'\[(.*?)\]\((.*?)\)', re.MULTILINE)
new_line_re = re.compile(r'\n')
patterns = [
    {"pattern": list_re, "identifier": "list", "is_special": True},
    {"pattern": bold_re, "identifier": "bold", "is_special": False},
    {"pattern": italic_re, "identifier": "italic", "is_special": False},
    {"pattern": link_re, "identifier": "link", "is_special": True},
    {"pattern": block_quote_re, "identifier": "block_quote", "is_special": True},
    {"pattern": header_re, "identifier": "header", "is_special": True},
    {"pattern": new_line_re, "identifier": "new_line", "is_special": False}

]

class MarkdownTokenizer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.ast = Node(node_type="root", childs=[])
        self.tokenize(self.text, self.ast)
        self.prettify_ast(self.ast.get_childs())
        # print("ds", self.ast.get_last_child().get_childs()[1].get_content())
        print(len(self.ast.get_childs()))
        self.save_to_file(self.ast, "example.json")
    
    def tokenize(self, markdown_text, parent_node):
        
        pos = 0
        text_len = len(markdown_text)
        found_text = ""
        # at this point only god understands this code
        while pos < text_len:
            found_match = False
            for pattern_info in patterns:
                match = pattern_info["pattern"].match(string=markdown_text[pos:])
                if match:
                    found_match = True
                    # get prev text
                    if found_text != "":
                        # print("TEXT before match:", found_text.strip())
                        parent_node.add_child(TextNode(found_text.strip()))
                        found_text = ""
                    # print("MATCH:", match)
                    if match.group() == "\n":
                        pos += 1
                        break
                    n = Node(node_type=f"node-{pattern_info['identifier']}", childs=[])
                    parent_node.add_child(n)

                    self.tokenize(match.group(2), n)                    
                    pos += match.end()

                    break
            if not found_match:
                found_text += markdown_text[pos]
                pos += 1
        
        parent_node.add_child(TextNode(found_text))

    def prettify_ast(self, childs, is_from=0):
        for node in childs:
            if isinstance(node, TextNode):
                print("text node with content:", node.get_content(), is_from)
            else:
                self.prettify_ast(node.get_childs(), is_from=is_from+1)

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