import pandas as pd
import os

def combine_last_three_sheets(input_file, output_file):
    """
    Combines the last three sheets of an Excel file into a single sheet 
    and saves the result to a new file.

    Args:
        input_file (str): Path to the input Excel file.
        output_file (str): Path to save the combined output file.
    """
    
    # Load all sheets into a dictionary
    all_sheets = pd.read_excel(input_file, sheet_name=None)

    # Get names of the last three sheets
    last_three_sheet_names = list(all_sheets.keys())[-3:]

    # Combine data from the last three sheets
    combined_data = pd.concat([all_sheets[sheet] for sheet in last_three_sheet_names])
    filtered_rows = []
    for index, row in combined_data.iterrows():
        keep_row = True
        for value in row:
            if isinstance(value, str):  # Check if value is a string
                if "Date" in value.lower() or (  # Check for "Date"
                    value.count("-") == 2 or value.count("/") == 2 or len(value) == 8
                ) and value.replace("-", "").replace("/", "").isdigit():
                    filtered_rows.append(row)
    df = pd.DataFrame(filtered_rows)
    display(df)

    # Write the combined data to a new Excel file with a single sheet
    with pd.ExcelWriter(output_file) as writer:
        df.to_excel(writer, sheet_name='Combined', index=False)

# Folder Paths
excel_folder_path = "./excel"
excel_processed_path = "./excel_processed"

if __name__ == "__main__":

    if not os.path.exists(excel_processed_path):
        os.makedirs(excel_processed_path)
    
    for idx, filename in enumerate(os.listdir(excel_folder_path)):
        if(idx > 0 ):
            break
        input_file_path = os.path.join(excel_folder_path, filename)
        output_file_path = os.path.join(excel_processed_path, filename)
        combine_last_three_sheets(input_file_path, output_file_path)
