import numpy as np
import os
import pandas as pd
import csv

FT_TO_METER = 0.3048

def process_traj_file(data_csv_fn, start_time, duration):
    
    # Load CSV file into a pandas DataFrame
    df = pd.read_csv(data_csv_fn)
    
    # Store all column names in a list
    column_names = ['frameNum', 
                    'carId', 
                    'carCenterXft', 
                    'carCenterYft']
    
    # Create variables with the same names as columns and assign the column data to them
    for col in column_names:
        globals()[col] = np.array(df[col].tolist())
    freq = 30
    delta_t = 0.5
    frame_diff = freq * delta_t

    start_frame = start_time*freq
    end_frame = start_frame + duration*freq

    unique_frames = np.unique(frameNum)
    needed_frames = np.arange(unique_frames[0], unique_frames[-1], frame_diff)
    
    frames = []
    ids = []
    x = []
    y = []
    for i in range(len(frameNum)):
        if frameNum[i] in needed_frames and frameNum[i] >= start_frame and frameNum[i] <= end_frame:
            frames.append(frameNum[i])
            ids.append(carId[i])
            x.append(carCenterXft[i]*FT_TO_METER)
            y.append(carCenterYft[i]*FT_TO_METER)

    file = data_csv_fn[:-4]+"_gatraj.csv"
    # Open a CSV file in write mode
    with open(file, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write each list as a row in the CSV file
        writer.writerow(frames)
        writer.writerow(ids)
        writer.writerow(y)
        writer.writerow(x)




def get_subdirectories(directory):
    subdirectories = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            subdirectories.append(item_path)
    return subdirectories

def get_trajectory_files(directory):
    files_list = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and item.split('.')[-1] == 'csv' and "gatraj" not in item:
            files_list.append(item_path)
    return files_list

if __name__ == "__main__":
    directory = "data/Citysim_debug/"
    all_scenarios = get_subdirectories(directory)
    for scenario in all_scenarios:
        trajectory_path = os.path.join(scenario, 'Trajectories')
        trajectory_files = get_trajectory_files(trajectory_path)
        start_time = 0.0
        duration = 100
        for trajectory_file in trajectory_files:
            trajectory_file_name = trajectory_file.split('/')[-1]
            print("Processing trajectory file: ", trajectory_file_name)
            process_traj_file(trajectory_file, start_time, duration)
        