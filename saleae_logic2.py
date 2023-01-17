from saleae import automation
import os
import os.path as path
import time
from Pylibs.protocols.dev_config_cli import DeviceConfigCLI
from Pylibs.protocols.saleae_interface import get_transmission, get_raw_samples, get_radio_warmup_samples, \
    get_sine_samples
# from Pylibs.protocols.SerialSampler import removeDC, trim, resamp, filt, comb, clean, sync, to_bytes


filename = 'C:\\Projects\\CampbellScientific\\Testing\\AL200_TestFarm/Captures/analog.csv'
directory = 'C:\\Projects\\CampbellScientific\\Testing\\AL200_TestFarm/Captures'
digital_timed_rate = 20000000
digital_trigger_rate = 10000000
analog_rate = 625000


class Configurations:
    # Class to store configurations for different purposes
    # Config attributes can be altered as needed if class is instantiated

    # Device config for basic transmission and PDU capture
    tx_device_config = automation.LogicDeviceConfiguration(
        enabled_analog_channels=[0, 1],
        enabled_digital_channels=[0, 1, 2],
        analog_sample_rate=analog_rate,
        digital_sample_rate=digital_trigger_rate,
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

    # Capture config for square wave used to measure gain
    timed_waveform_capture_config = automation.CaptureConfiguration(
        capture_mode=automation.TimedCaptureMode(
            duration_seconds=2,
            trim_data_seconds=2
        ),
        buffer_size_megabytes=3000
    )

    # Device config for checking radio warmup timing
    radio_warmup_device_config = automation.LogicDeviceConfiguration(
        enabled_analog_channels=[0, 1, 2],
        enabled_digital_channels=[0, 1, 2],
        analog_sample_rate=analog_rate,
        digital_sample_rate=digital_trigger_rate,
        glitch_filters=[automation.GlitchFilterEntry(
            channel_index=1,
            pulse_width_seconds=0.00001
        )]
    )

    # Capture config for radio warmup timing
    radio_warmup_capture_config = automation.CaptureConfiguration(
        capture_mode=automation.DigitalTriggerCaptureMode(
            trigger_type=automation.DigitalTriggerType.RISING,
            trigger_channel_index=2,
            after_trigger_seconds=3
        ),
        buffer_size_megabytes=4000
    )

    sine_wave_device_config = automation.LogicDeviceConfiguration(
        enabled_analog_channels=[0, 1],
        enabled_digital_channels=[0, 1],
        analog_sample_rate=analog_rate,
        digital_sample_rate=digital_timed_rate
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


def capture_square_wave(al2_cli):
    with automation.Manager.connect(port=10430) as manager:
        try:
            config = Configurations()
            al2_cli.send_command('square')
            with manager.start_capture(device_configuration=config.sine_wave_device_config,
                                       capture_configuration=config.timed_waveform_capture_config
                                       ) as capture:
                capture.wait()

                delete_export_file()
                capture.export_raw_data_csv(directory=directory,
                                            analog_channels=config.tx_device_config.enabled_analog_channels)
                al2_cli.send_command('waveoff')

            return True
        except automation.CaptureError:
            print("Saleae capture error")
            return False
        except automation.ExportError:
            print("Saleae export error")
            return False


def capture_radio_warmup(al2_cli):
    with automation.Manager.connect(port=10430) as manager:
        try:
            config = Configurations()
            with manager.start_capture(device_configuration=config.radio_warmup_device_config,
                                       capture_configuration=config.radio_warmup_capture_config
                                       ) as capture:
                al2_cli.send_command('sendtest')
                capture.wait()

                delete_export_file()
                capture.export_raw_data_csv(directory=directory,
                                            analog_channels=config.radio_warmup_device_config.enabled_analog_channels)

            return True
        except automation.CaptureError:
            print("Saleae capture error")
            return False
        except automation.ExportError:
            print("Saleae export error")
            return False


def capture_sine_wave(al2_cli):
    with automation.Manager.connect(port=10430) as manager:
        try:
            config = Configurations()
            config.timed_waveform_capture_config.capture_mode.duration_seconds = 1.5
            al2_cli.send_command('sine')
            with manager.start_capture(device_configuration=config.sine_wave_device_config,
                                       capture_configuration=config.timed_waveform_capture_config
                                       ) as capture:
                capture.wait()

                delete_export_file()
                capture.export_raw_data_csv(directory=directory,
                                            analog_channels=config.sine_wave_device_config.enabled_analog_channels)
            return True
        except automation.CaptureError:
            print("Saleae capture error")
            return False
        except automation.ExportError:
            print("Saleae export error")
            return False


def get_capture_data():
    return get_transmission(filename)


def get_raw_data():
    return get_raw_samples(filename)


def get_radio_warmup_data():
    return get_radio_warmup_samples(filename)


def get_sine_wave_data():
    return get_sine_samples(filename)


if __name__ == '__main__':
    cli = DeviceConfigCLI('COM34')
    bad = 0
    count = 0
    data = []
    while count < 10:
        result = capture_tx(cli)
        if not result:
            bad += 1
        else:
            data = get_capture_data()
            count += 1
            if data:
                break
        time.sleep(10)

    print("Received frame: {}".format(data))
