
def generate_ema(input_data : list, interval : int, x_axis : str, y_axis : str, inplace : bool) -> list:

    data = input_data[:] if not inplace else input_data
    data = sorted(input_data, key=lambda d: d[y_axis])

    def get_ema(interval, prev_ema, curr_value):
            return (2 / (interval + 1)) * (curr_value - prev_ema) + prev_ema

    for idx in range(len(data)):
        prev_ema = data[idx-1].get(f'ema_{interval}')
        prev_ema = prev_ema if prev_ema is not None else data[idx].get(x_axis)
        curr_value = data[idx].get(x_axis)
        data[idx][f'ema_{interval}'] = get_ema(interval, prev_ema, curr_value)

    if not inplace:
        return [{f'ema_{interval}' : el.get(f'ema_{interval}') for el in data}]
    
def generate_ema_signals(input_data: str, y_axis: str, short_ema: str, long_ema: str, signal_name : str, inplace: bool):

    data = input_data[:] if not inplace else input_data
    data = sorted(input_data, key=lambda d: d[y_axis])

    last_signal = ""

    for idx in range(1, len(data)):

        if data[idx-1].get(f'ema_{long_ema}') < data[idx].get(f'ema_{short_ema}') and last_signal != 'Buy':
            data[idx][signal_name], last_signal = "Buy", "Buy"

        if data[idx-1].get(f'ema_{long_ema}') > data[idx].get(f'ema_{short_ema}') and last_signal != 'Sell':
            data[idx][signal_name], last_signal = "Sell", "Sell"

    if not inplace:
        return [{signal_name : el.get(signal_name),  y_axis : el.get(y_axis)} for el in data if el.get(signal_name) is not None]
