def write_log(text, filename):
    with open(filename, "a") as f:
        f.write(text + "\n")