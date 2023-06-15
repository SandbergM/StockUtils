
def generate_rsi(input_data: list, interval: int, x_axis: str, y_axis: str, inplace: bool) -> list:

    data = input_data[:] if not inplace else input_data
    data = sorted(input_data, key=lambda d: d[y_axis])

    def get_rsi(values):

        loss, gain = 1, 1

        for idx in range(1, len(values), 1):
            prev, curr = values[idx-1], values[idx]
            gain += (curr - prev) if curr > prev else 0
            loss += (prev - curr) if curr < prev else 0

        return 100 - (100 / (1 + (gain / len(data)) / (loss / len(data))))

    for idx in range(len(data)):
        data[idx][f'rsi_{interval}'] = get_rsi(
            [el.get(x_axis) for el in data[(idx-interval):idx]])

    if not inplace:
        return [{f'rsi_{interval}' : el.get(f'rsi_{interval}') } for el in data]