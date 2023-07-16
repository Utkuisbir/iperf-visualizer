import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(
    description="This python code has written to analyze iperf3 throughput results with visualizing every minute."
)

parser.add_argument('--iwconfig', '-w', type=str, required=False, help='path of iwconfig text file')
parser.add_argument('--iperf_log', '-i', type=str, required=True, help='path of iperf log file')
parser.add_argument('--iperf_limit', '-l', type=int, required=True, help='upper limit of iperf graph')
args = parser.parse_args()


iwconfig_file = args.iwconfig
json_file = args.iperf_log
limit_for_Mbit_to_show_on_table = args.iperf_limit

#IWCONFIG FILE READ

#Access Point değişkeni
ap_str = "Access Point:"

# Zaman ve Access Point değeri için listeler oluştur
times = []
aps = []
signal_levels = []

# Dosyayı oku ve Access Point değerini ve zamanını al
if iwconfig_file:
    with open(iwconfig_file) as f:
        for line in f:
            if ap_str in line:
                time_str = line.split()[0] + " " + line.split()[1]
                time = datetime.strptime(time_str, "[%Y-%m-%d %H:%M:%S]")
                ap = line.split(ap_str)[1].strip()
                times.append(time)
                aps.append(ap)

        for line in f:
            if "Signal level" in line:
                signal_level = line.split("Signal level=")[1].split()[0].strip()
                signal_levels.append(signal_level)



conneceted_ap = []
for ap in aps:
    if " " in ap:  # Eğer boşluk varsa
        ap = ap.split(" ")[0]  # İlk kelimeyi al
    conneceted_ap.append(ap)



# JSON FILE READ

with open(json_file, 'r') as f:
    data = json.load(f)

bits_per_seconds = []
seconds = []
start_time_as_epoch_time = 0


start_time_as_epoch_time = data['start']['timestamp']['timesecs'] 



for interval in data['intervals']:
    for stream in interval['streams']:
        bits_per_seconds.append(stream['bits_per_second'])
        seconds.append(stream['start'])

int_bits_per_seconds = [int(round(x)) for x in bits_per_seconds]
Mbps = [x / 1000000 for x in bits_per_seconds]
Mbits_per_seconds = [float(f"{x:.1f}") for x in Mbps]



seconds_as_integers= []
for sec in seconds:
    num = int(sec)
    seconds_as_integers.append(num)


while_iperf_epoch_time = []
for sec in seconds_as_integers:
    sum_epoch_time = start_time_as_epoch_time + sec
    while_iperf_epoch_time.append(sum_epoch_time)

while_iperf_date_time = []
for while_iperf_epoch_t in while_iperf_epoch_time:
    while_iperf_date_time.append(datetime.fromtimestamp(while_iperf_epoch_t))


data = pd.DataFrame({'Mbit/s': Mbits_per_seconds, 'Dates': while_iperf_date_time})

# Excel'e yazdırma
data.to_excel('Throughput_datas_per_second.xlsx', index=False)

from datetime import datetime

while_iperf_date_time_hours = [dt.strftime('%m/%d/%Y %H:%M:%S') for dt in while_iperf_date_time]
# convert while_iperf_date_time_hours to datetime objects
while_iperf_date_time_hours_as_datetime = [datetime.strptime(dt, '%m/%d/%Y %H:%M:%S') for dt in while_iperf_date_time_hours]

#if iwconfig file is given
if iwconfig_file:
    
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)

    ax2.plot(times, conneceted_ap, label='connected bssid', color='red')
    ax1.plot(while_iperf_date_time_hours_as_datetime, Mbits_per_seconds, label='speed', color='blue')

    ax1.set_ylabel('Mbit/s')
    ax2.set_ylabel('Connected BSSID')

    ax1.legend()
    ax2.legend()
    plt.show()
    
else:
    fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True)

    ax1.plot(while_iperf_date_time_hours_as_datetime, Mbits_per_seconds, label='speed', color='blue')

    ax1.set_ylabel('Mbit/s')
    ax1.legend()
    plt.show()













