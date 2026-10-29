"""Explicit numeric checks: arithmetic only, no theorem or hardware verification."""
from decimal import Decimal, InvalidOperation, localcontext
from math import gcd


def check_arithmetic(checks):
    with localcontext() as ctx:
        ctx.prec = 256
        return _run_checks(checks)


def _run_checks(checks):
    """Evaluate submitted numeric assertions without parsing free-form mathematics."""
    results = []
    for item in checks:
        cid = item.get("id", "")
        op = item.get("operation")
        try:
            values = item["values"]
            if not isinstance(values, list) or not 2 <= len(values) <= 64:
                raise ValueError("expected 2..64 values")
            if any(isinstance(v, bool) or not isinstance(v, (int, str)) or len(str(v)) > 70 for v in values):
                raise ValueError("values must be bounded decimal integers/strings")
            if op == "pairwise_coprime":
                numbers = [int(v) for v in values]
                if any(str(v).strip().lstrip("-").isdigit() is False for v in values):
                    raise ValueError("coprime requires integers")
                calculated = all(gcd(a, b) == 1 for i, a in enumerate(numbers) for b in numbers[i+1:])
                if type(item.get("expected")) is not bool:
                    raise ValueError("expected must be boolean")
                passed = calculated is item["expected"]
            else:
                numbers = [Decimal(str(v)) for v in values]
                if any(not x.is_finite() for x in numbers):
                    raise ValueError("non-finite number")
                if op == "sum":
                    calculated = sum(numbers, Decimal(0))
                elif op == "product":
                    calculated = Decimal(1)
                    for n in numbers:
                        calculated *= n
                elif op == "difference" and len(numbers) == 2:
                    calculated = numbers[0] - numbers[1]
                else:
                    raise ValueError("unsupported operation")
                expected = Decimal(str(item["expected"]))
                passed = calculated == expected
                calculated = str(calculated)
            results.append({"id": cid, "operation": op, "status": "match" if passed else "mismatch",
                            "computed": calculated, "arithmetic_only": True})
        except (KeyError, TypeError, ValueError, InvalidOperation, OverflowError, ArithmeticError) as exc:
            results.append({"id": cid, "operation": op, "status": "not_evaluated",
                            "reason": type(exc).__name__, "arithmetic_only": True})
    return {"scope": "supplied-literal arithmetic only", "results": results}
