import pickle

# Load the dictionary of dictionaries from the pickle file
with open('MTK_SPACE_DICT_Data.pkl', 'rb') as f:
    my_dict = pickle.load(f)

# Print the tuple structure of the dictionary of dictionaries
for key1, value1 in my_dict.items():
    print(f"Key 1: {key1}")
    print("\n")
    print("\n")

    for key2, value2 in value1.items():
        if "(Crashed)" not in value2:
            print(f"\tKey 2: {key2}, Value: {value2}")
            print("\n")
