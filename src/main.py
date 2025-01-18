from textnode import TextNode, TextType
from copy_content import clear_public, copy_content, extract_title, generate_page, generate_pages_recursive

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)

    clear_public()
    copy_content()
    generate_pages_recursive("./content", "./template.html", "./public")


main()
