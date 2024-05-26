import json
from datetime import datetime

# Function to read the ICD data from the file
def read_icd_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

# Function to create the JSON structure
def create_icd_json(icd_data):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    icd_list = []
    
    for pk, line in enumerate(icd_data, start=1):
        code, description = line.split(' ', 1)
        icd_object = {
            "model": "avey.icd",
            "pk": pk,
            "fields": {
                "code": code.strip(),
                "description": description.strip(),
                "time_created": current_time,
                "time_updated": current_time
            }
        }
        icd_list.append(icd_object)
    
    return icd_list

def create_icd_json(icd_data):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    icd_list = []
    
    for pk, line in enumerate(icd_data, start=1):
        code, description = line.split(' ', 1)
        code = code.strip()
        description = description.strip()
        
        # Determine the type based on the first letter of the code
        type_attr = "SYMPTOM" if code[0] == "R" else "DIAGNOSIS"
        
        # Add a "." between the third and fourth characters if the code is longer than 3 characters
        if len(code) > 3:
            code = code[:3] + '.' + code[3:]
        
        icd_object = {
            "model": "avey.icd",
            "pk": pk,
            "fields": {
                "code": code,
                "description": description,
                "type": type_attr,
                "time_created": current_time,
                "time_updated": current_time
            }
        }
        icd_list.append(icd_object)
    
    return icd_list

# Main function to read the file and generate the JSON output
def main():
    file_path = '/Users/abdallamohamed/Desktop/Avey/fixtures/src/input/icd10cm-codes-April-2024.txt'
    icd_data = read_icd_file(file_path)
    icd_json = create_icd_json(icd_data)
    
    # Output the JSON to a file
    with open('/Users/abdallamohamed/Desktop/Avey/fixtures/src/output/icd_codes.json', 'w') as json_file:
        json.dump(icd_json, json_file, indent=2)

# Run the main function
if __name__ == "__main__":
    main()
