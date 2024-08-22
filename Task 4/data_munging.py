import csv
import sqlite3
import os

#Code by Seelam Nandini
def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipping_data_0 (
            origin_warehouse TEXT,
            destination_store TEXT,
            product TEXT,
            on_time TEXT,
            product_quantity INTEGER,
            driver_identifier TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipping_data_1 (
            shipment_identifier TEXT,
            product TEXT,
            on_time TEXT,
            origin_warehouse TEXT,
            destination_store TEXT
        )
    """)

def insert_shipping_data_0(cursor):
    csv_path = '../data/shipping_data_0.csv'
    print(f"Looking for file: {os.path.abspath(csv_path)}")
    if os.path.isfile(csv_path):
        with open(csv_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader) 
            for row in csv_reader:
                if len(row) == 6:  # Ensure correct number of columns
                    origin_warehouse, destination_store, product, on_time, product_quantity, driver_identifier = row
                    cursor.execute("INSERT INTO shipping_data_0 (origin_warehouse, destination_store, product, on_time, product_quantity, driver_identifier) VALUES (?, ?, ?, ?, ?, ?)",
                                   (origin_warehouse, destination_store, product, on_time, product_quantity, driver_identifier))
    else:
        print(f"File not found: {csv_path}")

def insert_shipping_data_2(cursor):
    csv_path_2 = '../data/shipping_data_2.csv'
    csv_path_1 = '../data/shipping_data_1.csv'
    
    print(f"Looking for files: {os.path.abspath(csv_path_2)}, {os.path.abspath(csv_path_1)}")
    if os.path.isfile(csv_path_2) and os.path.isfile(csv_path_1):
        with open(csv_path_2, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  
            shipping_data_2_rows = [row for row in csv_reader]
        
        with open(csv_path_1, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  
            for row in csv_reader:
                if len(row) == 3: 
                    shipment_identifier, product, on_time = row
                    matching_rows = [r for r in shipping_data_2_rows if r[0] == shipment_identifier]
                    if matching_rows:
                        origin_warehouse, destination_store, driver_identifier = matching_rows[0][1], matching_rows[0][2], matching_rows[0][3]
                        cursor.execute("INSERT INTO shipping_data_1 (shipment_identifier, product, on_time, origin_warehouse, destination_store) VALUES (?, ?, ?, ?, ?)",
                                       (shipment_identifier, product, on_time, origin_warehouse, destination_store))
    else:
        print(f"One or both files not found: {csv_path_2}, {csv_path_1}")

if __name__ == "__main__":
    conn = sqlite3.connect('../shipment_database.db')
    cursor = conn.cursor()

    create_tables(cursor)  # Create the necessary tables

    insert_shipping_data_0(cursor)
    insert_shipping_data_2(cursor)

    conn.commit()
    conn.close()

    print("Data successfully inserted into the database.")



