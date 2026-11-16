"""Sestavi index.html z template.html a data.json."""
import json
d = json.dumps(json.load(open("data.json")), ensure_ascii=False)
open("index.html", "w").write(open("template.html").read().replace("__DATA__", d))
