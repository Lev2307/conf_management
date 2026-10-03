def parse(line):
    parts = line.split()
    return (None, []) if not parts else (parts[0], parts[1:])