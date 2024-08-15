import csv
import firebase_admin
from firebase_admin import credentials, db
from collections import defaultdict

class Database:
    _app = None

    def __init__(self, chunk_size=1000):
        if not Database._app:
            try:
                self.cred = credentials.Certificate('C:/Users/Hackz/metaxtractor-firebase-adminsdk-5tt9b-14a71ade5e.json')
                Database._app = firebase_admin.initialize_app(self.cred, {
                    'databaseURL': 'https://metaxtractor-default-rtdb.asia-southeast1.firebasedatabase.app/your_database_path'
                })
            except Exception as e:
                raise Exception(f"Error initializing Firebase: {e}")
        self.chunk_size = chunk_size

    def send_data_to_firebase(self, file_path):
        try:
            with open(file_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = []
                for i, row in enumerate(reader):
                    data.append(row)
                    if (i + 1) % self.chunk_size == 0:
                        self.process_chunk(data)
                        data = []
                if data:
                    self.process_chunk(data)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")
        except Exception as e:
            print(f"Error sending data to Firebase: {e}")

    def process_chunk(self, data):
        try:
            ref = db.reference('Metadata Analysis')
            batch_data = defaultdict(dict)
            for row in data:
                try:
                    if row[0] == "File:":
                        file_name = row[1].replace('.', '-')
                    elif row[0]!= "" and row[1]!= "":
                        batch_data[file_name][row[0]] = row[1]
                except Exception as e:
                    print(f"Error processing chunk: {e}. Skipping row: {row}")
                    continue
            if batch_data:
                ref.update(dict(batch_data))
        except db.DatabaseError as e:
            print(f"Error updating Firebase database: {e}")
        except Exception as e:
            print(f"Error processing chunk: {e}")