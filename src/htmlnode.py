class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # will be overridden by child classes to render themselves in HTML
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        props = []
        for prop_key, prop_value in self.props.items():
            props.append(f' {prop_key}="{prop_value}"')
        return " ".join(props)

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode(tag = {self.tag}, value = {self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag = {self.tag}, value = {self.value}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag missing")
        if self.children is None:
            raise ValueError("children missing")
        children = ""
        for node in self.children:
            children += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag = {self.tag}, children={self.children}, props={self.props})"
