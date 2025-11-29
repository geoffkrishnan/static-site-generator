from textnode import TextNode, TextType


def main():
    print(TextNode("test", TextType.LINK, "https://www.boot.dev"))
    print(TextNode("test1", TextType.BOLD, "aoseunhao"))
    print(TextNode("test2", TextType.PLAIN, "aoseunhao"))


if __name__ == "__main__":
    main()
