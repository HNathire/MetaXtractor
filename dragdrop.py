from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QListWidgetItem, QListWidget, QFileDialog
from PyQt5.QtCore import Qt, QFileInfo, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

class DragDropWidget(QWidget):
    
    upload_file_signal = pyqtSignal(str)
    item_removed_signal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Drag and Drop")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create title label
        self.title_label = QLabel("MetaXtractor")
        self.title_label.setFont(QFont("Inter", 40))
        self.title_label.setStyleSheet("background-color: transparent; color: #c7ebec;")
        self.title_label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(self.title_label)
        self.layout.addSpacing(20)

        # Create drop label
        self.drop_label = QLabel("Drag and drop files here or Upload")
        self.drop_label.setFont(QFont("Inter", 12))
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet("background-color: #2a2f33; border: 2px dashed #1a94d6; border-radius: 10px; padding: 45px;")
        self.layout.addWidget(self.drop_label)
        self.layout.addSpacing(20)

        # Create upload button
        self.upload_button = QPushButton("Upload")
        self.upload_button.setFont(QFont("Inter", 10))
        self.upload_button.clicked.connect(self.upload_file)
        self.upload_button.setStyleSheet("background-color: #1a94d6; color: white; border-radius: 10px;")
        self.upload_button.setFixedSize(475, 40)
        self.layout.addWidget(self.upload_button)
        self.layout.addSpacing(20)

        # Create uploaded files listbox
        self.uploaded_files_listbox = QListWidget()
        self.uploaded_files_listbox.setFixedSize(475, 165)
        self.uploaded_files_listbox.setSpacing(2)
        
        self.uploaded_files_listbox.itemDoubleClicked.connect(self.remove_item_on_double_click)
        self.layout.addWidget(self.uploaded_files_listbox)

        # Set styles for listbox using CSS-like selectors
        self.uploaded_files_listbox.setStyleSheet("""
            QListWidget {
                font: 10pt "Roboto";
                border: 2px solid #1a94d6;
                border-radius: 10px;
                background-color: #2a2f33;
                outline: none;
            }
            QListWidget::item {
                background-color: #333333;
                border: 1px solid black;
                border-radius: 10px;
                margin-left: 4px; 
                margin-right: 4px;
                height: 7px;
                padding: 20px;
                outline: none;
            }
            QListWidget::item:hover {
                background-color: #2e96c7;
                border-radius: 10px;
                height: 9px;  
            }
            QListWidget::item:selected {
                background-color: #1a94d6;
                color: white;
                outline: none;
            }
            QListWidget::item::content {
                border-radius: 10px;
            }
        """)
        # Hide scrollbars
        self.uploaded_files_listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.uploaded_files_listbox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Enable drag and drop for the main window
        self.setAcceptDrops(True)
                
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def upload_file(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select files", "", "Supported files (*.docx *.pdf *.xlsx *.pptx *.mp4 *.avi *.mov *.mkv *.mpeg *.jpg *.jpeg *.png)")
        if file_paths:
            for file_path in file_paths:
                if QFileInfo(file_path).isFile() and QFileInfo(file_path).isReadable():
                    self.handle_file_upload(file_path)

    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            file_info = QFileInfo(file_path)
            if file_info.suffix().lower() in ["docx", "pdf", "xlsx", "pptx", "mp4", "avi", "mov", "mkv", "mpeg", "jpg", "jpeg", "png"]:
                files.append(file_path)
        for file in files:
            self.handle_file_upload(file)
            
    def handle_file_upload(self, file_path):
        file_info = QFileInfo(file_path)
        file_name = file_info.fileName()
        if not self.uploaded_files_listbox.findItems(file_name, Qt.MatchExactly):
            item = QListWidgetItem(file_name)
            icon = QIcon("logo.png")
            item.setIcon(icon)
            self.uploaded_files_listbox.addItem(item)
            self.upload_file_signal.emit(file_path)

    def remove_item_on_double_click(self, item):
        row = self.uploaded_files_listbox.row(item)
        self.uploaded_files_listbox.takeItem(row)
        self.item_removed_signal.emit(row)
