import csv
import firebase_admin
from firebase_admin import credentials, db
from collections import defaultdict

class Database:
    # Class variable to store the Firebase app instance
    _app = None

    def __init__(self, chunk_size=1000):
        # Initialize the Firebase app instance if it doesn't exist
        if not Database._app:
            try:
                # Load the Firebase credentials from a JSON file
                self.cred = credentials.Certificate('C:/Users/Hackz/metaxtractor-firebase-adminsdk-5tt9b-14a71ade5e.json')
                # Initialize the Firebase app with the credentials and database URL
                Database._app = firebase_admin.initialize_app(self.cred, {
                    'databaseURL': 'https://metaxtractor-default-rtdb.asia-southeast1.firebasedatabase.app/your_database_path'
                })
            except Exception as e:
                # Raise an exception if there's an error initializing Firebase
                raise Exception(f"Error initializing Firebase: {e}")
            # Set the chunk size for processing CSV data
        self.chunk_size = chunk_size

    def send_data_to_firebase(self, file_path):
        try:
            # Open the CSV file for reading
            with open(file_path, 'r') as csvfile:
                # Create a CSV reader object
                reader = csv.reader(csvfile)
                data = []
                # Iterate over the CSV rows
                for i, row in enumerate(reader):
                    # Append the row to the data list
                    data.append(row)
                    # If the data list has reached the chunk size, process it
                    if (i + 1) % self.chunk_size == 0:
                        self.process_chunk(data)
                        # Reset the data list
                        data = []
                # Process any remaining data in the list
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
            # Get a reference to the Firebase Realtime Database
            ref = db.reference('Metadata Analysis')
            # Initialize a dictionary to store the batch data
            batch_data = defaultdict(dict)
            # Iterate over the data rows
            for row in data:
                try:
                    # Extract the file name from the first row
                    if row[0] == "File:":
                        file_name = row[1].replace('.', '-')
                    # Extract the metadata key-value pairs from the remaining rows
                    elif row[0]!= "" and row[1]!= "":
                        batch_data[file_name][row[0]] = row[1]
                except Exception as e:
                    print(f"Error processing chunk: {e}. Skipping row: {row}")
                    continue
            # Update the Firebase database with the batch data
            if batch_data:
                ref.update(dict(batch_data))
        except db.DatabaseError as e:
            print(f"Error updating Firebase database: {e}")
        except Exception as e:
            print(f"Error processing chunk: {e}")