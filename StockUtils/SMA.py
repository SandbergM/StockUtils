
def generate_sma(input_data: list, interval: int, x_axis: str, y_axis: str, inplace: bool) -> list:

    data = input_data[:] if not inplace else input_data
    data = sorted(input_data, key=lambda d: d[y_axis])

    def get_sma(values):
        return 0 if sum(values) == 0 or len(values) == 0 else sum(values) / len(values)

    for idx in range(len(data)):
        data[idx][f'sma_{interval}'] = get_sma([el.get(x_axis) for el in data[idx-interval:idx]])

    if not inplace:
        return data