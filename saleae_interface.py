from saleae import Saleae, PerformanceOption, Trigger
from Alert2Encoder.Alert2Encoder.Unit_tests.pylibs.sfpPort import SfpPort
from Alert2Encoder.Alert2Encoder.Unit_tests.pylibs.protocols.interface.serialHub import SerialPort
import os
import time
import csv


filename = 'C:\\Projects\\CampbellScientific\\Testing\\AL200_TestFarm/Captures/test.csv'
filename2 = 'C:\\Projects\\CampbellScientific\\Testing\\AL200_TestFarm/Captures/rftail_wave_small.csv'
digital_rate = 50000000
analog_rate = 125000
sample_rate = (digital_rate, analog_rate)


def capture_samples(al200_cli, digital_channels, analog_channels, trigger_channel, trigger_type, capture_time, cli_cmd):
    if os.path.exists(filename):
        os.remove(filename)
    s = Saleae(host='localhost', port=10429)
    if s.is_logic_running():

        try:
            s.close_all_tabs()
        except s.CommandNAKedError:
            print("Close tabs command failed")
            s.capture_stop()
            return False
        s.set_performance(PerformanceOption.Full)

        devs = s.get_connected_devices()
        if len(devs) >= 1:
            print("Found {} logic analyzers".format(len(devs)))
            if len(devs) > 1:
                # Select first device found, this could change in the future or may not be needed at all
                s.select_active_device(0)

            s.set_active_channels(digital_channels, analog_channels)
            reset_all_triggers(s, digital_channels)
            if trigger_channel > 0:
                s.set_trigger_one_channel(trigger_channel, trigger_type)  # 1, Trigger.Negedge

            # s.set_num_samples(50000000)
            s.set_capture_seconds(capture_time)  # 2
            s.set_capture_pretrigger_buffer_size(100000)
            rates = s.get_all_sample_rates()
            # print("Rates: {}".format(rates))
            for tup in rates:
                if tup == sample_rate:
                    s.set_sample_rate(sample_rate)
                    break

            s.capture_start()
            time.sleep(.5)
            al200_cli.sendText(cli_cmd)
            start = time.time()
            while time.time() < start + 3:
                # print("Waiting for capture")
                if s.is_processing_complete():
                    break
            try:
                s.get_capture_range()
            except ValueError:
                pass
            except s.CommandNAKedError:
                return False
            time.sleep(1)

            print("Exporting data to csv")
            s.export_data2(filename, analog_channels=analog_channels)
            while not s.is_processing_complete():
                print("Waiting for export")
                time.sleep(5)

            if os.path.exists(filename): # and no_timeout:
                return True
            else:
                return False
        else:
            print("Failed to detect logic analyzer.")
            raise ConnectionError

def is_number(s):
    try:
        float(s)
        return True
    except:
        return False

def is_just_frame(csvreader):
    for row in csvreader:
        if is_number(row['PTT']):
            if float(row['PTT']) > 4.0:
                return False
    return True

def get_transmission():
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, fieldnames=['Time', 'TX', 'PTT'])
        HEADS, PRETRIG, PTTVALID, PTTHI, PTTLO = range(5)
        state = HEADS
        data = []
        try:
            if is_just_frame(csvreader):
                return [float(row['TX']) for row in csvreader if is_number(row['TX'])]
            for row in csvreader:
                if state is HEADS:
                    if is_number(row['Time']):
                        state = PRETRIG
                if state is PRETRIG:
                    if float(row['Time']) >= 0.0:
                        if float(row['PTT']) < 0.04:
                            state = PTTLO
                        else:
                            state = PTTVALID
                if state is PTTVALID:
                    if float(row['PTT']) > 4.0:
                        state = PTTHI
                if state is PTTHI:
                    if float(row['PTT']) < 0.04:
                        state = PTTLO
                if state is PTTLO:
                    if float(row['PTT']) > 4.0:
                        break
                    data.append(float(row['TX']))
            # if float(row['PTT']) < 1.0:
            #     return []
        except ValueError:
            return []
        return data


def get_transmission_plus_rx():
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, fieldnames=['Time', 'TX', 'PTT', 'AI'])
        count = 0
        tx_data = []
        rx_data = []
        try:
            for row in csvreader:
                if count > 1:
                    if float(row['Time']) < 0.0:
                        trigger_row = count
                    if count > trigger_row:
                        if float(row['PTT']) > 4.0:
                            break
                        if float(row['PTT']) < 0.04:
                            tx_data.append(float(row['TX']))
                            rx_data.append(float(row['AI']))
                count += 1
            # Slightly bad practice to look at row out of scope of the for loop
            # but this will detect an incomplete capture and return blank instead of returning a partial frame
            if float(row['PTT']) < 1.0:
                return []
        except ValueError:
            return []
        return tx_data, rx_data

def get_radio_warmup_samples():
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, fieldnames=['Time', 'TX', 'PTT', 'SW-12 V'])
        count = 0
        samples = 0
        ptt_high = False
        try:
            for row in csvreader:
                if count >= 2:
                    if float(row['Time']) > 0.0:
                        samples += 1
                        if ptt_high:
                            if float(row['PTT']) < 0.1:
                                return samples
                        if float(row['PTT']) > 4.0:
                            ptt_high = True
                count += 1
        except ValueError:
            return 0
        return 0


def get_sine_samples():
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, fieldnames=['Time', 'TX', 'PTT'])
        count = 0
        data = []
        try:
            for row in csvreader:
                if count > 1:
                    if float(row['PTT']) > 4.0:
                        data.append(float(row['TX']))
                count += 1
        except ValueError:
            return []
        return data


def reset_all_triggers(saleae, chans):
    for channel in chans:
        saleae.set_trigger_one_channel(channel, Trigger.NoTrigger)


if __name__ == '__main__':
    cli = SfpPort(SerialPort('COM13'))
    count = 0
    passes = 0
    bad_captures = 0
    while count < 10:
        result = capture_samples(cli)
        if result:
            data = get_transmission()
            if data:
                passes += 1
        else:
            bad_captures += 1
        count += 1
        time.sleep(10)
    print("Passed {} times".format(passes))
    print("Bad captures: {}".format(bad_captures))
