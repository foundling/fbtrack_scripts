import datetime

MS_PER_HR_FLOAT = float(1000 * 60 * 60)
MIN_PER_HR_FLOAT = 60.0

def get_calories(calories):

    if calories is None:
        return 0

    return int( calories[0].get('value') ) 


def fb_date_to_msband_date(date_string):
    ''' convert from fibit date format (yyyy-mm-dd) to match band date format (mm/dd/yyyy). '''

    return datetime.datetime.strptime(date_string, '%Y-%m-%d').strftime('%m/%d/%Y')

def get_avg_heart_rate(heart_intraday, hour=''):

    avg_heart_rate = None

    if len(heart_intraday['dataset']):

        hr_values = [ 
                record['value'] 
                for record 
                in heart_intraday['dataset']
                if record['time'].startswith(hour) ]

        avg_heart_rate = 0 if not len(hr_values) else float(sum(hr_values)) / len(hr_values) 

    return avg_heart_rate

def get_peak_heart_rate(heart_intraday, hour=''):

    max_heart_rate = None

    if len(heart_intraday['dataset']):

        readings = [ 
            record['value'] 
            for record 
            in heart_intraday['dataset'] 
            if record['time'].startswith(hour)
        ]

        max_heart_rate = max(readings) if len(readings) else 0

    return max_heart_rate

def get_lowest_heart_rate(heart_intraday, hour=''):

    min_heart_rate = None

    if len(heart_intraday['dataset']):

        readings = [ 
            record['value'] 
            for record 
            in heart_intraday['dataset'] 
            if record['time'].startswith(hour)
        ] 

        min_heart_rate = min(readings) if len(readings) else 0

    return min_heart_rate
