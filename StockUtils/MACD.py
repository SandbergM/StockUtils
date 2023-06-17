from .EMA import generate_ema

def generate_macd(input_data: list, short_interval: int,  long_interval: int, x_axis: str, y_axis: str, inplace: bool ) -> list :

    data = input_data[:] if not inplace else input_data
    data = sorted(input_data, key=lambda d: d[y_axis])

    ema_short = generate_ema(data, short_interval, x_axis, y_axis, False)
    ema_long  = generate_ema(data, long_interval, x_axis, y_axis, False)

    for idx in range(len(data)):
        
        data[idx]['macd'] = ema_short[idx].get(f'ema_{short_interval}') - ema_long[idx].get(f'ema_{long_interval}')
        
    ema_9 = generate_ema(data, 9, x_axis='macd', y_axis='date', inplace=False)

    for idx, el in enumerate(ema_9):
        data[idx]['macd_s'] = el.get('ema_9')
        data[idx]['macd_h'] = data[idx]['macd'] - el.get('ema_9')

    if not inplace:
        return [{
            'macd'      : el.get('macd'),
            'macd_s'    : el.get('macd_s'),
            'macd_h'    : el.get('macd_h'),
            y_axis      : el.get(y_axis),
        } for el in data]
    
def get_macd_signals(input_data: str, y_axis: str, inplace: bool):

    data = input_data[:] if not inplace else input_data
    data = sorted(input_data, key=lambda d: d[y_axis])
    data = data[::-1]

    sell_days_in_a_row = 0
    buy_days_in_a_row = 0

    for idx in range(len(data)):

        if data[idx].get('macd') < data[idx].get('macd_s') and data[idx].get('macd_h') < 0:
            if sell_days_in_a_row == 0:
                data[idx]['macd_signal'] = "Sell"
            sell_days_in_a_row = sell_days_in_a_row + 1 if sell_days_in_a_row < 5 else 0

        if data[idx].get('macd') > data[idx].get('macd_s') and data[idx].get('macd_h') > 0:
            if buy_days_in_a_row == 0:
                data[idx]['macd_signal'] = "Buy"

            buy_days_in_a_row = buy_days_in_a_row + 1 if buy_days_in_a_row < 5 else 0

    if not inplace:
        return [{'macd_signal' : el.get('macd'), y_axis : el.get('y_axis')} for el in data[::-1] if el.get('macd') is not None]

    else:
        data = data[::-1]