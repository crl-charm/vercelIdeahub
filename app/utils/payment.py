from __future__ import annotations

VALID_PAYMENT_METHODS = frozenset({"cash", "gcash", "bdo", "bpi"})


def normalize_payment_method(value: str | None) -> str:
    method = (value or "cash").strip().lower()
    return method if method in VALID_PAYMENT_METHODS else "cash"


def payment_method_label(value: str | None) -> str:
    method = normalize_payment_method(value)
    if method == "gcash":
        return "GCash"
    elif method == "bdo":
        return "BDO"
    elif method == "bpi":
        return "BPI"
    return "Cash"
