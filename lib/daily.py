from collections import namedtuple
from datetime import datetime
import json
import os

from .common import MS_PER_HR_FLOAT, get_calories, get_avg_heart_rate, get_peak_heart_rate, get_lowest_heart_rate, fb_date_to_msband_date
from .headers import headers
from .row import row_factory

Row = row_factory(headers=headers['daily'])

def build_daily(subject_id, dataset):

    heart_data = dataset['activities-heart-intraday']['dataset'] 

    if len(heart_data):     

        return Row(
            
            subjectid=subject_id,
            date=fb_date_to_msband_date( dataset['activities-heart'][0]['dateTime'] ),
            avghr=get_avg_heart_rate( dataset['activities-heart-intraday'] ), 
            pkhr=get_peak_heart_rate( dataset['activities-heart-intraday'] ), 
            lwhr=get_lowest_heart_rate( dataset['activities-heart-intraday'] ), 
            step=int( dataset['activities-steps'][0]['value'] ),
            #cal=int( dataset['activities-calories'][0]['value'] ),
            cal=get_calories(dataset.get('activities-calories')),
            dt=float(dataset['activities-distance'][0]['value']) if len(dataset.get('activities-distance', [])) else '.',
            dtof=float(dataset['activities-distance'][0]['value']) if len(dataset.get('activities-distance', [])) else '.',
            hract= (dataset['activities'][0]['duration']) / MS_PER_HR_FLOAT if dataset.get('activities') else '.'

        )

    else:

        return Row(
            subjectid=subject_id,
            date=dataset['activities-heart'][0]['dateTime'],
        ) 
