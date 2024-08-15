import os
import pikepdf
import docx
import openpyxl
import pptx

# Dictionary to map file extensions to their corresponding types
FILE_EXTENSIONS = {
    
    '.docx': 'word',
    '.pdf': 'pdf',
    '.xlsx': 'excel',
    '.pptx': 'powerpoint'
    
}

# Custom exception for metadata-related errors
class MetadataError(Exception):
    pass

class DocumentMetadata:
    def __init__(self, file_path: str):
         # Initialize the DocumentMetadata object with a file path
        self.file_path = file_path

    def _check_file_exists(self) -> None:
        # Check if the file exists at the specified path
        if not os.path.exists(self.file_path):
            raise MetadataError(f'File not found: {self.file_path}')

    def _determine_file_type(self) -> str:
        # Determine the type of the file based on its extension
        file_extension = os.path.splitext(self.file_path)[1].lower()
        if file_extension not in FILE_EXTENSIONS:
            raise MetadataError(f'Unsupported file type: {file_extension}')
        return FILE_EXTENSIONS[file_extension]

    def extract_metadata(self) -> dict:
        # Extract metadata from the document
        self._check_file_exists()
        file_type = self._determine_file_type()
        method_name = f'{file_type}_metadata'
        method = getattr(self, method_name)
        return method()

    def word_metadata(self) -> dict:
        doc = docx.Document(self.file_path)    

        metadata = {}
        metadata['Author'] = doc.core_properties.author
        metadata['Title'] = doc.core_properties.title
        metadata['Subject'] = doc.core_properties.subject
        metadata['Date Created'] = doc.core_properties.created
        metadata['Date Modified'] = doc.core_properties.modified
        metadata['Revision'] = doc.core_properties.revision
        metadata['Last Printed'] = doc.core_properties.last_printed
        metadata['Category'] = doc.core_properties.category
        metadata['Keywords'] = doc.core_properties.keywords
        metadata['Comments'] = doc.core_properties.comments
        metadata['Version'] = doc.core_properties.version
        metadata['Status'] = doc.core_properties.content_status
        metadata['Page Count'] = len(doc.sections)

        word_count = 0
        for para in doc.paragraphs:
            word_count += len(para.text.split())
        metadata['Word Count'] = word_count
        return metadata

    def pdf_metadata(self) -> dict:
        with pikepdf.Pdf.open(self.file_path) as pdf:
            metadata = {}
            metadata['Author'] = pdf.docinfo.get('/Author', '')
            metadata['Title'] = pdf.docinfo.get('/Title', '')
            metadata['Date Created'] = pdf.docinfo.get('/CreationDate', '')
            metadata['Date Modified'] = pdf.docinfo.get('/ModDate', '')
            metadata['Subject'] = pdf.docinfo.get('/Subject', '')
            metadata['Keywords'] = pdf.docinfo.get('/Keywords', '')
            metadata['PDDocID'] = pdf.docinfo.get('/ID', '')
            metadata['PDFVersion'] = pdf.pdf_version
            metadata['Page Count'] = len(pdf.pages)
            return metadata  


    def excel_metadata(self) -> dict: 
        excel = openpyxl.load_workbook(self.file_path)   

        metadata = {}
        metadata['Author'] = excel.properties.creator
        metadata['Title'] = excel.properties.title
        metadata['Date Created'] = excel.properties.created
        metadata['Date Modified'] = excel.properties.modified
        metadata['Sheet Count'] = len(excel.worksheets)
        metadata['Row Count'] = excel.active.max_row
        metadata['Column Count'] = excel.active.max_column
        return metadata

    def powerpoint_metadata(self) -> dict:
        ppt = pptx.Presentation(self.file_path)
            
        metadata = {}
        metadata['Author'] = ppt.core_properties.author
        metadata['Title'] = ppt.core_properties.title
        metadata['Subject'] = ppt.core_properties.subject
        metadata['Date Created'] = ppt.core_properties.created
        metadata['Date Modified'] = ppt.core_properties.modified
        metadata['Slide Count'] = len(ppt.slides)
        return metadata


    def __str__(self) -> str:
        # Return a string representation of the metadata
        return str(self.extract_metadata())

    def __repr__(self) -> str:
        # Return a representation of the DocumentMetadata object
        return f"DocumentMetadata('{self.file_path}')"
