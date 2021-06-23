#!/usr/bin/env python3
from astroquery.jplhorizons import Horizons
import pandas as pd
import sys
import argparse
import os
from datetime import datetime, date, timedelta

DATA_PATH = 'data/'


def daterange(start_date, end_date, step):
    for n in range(0, int((end_date - start_date).days), step):
        yield start_date + timedelta(n)


parser = argparse.ArgumentParser()

parser.add_argument('--init_date')
parser.add_argument('--end_date')
parser.add_argument('--lat', type=float)
parser.add_argument('--lon', type=float)
parser.add_argument('--alt', type=float)
parser.add_argument('--steps', type=int, default=1)
parser.add_argument('--data_steps')
parser.add_argument('--name', default="")


args = parser.parse_args()
steps = args.steps
arg_init_date = datetime.strptime(args.init_date, '%Y-%m-%d')
arg_end_date = datetime.strptime(args.end_date, '%Y-%m-%d')

if args.name == "":
    file_name = f"train_eph_data_{arg_init_date.strftime('%Y%m%d')}_{arg_end_date.strftime('%Y%m%d')}_{args.data_steps}.csv"
else:
    file_name = args.name

print(f"============ GETTING DATE FROM JPL HORIZONS ============")
for date in daterange(arg_init_date, arg_end_date, steps):
    start_date = date.strftime('%Y-%m-%d')
    end_date = (date + timedelta(steps - 1)).strftime('%Y-%m-%d')
    print(f"=== Processing data for {start_date} - {end_date} ===")
    print(f"Downloading data ....")
    obj = Horizons(
        id='301',
        id_type='majorbody',
        location={
            'lon': args.lon,
            'lat': args.lat,
            'elevation': args.alt
        },
        epochs={
            'start': f'{start_date} 00:00:00',
            'stop': f'{end_date} 23:59:59',
            'step': args.data_steps
        },
    )
    eph = obj.ephemerides(quantities='4')
    data_eph = eph.to_pandas()
    print(f"Transforming data ....")
    data_eph['datetime'] = pd.to_datetime(data_eph['datetime_str'])
    data_eph['hour'] = data_eph['datetime'].dt.hour

    # Adding observer coordinates
    data_eph['lon'] = args.lon
    data_eph['lat'] = args.lat
    data_eph['alt'] = args.alt

    # Drop columns
    data_eph.drop(columns=['datetime_str'], inplace=True)

    # Save
    print(f'Save data to file [{file_name}] ...')
    print(f'Saving {data_eph.shape[0]} rows ')

    if os.path.exists(DATA_PATH+file_name):
        data_eph.to_csv(DATA_PATH+file_name, index=False, header=False, mode='a')
    else:
        data_eph.to_csv(DATA_PATH+file_name, index=False)

    print("Saved data")

