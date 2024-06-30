import re
import pickle

# Load the dictionary of dictionaries from the pickle file
with open('MTK_SPACE_DICT_Data.pkl', 'rb') as f:
    my_dict = pickle.load(f)

# Dictionary to keep track of the count for each key1
key1_counts = {}

# Print key1, key2, and value2 for each value2 that matches the criteria
for key1, value1 in my_dict.items():
    # Initialize the count for this key1 to 0
    key1_count = 0
    for key2, value2 in value1.items():
        if isinstance(value2, list) and len(value2) > 3 and any("(Crashed)" in item for item in value2):
            print(f"key1: {key1} | key2: {key2} | value2: {value2}")
            print("\n")
            print("\n")
            print("\n")
            # Count the number of times "(Crashed)" appears in value2
            crashed_count = sum(1 for item in value2 if "(Crashed)" in item)
            key1_count += crashed_count
    if key1_count > 0:
        # Add the count for this key1 to the dictionary
        key1_counts[key1] = key1_counts.get(key1, 0) + key1_count

# Print the report for all key1 values in ascending order
print("Counts for all key1 values:")
for key1, count in sorted(key1_counts.items()):
    print(f"key1 {key1}: {count} instances")

# Print the report for key1 values in the specified list
print("\nCounts for key1 values in the list:")
for key1 in [8, 758, 178, 198, 228, 238, 268, 278, 58, 418, 438, 448, 458, 468, 128, 7, 297, 417, 427, 437, 447, 457, 467, 757, 127, 177, 197, 227, 237, 267, 277, 735, 775, 175, 415, 425, 435, 445, 455, 465, 235, 275, 295, 835, 431, 441, 451, 461, 201, 211, 221, 231, 181, 751, 251, 750, 760, 270, 430, 440, 450, 460, 180, 190, 200, 210, 220, 230, 752, 322, 382, 152, 182]:
    count = key1_counts.get(key1, 0)
    print(f"key1 {key1}: {count} instances")
