class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # will be overridden by child classes to render themselves of HTML
        raise NotImplementedError

    def props_to_html(self):
        props = []
        for prop_key, prop_value in self.props:
            props.append(f'{prop_key}="{prop_value}"')
        return " ".join(props)

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"tag = {self.tag}, value = {self.value}, children={self.children}, props={self.props}"
