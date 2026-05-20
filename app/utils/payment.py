from __future__ import annotations

VALID_PAYMENT_METHODS = frozenset({"cash", "gcash"})


def normalize_payment_method(value: str | None) -> str:
    method = (value or "cash").strip().lower()
    return method if method in VALID_PAYMENT_METHODS else "cash"


def payment_method_label(value: str | None) -> str:
    return "GCash" if normalize_payment_method(value) == "gcash" else "Cash"
