import csv
import xlrd
import sys
import datetime

def date_ascending(filename):

    ''' sort/sorted key function to sort dates in ascending order ''' 

    date_string = filename[-15: -5]
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    return (date - datetime.datetime(1970,1,1)).total_seconds()


def days_into_study(dataset_date, signup_date):

    start = datetime.date(signup_date.year, signup_date.month, signup_date.day)
    stop = datetime.date(dataset_date.year, dataset_date.month, dataset_date.day)

    return (stop - start).days

def months_into_study(subject_id, day):

    DATA_ROW_START = 2
    SUBJECT_ID_COL = 0
    SIGNUP_DATE_COL = 1

    book = xlrd.open_workbook('lib/month_day_subject_calculator.xlsx')
    sheet = book.sheet_by_name('Sheet1')

    # look through rows for subject id in first cell 
    for rownum in xrange(DATA_ROW_START, sheet.nrows):

        row_values = sheet.row_values(rownum)
        current_subject_id = str(int(float( row_values[SUBJECT_ID_COL] )))

        if current_subject_id == subject_id:

            day_columns = row_values[2:26:2] 

            for index, d in enumerate(day_columns):

                next_index = index + 1

                if next_index == len(day_columns):
                    return index

                day_end = day_columns[index + 1]
                if day < day_end:
                    return index


def normalize_date(days): 

    ''' convert days since 1900 to now '''

    base_date = datetime.datetime(1900,1,1)
    adjusted_date = base_date + datetime.timedelta(days=days - 2)

    return adjusted_date


def month_and_day_into_study(subject_id, dataset_date, filename):

    SUBJECT_ID_COL = 0
    SIGNUP_DATE_COL = 1
    DATA_ROW_START = 2

    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name('Sheet1')

    current_subject_id, signup_date = None, None
    month, day = None, None

    # look through rows for subject id in first cell 
    for rownum in xrange(DATA_ROW_START, sheet.nrows):

        current_subject_id = str(int(float( sheet.row_values(rownum)[SUBJECT_ID_COL] )))

        # when matched
        if current_subject_id == subject_id:

            # grab associated signup date (in days since 1900) from second cell
            # normalize it
            days_since_1900 = int( float( sheet.row_values(rownum)[SIGNUP_DATE_COL] ))
            signup_date = normalize_date(days_since_1900)
            signup_date = datetime.datetime(signup_date.year, signup_date.month, signup_date.day)

            # calculate current month and day of study 
            day = days_into_study(dataset_date, signup_date)
            month = months_into_study(subject_id, day);

    return month, day
