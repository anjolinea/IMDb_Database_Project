import sqlite3
import pandas as pd

def load_csv_to_sql(connection, csv_filename, insert_string):

    df = pd.read_csv(csv_filename)
    cursor = connection.cursor()

    for index, row in df.iterrows():
        cursor.execute("INSERT INTO " + insert_string,
                        row.to_list())
        
def run_command_view_output(connection, command):
    cursor = connection.cursor()
    cursor.execute(command)

    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    print(df)

def run_command(connection, command):
    cursor = connection.cursor()
    cursor.execute(command)