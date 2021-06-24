import os
import subprocess

    
commands = [
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=14.751404 --lon=-89.551260  --alt=384 --steps=5 --data_steps=500 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-06-15' --lat=14.551251 --lon=-90.741459 --alt=1524 --steps=5 --data_steps=550 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=15.699210 --lon=-90.990331 --alt=1291 --steps=10 --data_steps=300 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=14.359963 --lon=-90.949078 --alt=584 --steps=10 --data_steps=261 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=15.665604 --lon=-89.384656 --alt=833 --steps=10 --data_steps=400 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=13.953282 --lon=-90.352191 --alt=26 --steps=10 --data_steps=654 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=14.288236 --lon=-91.911006 --alt=0 --steps=10 --data_steps=575 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=14.618401 --lon=-90.498344 --alt=1476 --steps=10 --data_steps=354 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=14.603912 --lon=-90.594198 --alt=1575 --steps=10 --data_steps=792 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=14.587976 --lon=-90.551085 --alt=1488 --steps=10 --data_steps=650 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=14.711089 --lon=-90.646974 --alt=1907 --steps=10 --data_steps=897 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=15.435210 --lon=-90.742907 --alt=1356 --steps=10 --data_steps=654 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=14.536296 --lon=-90.579262 --alt=1338 --steps=10 --data_steps='1000' --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=14.259353 --lon=-91.354933 --alt=64 --steps=10 --data_steps=345 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=16.425908 --lon=-90.075304 --alt=157 --steps=10 --data_steps=798 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=17.200694 --lon=-89.580172 --alt=291 --steps=10 --data_steps=562 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=14.430869 --lon=-90.565353 --alt=1382 --steps=10 --data_steps=465 --name='train_data_'",
    "python3 download_data.py --init_date='2021-01-01' --end_date='2021-07-15' --lat=15.269285 --lon=-90.577148 --alt=1527 --steps=10 --data_steps=159 --name='train_data_'",
    "python3 download_data.py --init_date='2020-08-01' --end_date='2020-12-31' --lat=15.162066 --lon=-91.432063 --alt=1912 --step=10 --data_steps=565 --name='train_data_'",
    "python3 download_data.py --init_date='2020-08-01' --end_date='2020-12-31' --lat=15.245289 --lon=-91.933262 --alt=2794 --step=10 --data_steps=523 --name='train_data_'",
    "python3 download_data.py --init_date='2020-08-01' --end_date='2020-12-31' --lat=15.470579 --lon=-90.209735 --alt=1403 --step=10 --data_steps=242 --name='train_data_'",
    "python3 download_data.py --init_date='2020-08-01' --end_date='2020-12-31' --lat=15.370891 --lon=-88.976455 --alt=66 --step=10 --data_steps=365 --name='train_data_'",
    "python3 download_data.py --init_date='2020-08-01' --end_date='2020-12-31' --lat=14.553152 --lon=-90.489329 --alt=1780 --step=10 --data_steps=423 --name='train_data_'"
]

for index, command in enumerate(commands[18:], start=18):
    while True:
        try:
            subprocess.run([command+str(index)], check=True, shell=True)
            print(f">>>>>>>> {index+1}/{len(commands)} Batches of data downloaded")
            print(f"==========  [train_data_{index}.csv] ============")
        except subprocess.CalledProcessError:
            print("Error :S, removing file....")
            os.system("rm ./data/train_data_"+str(index))
            print("Removed file [ok]")
            continue
        break