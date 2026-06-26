def parse_kwh(value: str) -> float:
    value = value.replace(" kWh", "")
    value = value.replace(" ", "")
    value = value.replace(",", ".")
    return float(value)


def parse_kw(value: str) -> float:
    value = value.replace(" kW", "")
    value = value.replace(" ", "")
    value = value.replace(",", ".")
    return float(value)