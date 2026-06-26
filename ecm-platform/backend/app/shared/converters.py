def parse_kwh(value: str) -> float:
    value = value.replace(" kWh", "")
    value = value.replace(" ", "")
    value = value.replace(",", ".")
    return float(value)