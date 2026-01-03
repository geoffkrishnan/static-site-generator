def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
        if line.strip() == "#":
            continue
        if line.startswith("#") and not line.startswith("##"):
            return line[1:].strip()
    raise Exception("No h1 header found in markdown")
