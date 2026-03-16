from typing import Tuple, Optional

wildfire_risks = (
    (25, "low"),
    (50, "moderate"),
    (75, "high"),
    (100, "very high"),
)

def calculate_risk_percentage(temp: float, moist: bool) -> float:
    temp_factor = calculate_temp_factor(temp)
    moist_factor = calculate_moist_factor(moist)

    risk = round(temp_factor * moist_factor * 100, 2)
    return risk


def calculate_wildfire_risk(temp: float, moist: bool) -> Tuple[str, float]:
    risk_perc = calculate_risk_percentage(temp, moist)
    risk_mes = determine_risk_level(risk_perc)

    return risk_mes, risk_perc


def determine_risk_level(risk_perc: float) -> Optional[str]:
    if not (0 <= risk_perc <= 100):
        raise ValueError(f"Risk percentages is a value between 0 to 100, cannot be {risk_perc}")

    for val, mes in wildfire_risks:
        if risk_perc <= val:
            return mes
    raise


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
