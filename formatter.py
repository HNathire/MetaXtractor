"""
A class for formatting various types of data.
    
"""
class Formatter:

    def format_gps(self, gps_coordinates: str) -> str:
        latitude, longitude, _ = gps_coordinates.split('+')
        return f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    
    def convert_gps(self, degrees, minutes, seconds, direction):
        decimal_minutes = minutes + seconds / 60
        return f"{degrees}°{decimal_minutes:.4f}'{direction}"
    
    def format_exposure_time(self, exposure_time):
        numerator, denominator = map(int, str(exposure_time).split('/'))
        if denominator == 1:
            return f"{numerator} sec"
        elif denominator > 1:
            return f"1/{denominator} sec"
        else:
            return f"{numerator / denominator:.2f} sec"    
        
    
    def format_size(self, size_in_bytes):
        if size_in_bytes < 1024:
            return f"{size_in_bytes} B"
        elif size_in_bytes < 1024 ** 2:
            return f"{size_in_bytes / 1024:.2f} KB"
        elif size_in_bytes < 1024 ** 3:
            return f"{size_in_bytes / (1024 ** 2):.2f} MB"
        else:
            return f"{size_in_bytes / (1024 ** 3):.2f} GB"
          

    def format_duration(self, duration_in_seconds):
        if duration_in_seconds < 60:
            return f"{int(duration_in_seconds)} sec"
        elif duration_in_seconds < 3600:
            minutes = int(duration_in_seconds // 60)
            seconds = int(duration_in_seconds % 60)
            return f"{minutes} min {seconds} sec"
        else:
            hours = int(duration_in_seconds // 3600)
            minutes = int((duration_in_seconds % 3600) // 60)
            seconds = int(duration_in_seconds % 60)
            return f"{hours} hr {minutes} min {seconds} sec"
        
        
    def format_framerate(self, framerate):
        if isinstance(framerate, str):
            framerate = float(framerate)   
        return f"{framerate:.2f} fps"


    def format_bitrate(self, bitrate):
        if bitrate < 1024:
            return f"{bitrate} bps"
        elif bitrate < 1024 ** 2:
            return f"{bitrate / 1024:.2f} Kbps"
        elif bitrate < 1024 ** 3:
            return f"{bitrate / (1024 ** 2):.2f} Mbps"
        else:
            return f"{bitrate / (1024 ** 3):.2f} Gbps"


    def format_samplerate(self, samplerate):
        return f"{samplerate / 1000:.2f} KHz"
    
    
    def format_focal_length(self, FocalLength):
        numerator, denominator = map(int, str(FocalLength).split('/'))
        focal_length_mm = numerator / denominator
        if focal_length_mm < 10:
            return f"{focal_length_mm:.1f} mm"
        else:
            return f"{int(focal_length_mm)} mm"
       
        
    def format_brightness_value(self, BrightnessValue):
        numerator, denominator = map(int, str(BrightnessValue).split('/'))
        brightness_value = numerator / denominator
        return f"{brightness_value:.2f}"
    
    
    def format_aperture_value(self, ApertureValue):
        numerator, denominator = map(int, str(ApertureValue).split('/'))
        aperture_value = numerator / denominator
        return f"f/{aperture_value:.2f}"
    
    
    def format_shutter_speed(self, ShutterSpeedValue):
        numerator, denominator = map(int, str(ShutterSpeedValue).split('/'))
        shutter_speed = numerator / denominator
        if shutter_speed >= 1:
            return f"{int(shutter_speed)} sec"
        else:
            return f"1/{int(1 / shutter_speed)} sec"
     
        
