# expression_engine.py

import ast
import operator as op
from typing import Any, Callable, Dict

import pandas as pd


class SafeExpressionError(Exception):
    """Raised when an expression is invalid or unsafe."""
    pass


class SafeExpressionEvaluator(ast.NodeVisitor):
    """
    Safely evaluate a restricted expression AST using a context dict.

    Supports:
      - Numbers, bools, None
      - Variables (Name) resolved via context
      - Binary ops: +, -, *, /, //, %, ** (if desired), comparisons, &, |, ^
      - Boolean ops: and, or, not
      - Unary ops: +x, -x, not x
      - Function calls for whitelisted helpers only
    """

    # Allowed binary operators
    _bin_ops = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.FloorDiv: op.floordiv,
        ast.Mod: op.mod,
        ast.Pow: op.pow,
        ast.BitAnd: op.and_,
        ast.BitOr: op.or_,
        ast.BitXor: op.xor,
    }

    # Allowed unary operators
    _unary_ops = {
        ast.UAdd: op.pos,
        ast.USub: op.neg,
        ast.Not: op.not_,
    }

    # Allowed comparison operators
    _cmp_ops = {
        ast.Eq: op.eq,
        ast.NotEq: op.ne,
        ast.Gt: op.gt,
        ast.GtE: op.ge,
        ast.Lt: op.lt,
        ast.LtE: op.le,
    }

    def __init__(self, context: Dict[str, Any], functions: Dict[str, Callable]):
        super().__init__()
        self.context = context
        self.functions = functions

    # ---- public API ----

    def eval(self, expr: str) -> Any:
        try:
            node = ast.parse(expr, mode="eval")
        except SyntaxError as e:
            raise SafeExpressionError(f"Syntax error in expression: {expr!r}: {e}") from e
        return self.visit(node.body)

    # ---- visitor methods ----

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id not in self.context:
            raise SafeExpressionError(f"Unknown variable: {node.id}")
        return self.context[node.id]

    def visit_Constant(self, node: ast.Constant) -> Any:
        return node.value

    def visit_Num(self, node: ast.Num) -> Any:  # for older Python ASTs
        return node.n

    def visit_BoolOp(self, node: ast.BoolOp) -> Any:
        if isinstance(node.op, ast.And):
            result = True
            for v in node.values:
                result = result & self.visit(v)
            return result
        elif isinstance(node.op, ast.Or):
            result = False
            for v in node.values:
                result = result | self.visit(v)
            return result
        else:
            raise SafeExpressionError(f"Unsupported boolean operator: {node.op}")

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        op_type = type(node.op)
        if op_type not in self._bin_ops:
            raise SafeExpressionError(f"Unsupported binary operator: {node.op}")
        left = self.visit(node.left)
        right = self.visit(node.right)
        return self._bin_ops[op_type](left, right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        op_type = type(node.op)
        if op_type not in self._unary_ops:
            raise SafeExpressionError(f"Unsupported unary operator: {node.op}")
        operand = self.visit(node.operand)
        return self._unary_ops[op_type](operand)

    def visit_Compare(self, node: ast.Compare) -> Any:
        left = self.visit(node.left)
        result = True
        for op_node, comparator in zip(node.ops, node.comparators):
            right = self.visit(comparator)
            op_type = type(op_node)
            if op_type not in self._cmp_ops:
                raise SafeExpressionError(f"Unsupported comparison operator: {op_node}")
            result = result & self._cmp_ops[op_type](left, right)
            left = right
        return result

    def visit_Call(self, node: ast.Call) -> Any:
        if not isinstance(node.func, ast.Name):
            raise SafeExpressionError("Only simple function calls are allowed.")
        func_name = node.func.id
        if func_name not in self.functions:
            raise SafeExpressionError(f"Function {func_name} is not allowed.")
        func = self.functions[func_name]

        args = [self.visit(a) for a in node.args]
        kwargs = {kw.arg: self.visit(kw.value) for kw in node.keywords}

        return func(*args, **kwargs)

    def generic_visit(self, node: ast.AST) -> Any:
        # Disallow everything else: attributes, subscripts, lambdas, etc.
        raise SafeExpressionError(f"Unsupported expression element: {type(node).__name__}")


# ---- Helper functions for TA-style rules ----

def rising_2bar(series: pd.Series, bars: int = 2) -> pd.Series:
    """
    True where 'series' has been strictly rising for the last `bars` bars.
    Implemented as: series > series.shift(1) > series.shift(2) ...
    """
    result = pd.Series(True, index=series.index)
    prev = series
    for i in range(1, bars + 1):
        shifted = series.shift(i)
        result = result & (prev > shifted)
        prev = shifted
    return result


def falling_2bar(series: pd.Series, bars: int = 2) -> pd.Series:
    """
    True where 'series' has been strictly falling for the last `bars` bars.
    """
    result = pd.Series(True, index=series.index)
    prev = series
    for i in range(1, bars + 1):
        shifted = series.shift(i)
        result = result & (prev < shifted)
        prev = shifted
    return result


class ExpressionEngine:
    """
    High-level wrapper around SafeExpressionEvaluator.

    Usage:
        engine = ExpressionEngine()
        mask = engine.evaluate("RSI_14 > 60 and rising_2bar(RSI_14, 2)", context=df)
    """

    def __init__(self, extra_functions: Dict[str, Callable] | None = None):
        # function calls from 'master_rules_normalized.json'
        base_funcs = {
            "rising_2bar": rising_2bar,
            "falling_2bar": falling_2bar,
            "abs": abs,    
        }

        if extra_functions:
            base_funcs.update(extra_functions)
        self.functions = base_funcs

    def evaluate(self, expression: str, context: Dict[str, Any]) -> Any:
        """
        Evaluate expression in a safe environment.
        `context` is typically a dict mapping variable names → pandas Series or scalars.

        Returns a pandas Series (for vector expressions) or a scalar.
        """
        if expression is None:
            raise SafeExpressionError("Expression is None")
        expression = expression.strip()
        if expression == "":
            raise SafeExpressionError("Empty expression")
        evaluator = SafeExpressionEvaluator(context=context, functions=self.functions)
        return evaluator.eval(expression)