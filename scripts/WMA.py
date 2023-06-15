
def generate_wma(input_data: list, interval: int, x_axis: str, y_axis: str, inplace: bool) -> list:

    data = input_data[:] if not inplace else input_data
    data = sorted(input_data, key=lambda d: d[y_axis])

    def __get_wma(values):

        if len(values) == 0:
            return None

        weight = 1
        weighted_sum = 0
        weight_factor = sum([idx + 1 for idx in range(len(values))])

        for val in values:
            weighted_sum = (weighted_sum+(float(val)*(weight/weight_factor)))
            weight += 1

        return weighted_sum

    for idx in range(len(data)):
        data[idx][f'wma_{interval}'] = __get_wma([el.get(x_axis) for el in data[(idx-interval):idx]])

    if not inplace:
        return [{f'wma_{interval}' : el.get(f'wma_{interval}')} for el in data]
