from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return f"{self.value}"
        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
