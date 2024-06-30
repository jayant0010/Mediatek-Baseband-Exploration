import re
import pickle

# Load the dictionary of dictionaries from the pickle file
with open('MTK_SPACE_DICT_Data.pkl', 'rb') as f:
    my_dict = pickle.load(f)

# Print the key and word inside parentheses for each value2 that matches the criteria
for key1, value1 in my_dict.items():
    word = None
    for key2, value2 in value1.items():
        if isinstance(value2, str):
            match = re.search(r'TEST_MSG_ID: (\d+)\n\[(.*?)\]', value2)
            if match:
                word = match.group(2)
        elif isinstance(value2, list):
            for item in value2:
                if isinstance(item, str) and "(Crashed)" not in item:
                    match = re.search(r'TEST_MSG_ID: (\d+)\n\[(.*?)\]', item)
                    if match:
                        word = match.group(2)
    if word and "testtas" not in word:
        print(f"{key1}: {word}")
