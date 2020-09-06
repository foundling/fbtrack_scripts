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

    ''' Extract sleep data or return None if it doesn't exist. '''

    sleep_dataset = None 
    if 'sleep' in dataset and len( dataset['sleep'] ):
        sleep_dataset = dataset['sleep'][0]

    return sleep_dataset

def build_sleep(subject_id, dataset):
    # bug in this function?

    sleep_dataset = extract_sleep_data(dataset)

    if sleep_dataset:

        return Row(
            subjectid = subject_id,
            msid = '.',
            date = fb_date_to_msband_date( dataset['activities-heart'][0]['dateTime'] ),
            dur = sleep_dataset['duration'] / MS_PER_HR_FLOAT,  
            avghr = get_avg_heart_rate( dataset['activities-heart-intraday'] ),
            pkhr = get_peak_heart_rate( dataset['activities-heart-intraday'] ), 
            lwhr = get_lowest_heart_rate( dataset['activities-heart-intraday'] ),
            #cal = int( dataset['activities-calories'][0]['value'] ),
            cal = get_calories(dataset.get('activities-calories')),
            sleff = sleep_dataset['efficiency'],
            sdurrl = sleep_dataset['restlessDuration'] / MIN_PER_HR_FLOAT,

            sdurrf = '.',
            # sdurrf is N/A but here's a guess as to how to calculate:
            # (sleep_dataset['minutesAsleep'] - sleep_dataset['restlessDuration']) / MIN_PER_HR_FLOAT, 

            numwu = sleep_dataset['awakeningsCount'], 
            awdur = sleep_dataset['awakeDuration'] / MIN_PER_HR_FLOAT, 
            sdur = sleep_dataset['minutesAsleep'] / MIN_PER_HR_FLOAT,
            fadur = sleep_dataset['minutesToFallAsleep'] / MIN_PER_HR_FLOAT,
            hrrest = '.',
            fat = sleep_dataset['minutesToFallAsleep'] / MIN_PER_HR_FLOAT, 
            wutime = '.' 
        )

    else:
        return Row(
            subjectid=subject_id, 
            date=fb_date_to_msband_date(dataset['activities-heart'][0]['dateTime']),
        )