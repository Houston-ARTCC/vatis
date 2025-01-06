import json
import glob
import os
from datetime import datetime


parent_directory = os.path.join(os.getcwd(), "..")
files_in_parent = os.listdir(parent_directory)
json_files = [f for f in files_in_parent if f.endswith('.json')]
current_date = str(datetime.now().strftime('%Y%m%d'))


for json_file_name in json_files:
    json_file = "../" + json_file_name
    with open(json_file, 'r') as file:
        print(f"Working on {json_file}")
        #Parse JSON
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {json_file}: {e}")

    # Set initial release to 0
    release_number = 0
    # Grab file's current serial
    serial_value = str(data["updateSerial"])
    
    print(f"serial is: {serial_value}")
    print(f"serial comparison is: {serial_value[:8]}")
    print(f"date comparison value is {current_date}")
    # If the YYYYMMDD matches today, grab the last two digits and increment
    if serial_value[:8] == current_date:
        last_two_digits = int(serial_value[-2:])
        print(f"last two digits are: {last_two_digits}")
        last_two_digits = last_two_digits + 1
        release_number = last_two_digits
        print(f"new last two digits: {last_two_digits}")

        # If more than 99 updates in a day on this file, we need to bomb out loudly
        if last_two_digits > 99:
            print(f"Update count exceedes 99, unable to continue!")
            exit(1)


    # Pad the release number to 2 digits and combine with date, convert to int for JSON
    formatted_release_number = str(f"{release_number:02d}")
    release_serial_str = current_date + formatted_release_number
    release_serial_int = int(release_serial_str)
    print(f"new serial is {release_serial_int}")
    data["updateSerial"] = release_serial_int

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)
        print(f"wrote {json_file}")

print(f"End of run")

