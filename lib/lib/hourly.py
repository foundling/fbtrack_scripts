from collections import namedtuple
import datetime
from dateutil.parser import parse
import json
import os
    
from .common import MS_PER_HR_FLOAT, get_avg_heart_rate, get_peak_heart_rate, get_lowest_heart_rate 
from .headers import headers
from .row import row_factory

Row = row_factory(headers=headers['hourly'])

HOURS = [   
        str(n).zfill(2) 
        for n in range(24) ]

def total_steps_hr(hour, dataset):
    if dataset is None:
        return 0

    return sum( [ 
                    d['value']
                    for d in dataset
                    if d['time'].startswith(hour) ] )

def total_calories_hr(hour, dataset):

    if dataset is None:
        return 0

    return sum( [
                    d['value']
                    for d in dataset
                    if d['time'].startswith(hour) ] )

def hourly_time_stamp(hour, time_string):

    hour_offset = int(hour)
    date = parse(time_string) 
    offset_date = date + datetime.timedelta(hours=hour_offset)

    return datetime.datetime.strftime(offset_date, '%m/%d/%Y %H:%M')

def total_distance_hr(hour, dataset):

    if dataset is None:
        return 0

    return sum([
                d['value']
                for d in dataset
                if d['time'].startswith(hour) ])

def build_hourly(subject_id, dataset, month, day):

    if len(dataset.get('activities-heart-intraday', []).get('dataset', [])):     

        return [ Row(
                    subjectid=subject_id,
                    date=hourly_time_stamp(hour, dataset['activities-heart'][0]['dateTime']),
                    day=day,
                    month=month,
                    avghr=get_avg_heart_rate( dataset['activities-heart-intraday'], hour ), 
                    pkhr=get_peak_heart_rate( dataset['activities-heart-intraday'], hour ), 
                    lwhr=get_lowest_heart_rate( dataset['activities-heart-intraday'], hour ), 
                    step=total_steps_hr(hour, dataset.get('activities-steps-intraday',{}).get('dataset')),
                    cal=total_calories_hr(hour, dataset.get('activities-calories-intraday', {}).get('dataset')),
                    dtof=total_distance_hr(hour, dataset.get('activities-distance-intraday',{}).get('dataset')),
                    dt=total_distance_hr(hour, dataset.get('activities-distance-intraday', {}).get('dataset')),
                    hract=(dataset['activities'][0]['duration'] / MS_PER_HR_FLOAT) if dataset.get('activities') else '.'
                 )
                 for hour in HOURS ]

    else:

        return [ Row(
                    subjectid=subject_id,
                    date=hourly_time_stamp(hour, dataset['activities-heart'][0]['dateTime']),
                    day=day,
                    month=month
                 )
                 for hour in HOURS ]
