def extract_title(markdown):
    if markdown.startswith("## "):
        raise ValueError("Invalid heading")
    if not markdown.startswith("# "):
        raise ValueError("Invalid heading")

    title = markdown.removeprefix("# ")
    return title
