from saleae import automation
import os
import os.path as path
import time
from Pylibs.protocols.dev_config_cli import DeviceConfigCLI
from Pylibs.protocols.saleae_interface import get_transmission
from Pylibs.protocols.SerialSampler import *


filename = 'C:\\Projects\\CampbellScientific\\Testing\\AL200_TestFarm/Captures/analog.csv'
directory = 'C:\\Projects\\CampbellScientific\\Testing\\AL200_TestFarm/Captures'
digital_rate = 10000000
analog_rate = 625000


class Configurations:
    # Class to store configurations for different purposes
    # Config attributes can be altered as needed if class is instantiated

    # Device config for basic transmission and PDU capture
    tx_device_config = automation.LogicDeviceConfiguration(
        enabled_analog_channels=[0, 1],
        enabled_digital_channels=[0, 1, 2],
        analog_sample_rate=analog_rate,
        digital_sample_rate=digital_rate,
        glitch_filters=[automation.GlitchFilterEntry(
            channel_index=1,
            pulse_width_seconds=0.00001
        )]
    )

    # Capture config for basic transmission and PDU capture
    tx_capture_config = automation.CaptureConfiguration(
        capture_mode=automation.DigitalTriggerCaptureMode(
            trigger_type=automation.DigitalTriggerType.FALLING,
            trigger_channel_index=1,
            after_trigger_seconds=1
        ),
        buffer_size_megabytes=3000
    )


def delete_export_file():
    if path.exists(filename):
        os.remove(filename)


def capture_tx(al2_cli, after_trigger_seconds=1):
    with automation.Manager.connect(port=10430) as manager:
        try:
            config = Configurations()
            config.tx_capture_config.capture_mode.after_trigger_seconds = after_trigger_seconds
            with manager.start_capture(device_configuration=Configurations.tx_device_config,
                                       capture_configuration=config.tx_capture_config
                                       ) as capture:
                al2_cli.send_command('sendtest')
                capture.wait()

                # capture.save_capture(directory)

                delete_export_file()

                capture.export_raw_data_csv(directory=directory,
                                            analog_channels=Configurations.tx_device_config.enabled_analog_channels)
            return True
        except automation.CaptureError:
            print("Saleae capture error")
            return False
        except automation.ExportError:
            print("Saleae export error")
            return False

def get_capture_data():
    return get_transmission(filename)


test_frame = [
        0xEB, 0x90, 0xB4, 0x33, 0xAA, 0xAA, 0x35, 0x2E, 0xF8, 0x53, 0x0D, 0xC5,
        0xD4, 0x21, 0x1A, 0xCC, 0x7D, 0x3C, 0x8D, 0xC1, 0x6A, 0x36, 0x58, 0x61,
        0xDD, 0xF9, 0x0E, 0x92, 0x08, 0xA0, 0x05, 0x4E, 0x5B, 0x62, 0x0C, 0x10,
        0xA8, 0xF1, 0x7F, 0xD3, 0x8D, 0xB3, 0x1F, 0x4F, 0xF2, 0x34, 0x40, 0x53,
        0xCF, 0xCC, 0xB3, 0x99, 0xA6, 0x59, 0x7A, 0x3D, 0xAC, 0x15, 0x0D, 0x3C,
        0x83, 0x78, 0xD1, 0x36, 0x6C, 0xD5, 0x1C, 0x8F, 0x92, 0xBA, 0xC9, 0xEF,
        0x37, 0x83, 0x75, 0xF1, 0x12, 0xA1, 0x73, 0xDC, 0xC7, 0xD3, 0xC8, 0x0E,
        0x14, 0x09, 0x33, 0x81, 0x88, 0xD5, 0x6E, 0xC0, 0xAA
    ]


if __name__ == '__main__':
    cli = DeviceConfigCLI('COM34')
    bad = 0
    count = 0
    frame = []
    while count < 10:
        result = capture_tx(cli)
        if not result:
            bad += 1
        else:
            data = get_capture_data()
            count += 1
        try:
            frame = to_bytes(sync(clean(comb(filt(resamp(trim(removeDC(data)))[1])))))
            if frame:
                break
        except ValueError:
            print("Value error on frame processing")
            time.sleep(10)
            continue
    assert frame == test_frame
