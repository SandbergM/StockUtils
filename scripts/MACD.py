from .EMA import generate_ema

def generate_ema(input_data: list, short_interval: int,  long_interval: int, x_axis: str, y_axis: str, inplace: bool ) -> list :

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
            'macd': el.get('macd'),
            'macd_s': el.get('macd_s'),
            'macd_h': el.get('macd_h'),
        } for el in data]