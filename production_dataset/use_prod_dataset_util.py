import pandas as pd

def load_csv_to_sql(connection, csv_filename, insert_string):

    df = pd.read_csv(csv_filename)
    cursor = connection.cursor()

    for index, row in df.iterrows():
        try:
            cursor.execute("INSERT INTO " + insert_string,
                            row.to_list())
        except:
            print(row)

def run_command_from_string(connection, command, printOutput=False):
    cursor = connection.cursor()
    cursor.execute(command)

    if printOutput:
        rows = cursor.fetchall()
        df = pd.DataFrame(rows)
        print(df)

def run_command_from_file(connection, input_filename, output_filename=None, printOutput=True):
    cursor = connection.cursor()

    with open(input_filename) as f:
        cursor.execute(f.read())

    rows = cursor.fetchall()
    field_names = [i[0] for i in cursor.description]

    if printOutput:
        df = pd.DataFrame(rows, columns=field_names)
        print(df)

    if output_filename is not None:
        df = pd.DataFrame(rows, columns=field_names)
        output_filename = df.to_csv(output_filename, index=False)