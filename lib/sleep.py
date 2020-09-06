from collections import namedtuple
from datetime import datetime
from dateutil.parser import parse
import json
import os

from .common import MS_PER_HR_FLOAT, MIN_PER_HR_FLOAT, get_calories, get_avg_heart_rate, get_peak_heart_rate, get_lowest_heart_rate, fb_date_to_msband_date
from .headers import headers
from .row import row_factory

Row = row_factory(headers=headers['sleep'])

def extract_sleep_data(dataset):

    ''' Extract sleep data (might contain multiple sleep events) or return None if it doesn't exist. '''

    sleep_dataset = None
    if 'sleep' in dataset and len( dataset['sleep'] ):
        sleep_dataset = dataset['sleep']

    return sleep_dataset


def build_sleep(subject_id, dataset):

    sleep_dataset = extract_sleep_data(dataset)

    if sleep_dataset:

        return [ Row(
            subjectid = subject_id,
            msid = '.',
            date = fb_date_to_msband_date( dataset['activities-heart'][0]['dateTime'] ),
            avghr = get_avg_heart_rate( dataset['activities-heart-intraday'] ),
            pkhr = get_peak_heart_rate( dataset['activities-heart-intraday'] ),
            lwhr = get_lowest_heart_rate( dataset['activities-heart-intraday'] ),
            cal = int( dataset['activities-calories'][0]['value'] ) if dataset.get('activities-calories') else '.',

            sleep_events = int( dataset['summary']['totalSleepRecords'] ),
            total_sleep_dur = dataset['summary']['totalMinutesAsleep']/ MIN_PER_HR_FLOAT, #across sleep events
            total_time_bed = dataset['summary']['totalTimeInBed']/ MIN_PER_HR_FLOAT, #across sleep events

            is_main_event = '1' if sleep_dataset[i]['isMainSleep']==True else '0',
            sleep_start_time = sleep_dataset[i]['startTime'] if sleep_dataset[i].get('startTime') else '.',
            sleep_end_time = sleep_dataset[i]['endTime'] if sleep_dataset[i].get('endTime') else '.',

            sleep_dur = sleep_dataset[i]['minutesAsleep'] / MIN_PER_HR_FLOAT, #this would be the first sleep event only
            time_bed = sleep_dataset[i]['duration'] / MS_PER_HR_FLOAT, #this would be the first sleep event only
            sleep_eff = sleep_dataset[i]['efficiency'], #this would be the first sleep event only
            fall_asleep_dur = sleep_dataset[i]['minutesToFallAsleep'] / MIN_PER_HR_FLOAT,
            restless_dur = sleep_dataset[i]['restlessDuration'] / MIN_PER_HR_FLOAT,
            #restless_prop = restless_dur / sleep_dur,
            awakenings_count = sleep_dataset[i]['awakeningsCount'],
            awake_count = sleep_dataset[i]['awakeCount'],
            awake_dur = sleep_dataset[i]['awakeDuration'] / MIN_PER_HR_FLOAT

            #hrrest = '.',
            #fat = sleep_dataset['minutesToFallAsleep'] / MIN_PER_HR_FLOAT,
            #wutime = '.',
            #sdurrf = '.',
            # sdurrf is N/A but here's a guess as to how to calculate:
            # (sleep_dataset['minutesAsleep'] - sleep_dataset['restlessDuration']) / MIN_PER_HR_FLOAT

        )
        for i in range(len(sleep_dataset)) ]

    else:
        return [ Row(
            subjectid=subject_id,
            date=dataset['activities-heart'][0]['dateTime']
        ) ]
