from decimal import Decimal, InvalidOperation
from typing import Any, List, Optional, Tuple


def parse_decimal(
    value: Optional[str],
    field_name: str,
    errors: List[str],
) -> Optional[Decimal]:
    """Parse a form value into Decimal and append user-friendly errors when invalid."""
    if value is None or value.strip() == "":
        errors.append(f"{field_name} wajib diisi.")
        return None

    try:
        parsed_value = Decimal(value)
    except (InvalidOperation, ValueError):
        errors.append(f"{field_name} harus berupa angka.")
        return None

    if not parsed_value.is_finite():
        errors.append(f"{field_name} harus berupa angka yang valid.")
        return None

    return parsed_value


def validate_full_mode(form: Any) -> Tuple[List[str], Optional[Decimal]]:
    """
    Validate Full Mode input and return calculated CRO when valid.

    Rules:
    - Kas must be numeric and >= 0
    - Setara Kas must be numeric and >= 0
    - Total Aset must be numeric and > 0
    - Kas + Setara Kas must be <= Total Aset
    """
    errors: List[str] = []

    cash = parse_decimal(form.get("cash"), "Kas", errors)
    cash_equivalents = parse_decimal(form.get("cash_equivalents"), "Setara Kas", errors)
    total_assets = parse_decimal(form.get("total_assets"), "Total Aset", errors)

    if cash is not None and cash < 0:
        errors.append("Kas harus lebih dari atau sama dengan 0.")

    if cash_equivalents is not None and cash_equivalents < 0:
        errors.append("Setara Kas harus lebih dari atau sama dengan 0.")

    if total_assets is not None and total_assets <= 0:
        errors.append(
            "Total Aset harus lebih dari 0 untuk mencegah pembagian dengan nol."
        )

    if cash is not None and cash_equivalents is not None and total_assets is not None:
        if cash + cash_equivalents > total_assets:
            errors.append(
                "Total Kas + Setara Kas harus kurang dari atau sama dengan Total Aset."
            )

    if errors:
        return errors, None

    if cash is None or cash_equivalents is None or total_assets is None:
        return ["Semua input Full Mode harus valid sebelum perhitungan CRO."], None

    cro = (cash + cash_equivalents) / total_assets
    return errors, cro


def validate_simple_mode(form: Any) -> Tuple[List[str], Optional[Decimal]]:
    """
    Validate Simple Mode input and return CRO when valid.

    Rules:
    - CRO must be numeric
    - CRO must be between 0 and 1
    """
    errors: List[str] = []

    cro = parse_decimal(form.get("cro"), "CRO", errors)

    if cro is not None and (cro < 0 or cro > 1):
        errors.append("CRO harus berada dalam rentang 0 sampai 1.")

    if errors:
        return errors, None

    if cro is None:
        return ["CRO harus valid sebelum prediksi."], None

    return errors, cro
