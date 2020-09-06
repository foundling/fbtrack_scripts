from collections import namedtuple
from datetime import datetime
from dateutil.parser import parse
import json
import os

from .common import MS_PER_HR_FLOAT, MIN_PER_HR_FLOAT, get_calories, get_avg_heart_rate, get_peak_heart_rate, get_lowest_heart_rate, fb_date_to_msband_date
from .headers import headers
from .row import row_factory

Row = row_factory(headers=headers['sleep'])

def build_sleep(subject_id, dataset):

    sleep_data = dataset['sleep']
    if 'sleep' in sleep_data:

        return Row(
            subjectid = subject_id,
            msid = '.',
            date = fb_date_to_msband_date(dataset['activities-heart'][0]['dateTime']) if dataset.get('activities-heart') else None,
            dur = dataset['sleep']['duration'] / MS_PER_HR_FLOAT,  
            avghr = get_avg_heart_rate( dataset['activities-heart-intraday'] ),
            pkhr = get_peak_heart_rate( dataset['activities-heart-intraday'] ), 
            lwhr = get_lowest_heart_rate( dataset['activities-heart-intraday'] ),
            #cal = int( dataset['activities-calories'][0]['value'] ),
            cal = get_calories(dataset.get('activities-calories')),
            sleff = sleep_dataset['efficiency'],
            sdurrl = sleep_dataset['restlessDuration'] / MIN_PER_HR_FLOAT,
            sdurrf = '.',
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
            date=fb_date_to_msband_date(dataset['activities-heart'][0]['dateTime']) if dataset.get('activities-heart') else None,
        )
