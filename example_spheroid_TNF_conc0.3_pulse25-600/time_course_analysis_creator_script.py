#!/usr/bin/env python
# coding: utf-8

import os
import glob
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import statistics as sts

sns.set(style="darkgrid")

#i = 0

for run in range(0, 24, 1):
    # Reading a json file which includes a dictionary with the mapping between 
    # PhysiCell/Boss integer codes and the corresponding string the description
    with open('cell_phases_dict.json') as fh:
        # phases_dict = {0: 'Ki67_positive_premitotic', 1: 'Ki67_positive_postmitotic', 2: 'Ki67_positive', 3: 'Ki67_negative', 4: 'G0G1_phase', 101: 'necrotic_swelling', 102: 'necrotic_lysed', 7: 'G1a_phase', 104: 'debris', 9: 'G1c_phase', 10: 'S_phase', 11: 'G2M_phase', 12: 'G2_phase', 13: 'M_phase', 14: 'live', 8: 'G1b_phase', 100: 'apoptotic', 6: 'G1_phase', 103: 'necrotic', 5: 'G0_phase'}
        phases_dict = json.load(fh)
        #print(phases_dict)
        phases_dict = {int(k):v for k,v in phases_dict.items()}
        #print(phases_dict)
        #for k,v in phases_dict.items():
        #    print(k,v)
        
    # The following dict is used to group cell phases into three general classes:
    # Alive, Apoptotic (programmed cell death), Necrotic (Non-programed cell death)
    column_mapping = { 'Ki67_positive_premitotic':'Alive', 
                       'Ki67_positive_postmitotic':'Alive',
                       'apoptotic': 'Apoptotic', 
                       'necrotic_lysed': 'Necrotic',
                       'necrotic_swelling': 'Necrotic' 
                     }

    # folder where the outputfiles are stored
    cell_output_dir = ("./run%s/output/" %run)
    #df_time_course = ("df" %run)

    # Just counting the number of files (each one corresponding to a time snapshots)
    num_of_files = len(glob.glob(cell_output_dir +  "*.txt"))
    #print(num_of_files) # = 49

    # Initializing a Pandas Dataframe to store the data
    columns = ['Time', 'Alive', 'Apoptotic', 'Necrotic']
    #print(columns)
    # Zero paddind the array: number_of_(cells_txt_)files x 4(=[time, alive, apoptotic, necrotic])
    # Return a new array of given shape and type, filled with zeros.
    data = np.zeros((num_of_files, 4), dtype=int)
    #print(data)
    df_time_course = pd.DataFrame(columns=columns, data=data)
    #print(df_time_course)

    #print("Reading cell_output files:")
    # Iterating over all cell_output files
    # sorted = taksinomhsh twn arxeiwn se seira 
    for i,f in enumerate(sorted(glob.glob(cell_output_dir +  "*.txt"))):
        #print (i,f) => e.g. 0 ../run30/output/cells_00000.txt
        # i = 0, 1, ..., 48 & f = ../run30/output/cells_00000.txt etc
        #print("\tProcessing file: %s" %f)
        # The filename includes the simulation time. So, we extract the current time
        # from the files' name and store it in the created dataframe.
        # f : filename stored
        time = int(os.path.basename(f)[6:-4])
        #print(time)
        # Access a single value for a row/column pair by integer position.
        # Give value to "Time" column
        df_time_course.iat[i, 0] = time
        #print (df_time_course)
        # reading a cell_output file (plain text ; separated columns)
        # any function can be used here, using pandas is just a shortcut
        # Read a comma-separated values (csv) file
        df = pd.read_csv(f, sep=";")
        # Rename the phases integer codes using the phases_dict as the mapping
        df.replace(to_replace={'phase': phases_dict}, value=None, inplace=True)
        #print (df) #=> opou kwdikos mpainei necrotic_swelling kok
        # Count the number of cells in each phase
        counts = df.groupby('phase').ID.count()
        #print(counts)

        # group the previous phases count into the three general classes:
        # Alive, Apoptotic, Necrotic
        # to_dict: Convert the DataFrame to a dictionary.
        for k, v in counts.to_dict().items():
            #print("\n\ti = %s, || k = %s , v = %s " %(i,k,v))
            #print("\n\tk = %s , v = %s " %(k,v))
            # mapping
            # .at: Access a single value using a label.
            df_time_course.at[i, column_mapping[k]] += v
            # print(df_time_course)

    # ------------------------------ Figure Design -------------------------------------------#
            
    # Set time column as the dataframe index
    # Set the index to become the ‘Time’ column
    df_time_course.set_index('Time', inplace=True)
    print (df_time_course)

    # ----- Division with starting cells number normalization Decision ----- #
    # Use as normalization value the number of starting agents
    #normalization_value = df_time_course.loc[0,'Alive'];
    #print('\nNormalization Value: %d\n' %normalization_value)

    # Create the normalized pandas dataframe
    #normalized = df_time_course/normalization_value;
    #print(normalized)


    #print("Creating figure")
    # Create a figure
    # dpi: dots per inches
    fig, ax = plt.subplots(1, 1, figsize=(6,4), dpi=150)
    # plot Alive vs Time
    ax.plot(df_time_course.index, df_time_course.Alive, 'g', label='alive')
    # plot Necrotic vs Time
    ax.plot(df_time_course.index, df_time_course.Necrotic, 'k', label='necrotic')
    # plot Apoptotic vs Time
    ax.plot(df_time_course.index, df_time_course.Apoptotic, 'r', label='apoptotic')
    # setting axes labels
    ax.set_xlabel('time (min)')
    ax.set_ylabel('N of cells')
    # Showing legend
    ax.legend()

    # Saving fig
    fig_fname =("./figures/example_spheroid_TNF_conc0.3_pulse25-600_run%s.png" %run)
    fig.tight_layout()
    fig.savefig(fig_fname)
    print("Saving fig as %s" % fig_fname)


# #print("Creating normalized scattered figure - Alive only")
# # Create a figure
# fig, ax = plt.subplots(1, 1, figsize=(6,4), dpi=150)
# # plot Alive vs Time
# #ax.scatter(normalized.index, normalized.Alive)
# # plot Necrotic vs Time
# ax.plot(normalized.index, normalized.Necrotic, 'k', label='necrotic')
# # plot Apoptotic vs Time
# #ax.plot(normalized.index, normalized.Apoptotic, 'r', label='apoptotic')
# # setting axes labels
# ax.set_xlabel('time (min)')
# ax.set_ylabel('N of cells')
# # Showing legend
# ax.legend()
# # axes bounds
# plt.axis([-200, 1600, -0.2, 1.2])
# plt.grid(True, axis='y', color='k', linestyle='-', linewidth=1)
# #plt.xlim([-200,1600])
# #plt.ylim([-0.2, 1.2])
# # Saving fig
# fig_fname =("./normalized_figures cell_vs_time2/normalized_pulse150_oxy_run%s.png" %run)
# #fig_fname =("./normalized_figures cell_vs_time/normalized_pulse150_oxy_runALL.png")    
# fig.tight_layout()
# fig.savefig(fig_fname)
# print("Saving normalized fig as %s" % fig_fname)

