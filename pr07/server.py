#!/usr/bin/env python3
"""FIFO server for simple arithmetic expressions; one request at a time."""
import ast
import operator
import os
from pathlib import Path

BASE = Path("/tmp/os_pr07")
REQUEST_FIFO = BASE / "requests.fifo"
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
       ast.Mod: operator.mod, ast.Pow: operator.pow,
       ast.USub: operator.neg, ast.UAdd: operator.pos}

def safe_eval(expression):
    tree = ast.parse(expression, mode="eval")
    def visit(node):
        if isinstance(node, ast.Expression): return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float): return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 8: raise ValueError("exponent too large")
            value = OPS[type(node.op)](left, right)
            if abs(value) > 10**100: raise ValueError("result too large")
            return value
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS: return OPS[type(node.op)](visit(node.operand))
        raise ValueError("only arithmetic numbers and operators are allowed")
    return visit(tree)

def main():
    BASE.mkdir(mode=0o700, parents=True, exist_ok=True)
    if REQUEST_FIFO.exists() and not REQUEST_FIFO.is_fifo(): REQUEST_FIFO.unlink()
    if not REQUEST_FIFO.exists(): os.mkfifo(REQUEST_FIFO, 0o600)
    print(f"FIFO server ready: {REQUEST_FIFO}", flush=True)
    print("Stop with Ctrl+C.", flush=True)
    while True:
        with REQUEST_FIFO.open("r", encoding="utf-8") as stream:
            for line in stream:
                line = line.strip()
                if not line: continue
                try:
                    client_id, expression = line.split("|", 1)
                    reply_fifo = BASE / f"reply_{client_id}.fifo"
                    result = safe_eval(expression)
                    answer = f"OK|{result}\n"
                except Exception as exc:
                    try: reply_fifo = BASE / f"reply_{client_id}.fifo"
                    except UnboundLocalError: continue
                    answer = f"ERROR|{exc}\n"
                try:
                    with reply_fifo.open("w", encoding="utf-8") as out: out.write(answer)
                except OSError as exc:
                    print(f"Could not reply: {exc}", flush=True)
                print(f"{client_id}: {expression} -> {answer.strip()}", flush=True)

if __name__ == "__main__":
    main()
