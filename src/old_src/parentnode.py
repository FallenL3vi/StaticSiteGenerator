from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, value = None, props=None):
        super().__init__(tag, value, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Missing Tag Value")
        if not self.children:
            raise ValueError("Missing Chlidren Value")
        new_html_line = ""
        
        for child in self.children:
            new_html_line += child.to_html()
        return f"<{self.tag}>{new_html_line}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode: {self.tag}, {self.children}, {self.value}, {self.props}"