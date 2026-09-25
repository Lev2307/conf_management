import json

dotLines = []
seen = set()

def walk_through_tree(name: str, node):
    for dep_name, dep in (node.get("dependencies") or {}).items():
        dotLines.append(f' "{name}" -> "{dep_name}";')
        key = (name, dep_name)
        if key in seen:
            continue
        seen.add(key)
        walk_through_tree(dep_name, dep)

def main():
    data = json.load(open("initExpressDep.json", encoding="utf-8"))
    walk_through_tree("express", data["dependencies"]["express"])

    with open("express.dot", "w", encoding="utf-8") as f:
        f.write("digraph deps {\n  rankdir=LR;\n  node [shape=box];\n")
        f.write("\n".join(sorted(set(dotLines))))
        f.write("\n}\n")

if __name__ == "__main__":
    main()