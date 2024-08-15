from pymediainfo import MediaInfo
from formatter import Formatter

class VideoMetadata:
    def __init__(self, video_file):
        # Initialize the video file path and formatter object
        self.video_file = video_file
        self.formatter = Formatter()
        
    # Parse the video file using MediaInfo
    def parse_video_file(self):
        try:
            # Return the parsed media info object
            return MediaInfo.parse(self.video_file)
        except Exception as e:
            # Raise an error if parsing fails
            raise ValueError(f"Error parsing video file: {e}")
        
    # Extract metadata from the parsed media info object
    def extract_metadata(self, media_info):
        try:
            # Initialize an empty metadata dictionary
            metadata = {}
            
            # Iterate through each track in the media info object
            for track in media_info.tracks:
                if track.track_type == 'General':
                    metadata['Count'] = track.count
                    metadata['File Size'] = self.formatter.format_size(track.file_size)
                    metadata['Format'] = track.format
                    metadata['Duration'] = self.formatter.format_duration(track.duration / 1000)
                if track.comapplequicktimelocationiso6709 is not None:
                    metadata['Location'] = self.formatter.format_gps(track.comapplequicktimelocationiso6709)
                    metadata['Creation Date'] = track.file_creation_date    
                    metadata['Modification Date'] = track.file_last_modification_date
                    metadata['Writing Library'] = track.writing_library
                    metadata['Encoded Date'] = track.encoded_date
                    metadata['Tagged Date'] = track.tagged_date               
                    metadata['Device Make'] = track.comapplequicktimemake
                    metadata['Device Model'] = track.comapplequicktimemodel
                    metadata['Device Version'] = track.comapplequicktimesoftware
                    
                elif track.track_type == 'Video':
                    metadata['Video Format'] = track.format
                    metadata['Video Format Info'] = track.format_info
                    metadata['Format Profile'] = track.format_profile
                    metadata['Internet Media Type'] = track.internet_media_type
                    
                    metadata['Video Codec'] = track.codec_id
                    metadata['Resolution'] = f"{track.sampled_width}x{track.sampled_height}"
                    metadata['Framerate'] = self.formatter.format_framerate(track.frame_rate)
                    metadata['Bit Depth'] = track.bit_depth
                    metadata['Frame Count'] = track.frame_count
                    metadata['Stream Count'] = track.stream_count
                    
                elif track.track_type == 'Audio':
                    metadata['Audio Format'] = track.format
                    metadata['Audio Format Info'] = track.format_info
                    metadata['Audio Codec'] = track.codec_id
                    metadata['Audio Bitrate'] = self.formatter.format_bitrate(track.bit_rate)
                    metadata['Audio Channels'] = track.channel_s
                    metadata['Audio Sample Rate'] = self.formatter.format_samplerate(track.sampling_rate)
                    metadata['Compression Mode'] = track.compression_mode

            # Return the extracted metadata dictionary
            return metadata
        
        except AttributeError as e:
            # Raise an error if attribute extraction fails
            raise ValueError(f"Error extracting metadata: {e}")