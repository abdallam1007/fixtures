import csv
import json
from datetime import datetime

# Function to read the MUE policy files and create a dictionary for quick lookup
def load_mue_policies(file_paths):
    mue_data = {}
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)
            mue_data.update(data)
    return mue_data

# Function to read the CPT data from the CSV file
def read_cpt_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# Function to create the JSON structure
def create_cpt_json(cpt_data, mue_data):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    cpt_list = []
    
    for pk, row in enumerate(cpt_data, start=1):
        code = row['CPT Code']
        description = row['Full Descriptor']
        
        # Lookup max_units in the MUE data
        max_units = mue_data.get(code, None)

        cpt_object = {
            "model": "avey.cpt",
            "pk": pk,
            "fields": {
                "code": code,
                "description": description,
                "max_units": max_units,
                "time_quantity": 1,
                "time_unit": "D",
                "time_created": current_time,
                "time_updated": current_time
            }
        }
        cpt_list.append(cpt_object)
    
    return cpt_list

# Main function to read the files and generate the JSON output
def main():
    cpt_file_path = '/Users/abdallamohamed/Desktop/Avey/fixtures/src/input/cpt-base.csv'
    mue_policy_files = ['/Users/abdallamohamed/Desktop/Avey/fixtures/src/input/MUE-policy1.json',
                        '/Users/abdallamohamed/Desktop/Avey/fixtures/src/input/MUE-policy2.json',
                        '/Users/abdallamohamed/Desktop/Avey/fixtures/src/input/MUE-policy3.json']

    # Load MUE policy data
    mue_data = load_mue_policies(mue_policy_files)
    
    # Read CPT data from CSV
    cpt_data = read_cpt_file(cpt_file_path)
    
    # Create CPT JSON
    cpt_json = create_cpt_json(cpt_data, mue_data)
    
    # Output the JSON to a file
    with open('/Users/abdallamohamed/Desktop/Avey/fixtures/src/output/cpt_codes.json', 'w') as json_file:
        json.dump(cpt_json, json_file, indent=2)

# Run the main function
if __name__ == "__main__":
    main()
