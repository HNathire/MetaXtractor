import exifread
import os
from formatter import Formatter

class PhotoMetadata:
    def __init__(self, file_path: str):
        # file_path: the path to the photo file
        self.file_path = file_path
        self.formatter = Formatter()

    def extract_metadata(self):
        # Extract metadata from the photo file
        try:
            with open(self.file_path, 'rb') as f:
                # Read the EXIF data from the file
                tags = exifread.process_file(f)
                metadata = {}
                
                metadata['File Size'] = self.formatter.format_size(os.path.getsize(self.file_path))
                metadata['Camera Make'] = tags.get('Image Make')
                metadata['Camera Model'] = tags.get('Image Model')
                metadata['Date and Time'] = tags.get('EXIF DateTimeOriginal')
                metadata['Resolution'] = f"{tags.get('EXIF ExifImageLength')} x {tags.get('EXIF ExifImageWidth')}"
                metadata['Compression'] = tags.get('Thumbnail Compression')
                metadata['LensMake'] = tags.get('EXIF LensMake')
                metadata['LensModel'] = tags.get('EXIF LensModel')
                
                gps_latitude = tags.get('GPS GPSLatitude')
                gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
                gps_longitude = tags.get('GPS GPSLongitude')
                gps_longitude_ref = tags.get('GPS GPSLongitudeRef')

                if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                    gps_latitude_degrees, gps_latitude_minutes, gps_latitude_seconds = gps_latitude.values
                    gps_longitude_degrees, gps_longitude_minutes, gps_longitude_seconds = gps_longitude.values

                    gps_latitude_dmm = self.formatter.convert_gps(gps_latitude_degrees, gps_latitude_minutes, gps_latitude_seconds, gps_latitude_ref)
                    gps_longitude_dmm = self.formatter.convert_gps(gps_longitude_degrees, gps_longitude_minutes, gps_longitude_seconds, gps_longitude_ref)

                    metadata['GPS Coordinates'] = f"{gps_latitude_dmm}, {gps_longitude_dmm}"
                else:
                    metadata['GPS Coordinates'] = 'GPS Not Available'
                
                metadata['SceneType'] = tags.get('EXIF SceneType')
                metadata['SceneCaptureType'] = tags.get('EXIF SceneCaptureType')
                
                metadata['ISO'] = tags.get('EXIF ISOSpeedRatings')
                metadata['Exposure Time'] = self.formatter.format_exposure_time(tags.get('EXIF ExposureTime').values[0])
                metadata['Exposure Program'] = tags.get('EXIF ExposureProgram')
                metadata['ExposureBiasValue'] = tags.get('EXIF ExposureBiasValue')
                metadata['ExposureMode'] = tags.get('EXIF ExposureMode')
                
                
                metadata['Thumbnail ResolutionUnit'] = tags.get('Thumbnail ResolutionUnit')
                metadata['Thumbnail JPEGInterchangeFormat'] = tags.get('Thumbnail JPEGInterchangeFormat')
                metadata['Thumbnail JPEGInterchangeFormatLength'] = tags.get('Thumbnail JPEGInterchangeFormatLength')
                metadata['FNumber'] = tags.get('EXIF FNumber')

                metadata['ExifVersion'] = tags.get('EXIF ExifVersion')
                metadata['OffsetTime'] = tags.get('EXIF OffsetTime')
                metadata['ComponentsConfiguration'] = tags.get('EXIF ComponentsConfiguration')
                metadata['ShutterSpeedValue'] = self.formatter.format_shutter_speed(tags.get('EXIF ShutterSpeedValue'))
                metadata['ApertureValue'] = self.formatter.format_aperture_value(tags.get('EXIF ApertureValue'))
                metadata['BrightnessValue'] = self.formatter.format_brightness_value(tags.get('EXIF BrightnessValue'))
                metadata['MeteringMode'] = tags.get('EXIF MeteringMode')
                metadata['Flash'] = tags.get('EXIF Flash')
                metadata['FocalLength'] = self.formatter.format_focal_length(tags.get('EXIF FocalLength'))
                metadata['FlashPixVersion'] = tags.get('EXIF FlashPixVersion')
                metadata['ColorSpace'] = tags.get('EXIF ColorSpace')
                metadata['SensingMethod'] = tags.get('EXIF SensingMethod')
                metadata['WhiteBalance'] = tags.get('EXIF WhiteBalance')
                metadata['FocalLengthIn35mmFilm'] = tags.get('EXIF FocalLengthIn35mmFilm')
                return metadata

        except IOError as e:
            # Handle file reading errors
            print(f'Error reading file {self.file_path}: {e}')
            return "File Error"
        except exifread.errors.ExifReadError as e:
            # Handle EXIF parsing errors
            print(f'Error parsing EXIF data from {self.file_path}: {e}')
            return 'Metadata Not Available'
        except Exception as e:
            # Handle unexpected errors
            print(f'An unexpected error occurred while extracting metadata from {self.file_path}: {e}')
