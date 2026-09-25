packages = {
    "root": {
        "1.0.0": {"foo": "^1.0.0", "target": "^2.0.0"},
    },
    "foo": {
        "1.1.0": {"left": "^1.0.0", "right": "^1.0.0"},
        "1.0.0": {},
    },
    "left": {
        "1.0.0": {"shared": ">=1.0.0"},
    },
    "right": {
        "1.0.0": {"shared": "<2.0.0"},
    },
    "shared": {
        "2.0.0": {},
        "1.0.0": {"target": "^1.0.0"},
    },
    "target": {
        "2.0.0": {},
        "1.0.0": {},
    },
}

def parse(v):
    return tuple(int(x) for x in v.split("."))

def matches(v: str, spec: str) -> bool:
    vc = parse(v)
    if spec.startswith("^"):
        vspec = parse(spec[1:])
        return vc[0] == vspec[0] and vc >= vspec
    elif spec.startswith(">="):
        return vc >= parse(spec[2:])
    elif spec.startswith("<="):
        return vc <= parse(spec[2:])
    elif spec.startswith(">"):
        return vc > parse(spec[1:])
    elif spec.startswith("<"):
        return vc < parse(spec[1:])
    else:
        return vc == parse(spec)
    
def main():
    lines = []
    versions = dict()
    for package, v in packages.items():
        if not versions.get(package):
            keys = list(v.keys())
            versions[package] = sorted(keys, key=parse)
    for pckg, v in versions.items():
        if pckg != "root":
            lines.append(f"var 0..{len(v)}: {pckg};")

    root = versions.get("root", "")
    if root:
        rootP = packages.get("root").get("1.0.0")
        for name, v in rootP.items():
            idx = [0 for _ in range(len(versions.get(name))+1)]
            for i, vers in enumerate(versions.get(name)):
                if matches(vers, v):
                    idx[i+1] = 1
            sIDX = []
            for j in range(len(idx)):
                if idx[j] == 1:
                    sIDX.append(j)
            sIDX = ", ".join([str(i) for i in sIDX])
            lines.append(f"constraint {name} in {{{sIDX}}};")

    for pkg, vers in packages.items():        # pkg = "foo", vers = {"1.1.0": {...}, "1.0.0": {}}
        if pkg == "root":
            continue
        for ver, deps in vers.items():        # ver = "1.1.0", deps = {"left": "^1.0.0", "right": "^1.0.0"}
            for dep_name, spec in deps.items():   # dep_name = "left", spec = "^1.0.0"
                keyIDX = versions[pkg].index(ver) + 1
                idx = [0 for _ in range(len(versions.get(dep_name))+1)]
                for i, vv in enumerate(versions.get(dep_name)):
                    if matches(vv, spec):
                        idx[i+1] = 1
                sIDX = []
                for j in range(len(idx)):
                    if idx[j] == 1:
                        sIDX.append(j)
                sIDX = ", ".join([str(i) for i in sIDX])
                lines.append(f"constraint {pkg} = {keyIDX} -> ({dep_name} in {{{sIDX}}});")

    lines.append("solve maximize foo;")
    with open("model.mzn", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
if __name__ == "__main__":
    main()