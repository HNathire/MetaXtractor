import csv
import os
from database import Database
from metadata import MetadataExtractor
from dragdrop import DragDropWidget
from PyQt5.QtWidgets import (QSizePolicy,
                             QWidget, 
                             QVBoxLayout, 
                             QHBoxLayout, 
                             QPushButton,  
                             QFileDialog,  
                             QTableWidget,
                             QProgressBar, 
                             QTableWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.file_paths = []
        self.inspected_files = set()  # Set to keep track of inspected files
        self.exported_files = set()  
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MetaXtractor")
        self.setStyleSheet("background-color: #2b2b2b; color: white;")
        self.setFixedSize(1150, 750)
        self.create_frames()
        self.create_left_layout()
        self.create_right_layout()
        self.create_main_layout()

    def create_frames(self):
        self.left_frame = QWidget()
        self.left_frame.setStyleSheet("background-color: #333333; border-radius: 10px;")
        self.right_frame = QWidget()
        self.right_frame.setStyleSheet("background-color: #333333; border-radius: 10px;")

    def create_left_layout(self):
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(20, 20, 20, 20)
        self.left_layout.setSpacing(20)

        # Create a horizontal layout to center the drag drop widget
        drag_drop_layout = QHBoxLayout()
        drag_drop_layout.addStretch(1)
        drag_drop_layout.addWidget(self.create_drag_drop_widget())
        drag_drop_layout.addStretch(1)
        self.left_layout.addLayout(drag_drop_layout)

        # Create a horizontal layout to center the loading bar
        loading_bar_layout = QHBoxLayout()
        loading_bar_layout.addStretch(1)

        # Customize the progress bar layout and display
        self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0, 100)
        self.loading_bar.setValue(0)
        self.loading_bar.setTextVisible(True)
        self.loading_bar.setFormat("")
        self.loading_bar.setStyleSheet("""
            QProgressBar {
            border: 2px solid #1a94d6;
            border-radius: 10px;
            text-align: center;
            font: 10pt "Open Sans";
            background-color: transparent;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
            border-radius: 10px;
        }   
        """)
        
        self.loading_bar.setFixedSize(470, 35)
        loading_bar_layout.addWidget(self.loading_bar)
        loading_bar_layout.addStretch(1)
        self.left_layout.addLayout(loading_bar_layout)
        
        # Create a horizontal layout to center the buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addLayout(self.create_button_layout())
        button_layout.addStretch(1)
        self.left_layout.addLayout(button_layout)

        # Create a horizontal layout to center the clear and export buttons
        clear_export_layout = QHBoxLayout()
        clear_export_layout.addStretch(1)
        clear_export_layout.addLayout(self.create_clear_export_layout())
        clear_export_layout.addStretch(1)
        self.left_layout.addLayout(clear_export_layout)

        self.left_frame.setLayout(self.left_layout)
        return self.left_layout
     
    def create_right_layout(self):
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(20, 20, 20, 20)
        self.right_layout.setSpacing(20)
        self.right_layout.addWidget(self.create_data_table())
        self.right_frame.setLayout(self.right_layout)

    def create_main_layout(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        self.main_layout.addWidget(self.left_frame)
        self.main_layout.addWidget(self.right_frame)
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 1)
        self.setLayout(self.main_layout)

    def create_drag_drop_widget(self):
        self.drag_drop_widget = DragDropWidget()
        self.drag_drop_widget.upload_file_signal.connect(self.add_file)
        self.drag_drop_widget.setFixedSize(500, 500)
        self.drag_drop_widget.setStyleSheet("background-color: #444444; border-radius: 10px;")
        return self.drag_drop_widget

    def create_button(self, text, slot=None):
        button = QPushButton(text)
        button.setFixedSize(225, 40)
        font = QFont("Inter", 10)
        button.setFont(font)
        button.setStyleSheet("background-color: #1a94d6; color: white; border-radius: 10px;")
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        if slot:
            button.clicked.connect(slot)
        return button

    def create_button_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        buttons = [
            {"text": "Inspect", "slot": self.inspect_files},
            {"text": "Export to Database", "slot": self.export_to_database},  
        ]
        for button in buttons:
            btn = self.create_button(button["text"], button["slot"])
            if button["text"] == "Inspect":
                self.inspect_button = btn
                self.inspect_button.setEnabled(False)  # Disable the button by default
            elif button["text"] == "Export to Database":
                self.export_button = btn
                self.export_button.setEnabled(False)  # Disable the button by default
            layout.addWidget(btn)
        return layout

    def create_clear_export_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        buttons = [
            {"text": "Clear", "slot": self.clear_all},
            {"text": "Export to File", "slot": self.export_to_file},
        ]
        for button in buttons:
            btn = self.create_button(button["text"], button["slot"])
            if button["text"] == "Export to File":
                self.export_file_button = btn
                self.export_file_button.setEnabled(False)  # Disable the button by default
            layout.addWidget(btn)
        return layout

    def create_data_table(self):
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderItem(0, QTableWidgetItem("Tag Name"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("Value"))
        widths = [180, 360]  
        for i, width in enumerate(widths):
            table.setColumnWidth(i, width)
        table.verticalHeader().setVisible(False)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #2a2f33;
                border: 3px solid #1a94d6;
                border-radius: 10px;
                font: 10pt "Open Sans";
                outline: none;
            }
            QTableWidget::item {
                border: none;
                padding: 10px;
                outline: none;
            }
            QTableWidget::item:selected {
                background-color: #1a94d6;
                color: white;
                outline: none;
            }
            QHeaderView::section {
                background-color: #1a94d6;
                color: white;
                padding: 5px;
                text-align: left;
                font: 10pt "Open Sans";
                border: none;
                outline: none;
            }
        """)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return table
    
    def inspect_files(self):
        """
        Inspect files and extract metadata.
        """
        new_files = [file_path for file_path in self.file_paths if file_path not in self.inspected_files]
        if not new_files:
            self._handle_error("No new files to inspect.")
            self.inspect_button.setEnabled(False)  # Disable the inspect button
            return

        self.loading_bar.setValue(0)
        self.loading_bar.setFormat("Inspecting files...")
        self.loading_bar.setTextVisible(True)

        try:
            metadata_extractor = MetadataExtractor(new_files)
            metadata_dict = metadata_extractor.extract_metadata()  # Call the function
            table_data = []
            total_files = len(new_files)

            for i, (file_path, metadata) in enumerate(metadata_dict.items()):
                # Add file path to table data
                table_data.append(("File:", os.path.basename(file_path)))

                # Add metadata to table data
                for key, value in metadata.items():
                    table_data.append((key, value))

                # Add a blank line after all metadata for a file has been extracted
                table_data.append(("", ""))

                # Update progress bar
                progress = int((i + 1) / total_files * 100)
                self.loading_bar.setValue(progress)
                self.loading_bar.setFormat(f"Inspecting files... ({progress}%)")

                # Mark the file as inspected
                self.inspected_files.add(file_path)

            self.update_table(table_data)
            self.loading_bar.setFormat("Done!")
            self.loading_bar.setValue(100)
            self.export_button.setEnabled(True)
        except RuntimeError as e:
            self._handle_error(f"Error inspecting files: {str(e)}")
           
    def export_to_database(self):
        """
        Export data to Firebase Realtime Database.
        """
        new_files = [file_path for file_path in self.file_paths if file_path not in self.exported_files]
        if not new_files:
            self._handle_error("No new files to export.")
            self.export_button.setEnabled(False)  # Disable the export button
            return

        self.loading_bar.setValue(0)
        self.loading_bar.setFormat("Exporting to database...")
        self.loading_bar.setTextVisible(True)

        try:
            rows = self._prepare_data_for_export()
            if rows is None:
                self._handle_error("Error preparing data")
                return

            temp_file_path = "temp.csv"

            with open(temp_file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)

            database = Database()
            total_files = len(new_files)
            for i, file_path in enumerate(new_files):
                try:
                    database.send_data_to_firebase(temp_file_path)
                    self._update_progress_bar(int((i + 1) / total_files * 100), f"Exporting to database... ({int((i + 1) / total_files * 100)}%)")
                    self.exported_files.add(file_path)
                except Exception as e:
                    self._handle_error(f"Error sending data to Firebase: {str(e)}")
            self._remove_temp_file(temp_file_path)
            self.loading_bar.setFormat("Done!")
            self.loading_bar.setValue(100)
        except RuntimeError as e:
            self._handle_error(f"Error exporting to database: {str(e)}")


    def _update_progress_bar(self, value, format):
        self.loading_bar.setValue(value)
        self.loading_bar.setFormat(format)


    def update_table(self, table_data):
        table = self.right_layout.itemAt(0).widget()
        table.setRowCount(len(table_data))

        for row, (key, value) in enumerate(table_data):
            font = QFont("Roboto", 10)
            if key == "File:":
                font.setBold(True)

            key_item = QTableWidgetItem(key)
            key_item.setFont(font)
            key_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Left align the text
            table.setItem(row, 0, key_item)

            value_item = QTableWidgetItem(str(value))
            value_item.setFont(font)
            table.setItem(row, 1, value_item)
            
        if len(table_data) > 4:
            self.export_button.setEnabled(True)
            self.export_file_button.setEnabled(True)
        else:
            self.export_button.setEnabled(False)
            self.export_file_button.setEnabled(False)
            
    def add_file(self, file_path):
        self.file_paths.append(file_path)
        # Reset the flags for the new file
        self.inspected_files.discard(file_path)
        self.exported_files.discard(file_path)
        if self.file_paths:  # If there are files in the list
            self.inspect_button.setEnabled(True)  # Enable the inspect button
            
    def _prepare_data_for_export(self):
        table = self.right_layout.itemAt(0).widget()
        rows = []
        file_name = None

        for row in range(table.rowCount()):
            row_data = [item.text() if item else "" for item in [table.item(row, column) for column in range(table.columnCount())]]
            if row_data and row_data[0] == "File:":
                file_name = row_data[1]
            rows.append(row_data)
        return rows

    def export_to_file(self):
        """Export data to a file."""
        rows = self._prepare_data_for_export()
        if not rows:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
            self.update_table([("Success:", "Data exported to file successfully.")])
            self.data_exported_to_file = True  # Set the flag to True
            self.export_button.setEnabled(False)  # Disable the export to database button
    
    def _write_data_to_csv(self, rows, file_path):
        """Write data to a CSV file."""
        if os.path.exists(file_path):
            file_name, file_extension = os.path.splitext(file_path)
            i = 1
            while os.path.exists(file_path):
                file_path = f"{file_name}_{i}{file_extension}"
                i += 1
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
            
    def _remove_temp_file(self, file_path):
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                self._handle_error(f"Error removing temporary CSV file: {str(e)}")
        else:
            self._handle_error(f"File not found: '{file_path}'")

    def _handle_error(self, error_message):
        """
        Handle errors by displaying an error message and logging the error.
        """
        print(error_message)
        self.loading_bar.setFormat("Error: " + error_message)
        self.loading_bar.setTextVisible(True)
        self.loading_bar.setValue(0)  # Reset the progress bar value
                  
    def clear_all(self):
        self.right_layout.itemAt(0).widget().setRowCount(0)  # Clear the table
        self.export_button.setEnabled(False)  # Disable the export buttons
        self.export_file_button.setEnabled(False)
        self.data_exported_to_file = False  # Reset the flag
        self.update_table([])  # Clear the table data
        self.file_paths = []  # Clear the file paths
        self.drag_drop_widget.uploaded_files_listbox.clear()  # Clear the uploaded files listbox
        self.inspect_button.setEnabled(False)  # Disable the inspect button
        self.loading_bar.setValue(0)  # Reset the progress bar
        self.loading_bar.setFormat("")  # Clear the progress bar text
        self.inspected_files.clear()
        self.exported_files.clear()
        
