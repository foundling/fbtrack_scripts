from collections import namedtuple
from datetime import datetime
from dateutil.parser import parse
import json
import os

from common import MS_PER_HR_FLOAT, MIN_PER_HR_FLOAT, get_avg_heart_rate, get_peak_heart_rate, get_lowest_heart_rate, fb_date_to_msband_date
from headers import headers
from row import row_factory

Row = row_factory(headers=headers['sleep_by_minute'])

def extract_sleep_data_minute(dataset):

    ''' Extract sleep data or return None if it doesn't exist. '''

    sleep_dataset = None
    if 'sleep' in dataset and len( dataset['sleep'] ):
        sleep_dataset = dataset['sleep']

    return sleep_dataset

def build_sleep_minute(subject_id, dataset):

    sleep_dataset = extract_sleep_data_minute(dataset)

    if sleep_dataset:
        return [ Row(
            subjectid = subject_id,
            date = fb_date_to_msband_date( dataset['activities-heart'][0]['dateTime'] ),
            is_main_event = '1' if sleep_dataset[i]['isMainSleep']==True else '0',
            time_bed = sleep_dataset[i]['duration'] / MS_PER_HR_FLOAT,
            sleep_dur = sleep_dataset[i]['minutesAsleep'] / MIN_PER_HR_FLOAT,
            sleep_start_time = sleep_dataset[i]['startTime'] if sleep_dataset[i].get('startTime') else '.',
            sleep_end_time = sleep_dataset[i]['endTime'] if sleep_dataset[i].get('endTime') else '.',
            sleep_time = sleep_dataset[i]['minuteData'][j]['dateTime'],
            sleep_phase = sleep_dataset[i]['minuteData'][j]['value']
        )
        for i in range(len(sleep_dataset))
        for j in range(len(sleep_dataset[i]['minuteData'] ))]

    else:
        return [ Row(
            subjectid=subject_id,
            date=dataset['activities-heart'][0]['dateTime'],
        ) ]
