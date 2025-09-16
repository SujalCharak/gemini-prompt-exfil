#!/usr/bin/env python3
import sys, json, pathlib
docs = list(pathlib.Path("staging/rag_docs").glob("*.txt"))
def top_k(query, k=1):
    if not docs:
        return []
    text = docs[0].read_text()
    return [{"id":"doc-001","score":0.99,"text":text}]
if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv)>1 else ""
    print(json.dumps(top_k(q)))
