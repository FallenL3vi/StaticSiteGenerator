from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value, props = None, tag = None,):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        else:
            new_prop = ""
            if self.props:
                for prop in self.props:
                    new_prop += f' {prop}="{self.props[prop]}"'

            return f"<{self.tag}{new_prop}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode: {self.tag}, {self.value}, {self.props}"