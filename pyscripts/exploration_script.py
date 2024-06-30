import subprocess
import socket
import time
import select
import sys
import time
import os
import random
import signal
import psutil

def timeouthandler(signum, frame):
    raise Exception("Timeout: 1000 seconds has elapsed. This values are making the FirmWire hang.")

signal.signal(signal.SIGALRM, timeouthandler)


# Set the command and arguments for the make clean command
clean_command = "make -C modkit/mtk clean >/dev/null 2>&1"

# Set the command and arguments for the make command
make_command = "make -C modkit/mtk >/dev/null 2>&1"

# Run the make clean command and capture its output
t_start = time.time() 
clean_process = os.popen(clean_command)
_ = clean_process.read()
t_end = time.time()
print(f"make clean took {abs(t_start - t_end)} sec")

# Run the make command and capture its output
t_start = time.time() 
make_process = os.popen(make_command)
_ = make_process.read()
t_end = time.time()
print(f"make took {abs(t_start - t_end)} sec")

# Set the command and arguments for the Python script
firmwire_command = ["python3", "firmwire.py", "images/CP_A415FXXU1BUA1_CP17952712_CL20194519_QB37484013_REV00_user_low_ship_MULTI_CERT/md1img.img", "--mtk-loader-nv_data", "images/CP_A415FXXU1BUA1_CP17952712_CL20194519_QB37484013_REV00_user_low_ship_MULTI_CERT/mnt/", "-t", "msg_inject_test"]

# Set the number of times to run the firmware command
num_runs = 10000

# Set the timeout for readline
readline_timeout = 200
cur_task_id = -1
cur_task_id_inst_index = 0
end_condition = False
# Run the command multiple times
while(not end_condition):
    # Print a message indicating the start of the firmware command
    t_start_total = time.time() 
    print(f"Starting firmware command {cur_task_id}_{cur_task_id_inst_index}")
    process_firm_stdout = ""
    # Open a file for writing the output
    # output_file = open(f"output_{i + 1}.txt", "w")

    # Run the make command and capture its output
    t_start = time.time() 
    make_process = os.popen(make_command)
    _ = make_process.read()
    t_end = time.time()
    print(f"make took {abs(t_start - t_end)} sec")

    try:
        # Run the command and capture its output
        signal.alarm(1000)
        t_start = time.time() 
        process_firm = os.popen(f"./firmwire_comm.sh output_{cur_task_id}_{cur_task_id_inst_index}.txt")
        t_end = time.time()
        print(f"popin command took {abs(t_start - t_end)} sec")
        t_start = time.time() 
        process_firm_stdout = process_firm.read()
        t_end = time.time()
        print(f"stdout read took {abs(t_start - t_end)} sec")
        print("Read finished...")
        # print(process_firm_stdout)
        signal.alarm(0)

    except Exception as ex:
        sys.stdout.flush()
        print("Inside catch:", ex)
        signal.alarm(0)
        pobj = psutil.Process(os.getpid())
        for c in pobj.children(recursive=True):
            c.kill()
        
    finally:
        sys.stdout.flush()
        signal.alarm(0)
        pobj = psutil.Process(os.getpid())
        for c in pobj.children(recursive=True):
            c.kill()
        t_start = time.time()
    
    latesti = 0
    if process_firm_stdout == "":
        with open(f"output_{cur_task_id}_{cur_task_id_inst_index}.txt", "r") as fl:
            process_firm_stdout = fl.read()

    if "**TEST_TASK_ID:" in process_firm_stdout:
        task_id_content = process_firm_stdout.split("**TEST_TASK_ID:")[-1]
        try:
            if "**TEST_MSG_ID:" in process_firm_stdout.split("**TEST_TASK_ID:")[-1]:
                number = int(task_id_content.split("**TEST_MSG_ID:")[1].split("\n")[0])
            else:
                task_id_content = process_firm_stdout.split("**TEST_TASK_ID:")[-2]
                number = int(task_id_content.split("**TEST_MSG_ID:")[1].split("\n")[0])
            latesti = int(task_id_content.split("\n")[0])

        except ValueError:
            pass
    else:
        number = -1
    t_end = time.time()
    print(f"task_id and msg_id find took {abs(t_start - t_end)} sec")

    # Write the latest number to the file
    t_start = time.time() 
    with open("number.txt", "w") as f:
        f.write("Latest i : ")
        f.write(str(latesti))
        f.write("Latest j : ")
        f.write(str(number))
    t_end = time.time()
    print(f"writing to number.txt took {abs(t_start - t_end)} sec")
        
    t_start = time.time()
    # Read the start value for j from the msg_inject_test.c file
    with open("modkit/mtk/msg_inject_test.c", "r+") as fl:
        fl_content = fl.read()
        start_value = None 
        start_value = fl_content.split("int startj =")[1].split("\n")[0].strip()
        start_value = ''.join(filter(str.isdigit, start_value))  # remove any non-numeric characters
        start_value = int(start_value) if start_value else 0  # handle case where string is empty or non-numeric
        start_value = 0 if start_value == None else start_value
        start_valuei = fl_content.split("int starti =")[1].split("\n")[0].strip()
        start_valuei = ''.join(filter(str.isdigit, start_valuei))  # remove any non-numeric characters
        start_valuei = int(start_valuei) if start_valuei else 0  # handle case where string is empty or non-numeric
        start_valuei = 0 if start_valuei == None else start_valuei
        # # Update the start value for j if it is less than the latest number + 1
        # start_value = max(start_value, number + 1)
        # # Update the start value for i
        # if cur_task_id == -1:
        #     start_valuei = max(start_valuei, latesti)
        if cur_task_id_inst_index == 0:
            start_valuei = max(start_valuei, latesti)
            cur_task_id_inst_index += 1
            cur_task_id = start_valuei
        elif cur_task_id_inst_index == 103:
            start_valuei += 100
            cur_task_id_inst_index = 0
            start_value = 10
            cur_task_id = start_valuei
            if start_valuei > 1000:
                end_condition = True
        elif cur_task_id == start_valuei:
            cur_task_id_inst_index += 1
        else:
            start_valuei = cur_task_id
        
        if cur_task_id_inst_index == 0:
            start_value = 10
        elif cur_task_id_inst_index == 1:
            start_value = 32768
        elif cur_task_id_inst_index == 2:
            start_value = 65526
        else:
            start_value = random.randint(0, 65526)

            
        print(f"current instant index of the task_id is: {cur_task_id_inst_index}")
        print(f"current task_id is: {cur_task_id}")
        fl.seek(0)
        fl.truncate(0)
        fl_lines = fl_content.split("\n")
        for index, line in enumerate(fl_lines):
            if "int startj =" in line:
                print(f"**TEST_MSG_ID: {start_value}")
                fl.write(f"\tint startj = {start_value};\n")
            elif "int starti =" in line:
                print(f"**TEST_TASK_ID: {start_valuei}")
                fl.write(f"\tint starti = {start_valuei};\n")
            else:
                if index != len(fl_lines) - 1:
                    fl.write(line + "\n")
                else:
                    fl.write(line)

    t_end = time.time()
    print(f"updating msg_inject_test.c took {abs(t_start - t_end)} sec")
    
    # Close the socket used by the process
    pobj = psutil.Process(os.getpid())
    for c in pobj.children(recursive=True):
        c.kill()

    t_end_total = time.time() 
    print(f"this iteration took {abs(t_start_total - t_end_total)} sec in total")
