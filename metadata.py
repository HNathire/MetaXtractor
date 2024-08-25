import os
import concurrent.futures
import cachetools
import threading
from document import DocumentMetadata
from photo import PhotoMetadata
from video import VideoMetadata

class MetadataExtractor:
    # Initialize MetadataExtractor with a list of file paths
    def __init__(self, file_paths: list):
        self.file_paths = file_paths
        self.extension_map = {
            '.docx': DocumentMetadata,
            '.pdf': DocumentMetadata,
            '.xlsx': DocumentMetadata,
            '.pptx': DocumentMetadata,
            '.mp4': VideoMetadata,
            '.avi': VideoMetadata,
            '.mov': VideoMetadata,
            '.mkv': VideoMetadata,
            '.mpeg': VideoMetadata,
            '.jpg': PhotoMetadata,
            '.jpeg': PhotoMetadata,
            '.png': PhotoMetadata,
        }
        self.cache = cachetools.TTLCache(maxsize=100, ttl=60)  # 1-minute TTL
        self.lock = threading.RLock()  # Create a thread-local lock

    @staticmethod
    def replace_none_with_default(metadata: dict) -> dict:
        """Replace None values with 'Not Available' and handle other types of metadata values"""
        if metadata is None:
            return {}
        normalized_metadata = {}
        for key, value in metadata.items():
            if value is None:
                normalized_metadata[key] = "Not Available"
            elif isinstance(value, str) and value.strip() == "":
                normalized_metadata[key] = "Not Available"
            elif isinstance(value, list) and len(value) == 0:
                normalized_metadata[key] = "Not Available"
            elif isinstance(value, dict) and len(value) == 0:
                normalized_metadata[key] = "Not Available"
            else:
                normalized_metadata[key] = value
        return normalized_metadata
    
    # Extract metadata from files in parallel using ThreadPoolExecutor
    def extract_metadata(self) -> dict:
        metadata_dict = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._extract_metadata, file_path): file_path for file_path in self.file_paths}
            for future in concurrent.futures.as_completed(futures):
                file_path = futures[future]
                try:
                    metadata = future.result()
                    metadata_dict[file_path] = self.replace_none_with_default(metadata)
                except Exception as e:
                    metadata_dict[file_path] = {'error': str(e)}
                    self.cache[file_path] = {'error': str(e)}  
        return metadata_dict
    
    #Extract metadata from a single file
    def _extract_metadata(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            return {'error': f"File not found: {file_path}"}

        file_extension = os.path.splitext(file_path)[1].lower()
        # Check if metadata is cached
        with self.lock:  # Synchronize cache access
            cached_metadata = self.cache.get(file_path)
            if cached_metadata:
                return cached_metadata

        # Select the appropriate metadata extractor based on file extension
        extractor = self.extension_map.get(file_extension)
        if extractor:
            try:
                if extractor == VideoMetadata:
                    video_extractor = extractor(file_path)
                    media_info = video_extractor.parse_video_file()
                    metadata = video_extractor.extract_metadata(media_info)
                    with self.lock:  # Synchronize cache update
                        self.cache[file_path] = metadata
                    return metadata
                else:
                    metadata_extractor = extractor(file_path)
                    metadata = metadata_extractor.extract_metadata()
                    with self.lock:  # Synchronize cache update
                        self.cache[file_path] = metadata
                    return metadata
            except Exception as e:
                return {'error': str(e)}
        else:
            return {'error': f"Unsupported file type: {file_extension}"}