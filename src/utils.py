def precisionRound(number:float, decimalPlaces:int, base:float):
    return round(base * round(number/base),decimalPlaces)