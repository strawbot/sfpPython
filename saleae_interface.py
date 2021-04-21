from saleae import Saleae, PerformanceOption, Trigger
from Alert2Encoder.Alert2Encoder.Unit_tests.pylibs.sfpPort import SfpPort
from Alert2Encoder.Alert2Encoder.Unit_tests.pylibs.protocols.interface.serialHub import SerialPort
import os
import time
import csv


filename = 'C:\\Projects\\CampbellScientific\\Testing\\AL200_TestFarm/Captures/test.csv'
sample_rate = (50000000, 2500000)


def capture_frames(al200_cli):
    if os.path.exists(filename):
        os.remove(filename)
    s = Saleae(host='localhost', port=10429)
    s.close_all_tabs()
    s.set_performance(PerformanceOption.Full)

    devs = s.get_connected_devices()
    if len(devs) >= 1:
        print("Found {} logic analyzers".format(len(devs)))
        if len(devs) > 1:
            # Select first device found, this could change in the future or may not be needed at all
            s.select_active_device(0)

        digital = [0, 1, 2]
        analog = [0, 1]
        s.set_active_channels(digital, analog)
        s.set_trigger_one_channel(1, Trigger.Negedge)

        s.set_num_samples(30000000)
        s.set_capture_pretrigger_buffer_size(100000)
        # s.set_capture_seconds(1)
        rates = s.get_all_sample_rates()
        print("Rates: {}".format(rates))
        for tup in rates:
            if tup == sample_rate:
                s.set_sample_rate(sample_rate)
                break

        s.capture_start()
        al200_cli.sendText('sendtest')
        start = time.time()
        no_timeout = False
        while time.time() < start + 3:
            print("Waiting for capture")
            if s.is_processing_complete():
                no_timeout = True
                break
        try:
            s.get_capture_range()
        except ValueError:
            pass
        except s.CommandNAKedError:
            return False
        time.sleep(3)

        # s.capture_stop()
        print("Exporting data to csv")
        s.export_data2(filename, analog_channels=analog)
        while not s.is_processing_complete():
            print("Waiting for export")
            time.sleep(1)

        al200_cli.sendText('0 beacon')

        if os.path.exists(filename): # and no_timeout:
            return True
        else:
            return False
    else:
        print("Failed to detect logic analyzer.")
        raise ConnectionError


def get_data():
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, fieldnames=['Time', 'TX', 'PTT'])
        count = 0
        data = []
        for row in csvreader:
            if count > 1:
                if float(row['Time']) < 0.0:
                    trigger_row = count
                if count > trigger_row:
                    if float(row['PTT']) > 4.0:
                        break
                    data.append(float(row['TX']))
            count += 1
        if float(row['PTT']) < 1.0:
            return []
        return data


if __name__ == '__main__':
    cli = SfpPort(SerialPort('COM13'))
    count = 0
    passes = 0
    bad_captures = 0
    while count < 10:
        result = capture_frames(cli)
        if result:
            data = get_data()
            if data:
                passes += 1
        else:
            bad_captures += 1
        count += 1
        time.sleep(10)
    print("Passed {} times".format(passes))
    print("Bad captures: {}".format(bad_captures))
