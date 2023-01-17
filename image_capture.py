import gxipy as gx
from datetime import datetime, timedelta
from PIL import Image

def get_first_camera():
    device_manager = gx.DeviceManager()
    num_devices, _ = device_manager.update_device_list()
    if num_devices == 0:
        raise RuntimeError("No devices found")

    camera = device_manager.open_device_by_index(1)

    camera.BalanceWhiteAuto = 1
    camera.ExposureAuto = 1
    camera.GainAuto = 1
    camera.TriggerMode.set(gx.GxSwitchEntry.ON)
    camera.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
    camera.stream_on()

def acquire_color_frame(device: gx.Device, timeout):
    initial_time = datetime.now()
    while True:
        if datetime.now() - initial_time > timedelta(milliseconds=timeout):
            raise RuntimeError("Failed to get frame")

        device.TriggerSoftware.send_command()
        raw_frame = device.data_stream[0].get_image()
        if raw_frame is None:
            print("Retrying to acquire frame")
            continue

        rgb_buffer = raw_frame.convert("RGB")

        gamma_value = camera.GammaParam.get()
        gamma_lut = gx.Utility.get_gamma_lut(gamma_value)
        contrast_value = camera.ContrastParam.get()
        contrast_lut = gx.Utility.get_contrast_lut(contrast_value)
        color_correction_param = camera.ColorCorrectionParam.get()

        rgb_buffer.image_improvement(color_correction_param, contrast_lut, gamma_lut)
        
        return Image.fromarray(rgb_buffer.get_numpy_array(), "RGB")

if __name__ == "__main__":
    from time import sleep

    camera = get_first_camera()

    print("Starting acquisition, rate 2 frames per second")
    seq = 0
    idx = 0
    for seq in range(10):
        for idx in range(10):
            input(f"Enter to acquire {seq}_{idx}")
            image = acquire_color_frame(camera, 300)
            image.save(f"captures/seq_{seq}_img_{idx}.jpeg", "JPEG")
        print("Rotate")