from typing import Tuple

wildfire_risks = (
    (25, "low"),
    (50, "moderate"),
    (75, "high"),
    (100, "very high"),
)

def calculate_wildfire_risk(temp: float, moist: bool) -> Tuple[str, float]:
    temp_factor = calculate_temp_factor(temp)
    moist_factor = calculate_moist_factor(moist)

    risk = round(temp_factor * moist_factor * 100, 2)
    risk_mes = ""
    for val, mes in wildfire_risks:
        if risk <= val:
            risk_mes = mes
            break

    return risk_mes, risk


def calculate_temp_factor(temp: float) -> float:
    factor = (temp - 10) / 30
    if factor < 0:
        factor = 0
    elif factor > 1:
        factor = 1

    return factor


def calculate_moist_factor(moist: bool) -> float:
    factor = 1
    if moist:
        factor = 0.6
    return factor


if __name__ == "__main__":
    data = [val for val in input().strip().split()]
    out = calculate_wildfire_risk(float(data[0]), bool(data[1]))
    print(*data)
    print(out)
