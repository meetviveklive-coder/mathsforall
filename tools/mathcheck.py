"""Safe parsing and comparison of maths values for content verification.

Content files are AI-written, so expressions are never passed to a bare eval:
identifiers are checked against a whitelist before SymPy parses them.
"""
from __future__ import annotations

import re

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

ALLOWED_NAMES = {
    # functions
    "Rational": sp.Rational, "sqrt": sp.sqrt, "root": sp.root, "floor": sp.floor,
    "ceiling": sp.ceiling, "Mod": sp.Mod, "gcd": sp.gcd, "lcm": sp.lcm, "Abs": sp.Abs,
    "factorial": sp.factorial, "binomial": sp.binomial, "Min": sp.Min, "Max": sp.Max,
    "round": lambda x, n=0: sp.Float(round(float(x), int(n))) if n else sp.Integer(round(float(x))),
    "isprime": lambda n: sp.true if sp.isprime(int(n)) else sp.false,
    "divisors_count": lambda n: sp.Integer(len(sp.divisors(int(n)))),
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "log": sp.log, "exp": sp.exp,
    # relations / logic
    "Eq": sp.Eq, "Ne": sp.Ne, "Lt": sp.Lt, "Le": sp.Le, "Gt": sp.Gt, "Ge": sp.Ge,
    "And": sp.And, "Or": sp.Or, "Not": sp.Not,
    # constants
    "pi": sp.pi, "E": sp.E, "I": sp.I, "true": sp.true, "false": sp.false,
    "True": sp.true, "False": sp.false,
}
# Single-letter symbols allowed for algebra stages.
SYMBOLS = {c: sp.Symbol(c) for c in "abcdmnpqrstuvwxyz"}

_IDENT = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
_ALLOWED_CHARS = re.compile(r"^[0-9A-Za-z_+\-*/^().,%<>=!&| \t]*$")
_TRANSFORMS = standard_transformations + (convert_xor,)


class UnsafeExpression(ValueError):
    pass


def _check_safe(text: str) -> None:
    if not _ALLOWED_CHARS.match(text):
        raise UnsafeExpression(f"disallowed characters in {text!r}")
    if "__" in text or "lambda" in text:
        raise UnsafeExpression(f"disallowed token in {text!r}")
    for name in _IDENT.findall(text):
        if name not in ALLOWED_NAMES and name not in SYMBOLS:
            raise UnsafeExpression(f"unknown name {name!r} in {text!r}")


def _clean_value(text: str) -> str:
    """Normalise a learner-style answer: '₹1,25,000' -> '125000', '50 %' -> '50/100'."""
    t = text.strip()
    t = t.replace("₹", "").replace("Rs.", "").replace("Rs", "")
    t = t.replace("×", "*").replace("÷", "/").replace("−", "-")
    # Indian or international digit grouping ('1,25,000'): strip commas only when the
    # whole value is a plain number, so function arguments like gcd(12,18) are untouched.
    if re.fullmatch(r"-?\d[\d,]*(\.\d+)?", t):
        t = t.replace(",", "")
    t = re.sub(r"(\d+(?:\.\d+)?)\s*%", r"(\1/100)", t)
    # mixed number '2 1/2' -> '(2+1/2)'
    t = re.sub(r"^(\d+)\s+(\d+)/(\d+)$", r"(\1+\2/\3)", t)
    return t.strip()


def parse(text: str) -> sp.Basic:
    cleaned = _clean_value(text)
    _check_safe(cleaned)
    local = {**ALLOWED_NAMES, **SYMBOLS}
    # Safe because _check_safe has already rejected every identifier not in the whitelist.
    expr = parse_expr(cleaned, local_dict=local, transformations=_TRANSFORMS, evaluate=True)
    if isinstance(expr, sp.Basic):
        return sp.nsimplify(expr, rational=True) if expr.has(sp.Float) else expr
    if isinstance(expr, bool):
        return sp.true if expr else sp.false
    return sp.sympify(expr)


def equal(a: sp.Basic, b: sp.Basic) -> bool:
    if isinstance(a, sp.logic.boolalg.Boolean) or isinstance(b, sp.logic.boolalg.Boolean):
        return bool(a == b)
    try:
        diff = sp.simplify(a - b)
        return diff == 0
    except TypeError:
        return a == b


def as_bool(value: sp.Basic) -> bool | None:
    if value in (sp.true, True):
        return True
    if value in (sp.false, False):
        return False
    return None
