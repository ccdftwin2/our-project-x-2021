# List the tissues
mode = 1 # one for output process, 2 for input
import os
import csv
tissues = ["islet"]
run_id_base = 500
run_id_count = 0
network_structures = [[25000,  15000, 1000, 200],[25000,  15000, 1000, 200],[25000,  15000, 1000, 200],
                      [26000,  15000, 1000, 200],[26000,  15000, 1000, 200],[26000,  15000, 1000, 200],
                      [27000,  15000, 1000, 200],[27000,  15000, 1000, 200],[27000,  15000, 1000, 200],
                      [28000,  15000, 1000, 200],[28000,  15000, 1000, 200],[28000,  15000, 1000, 200],
                      [29000,  15000, 1000, 200],[29000,  15000, 1000, 200],[29000,  15000, 1000, 200],
                      [30000,  15000, 1000, 200],[30000,  15000, 1000, 200],[30000,  15000, 1000, 200]]
momentums = [0.9]
l2_rs = [0.3]
batch_sizes = [100]
learning_rates = [0.0001]
optimizers = ["adam"]
num_layers = [len(net) for net in network_structures]
patiences = [3,4]
dropout_rates = [[0.25,0.25,0.25,0.1],[0.2,0.2,0.2,0.1],[0.15,0.15,0.15,0.1],
                 [0.25,0.25,0.25,0.1],[0.2,0.2,0.2,0.1],[0.15,0.15,0.15,0.1],
                 [0.25,0.25,0.25,0.1],[0.2,0.2,0.2,0.1],[0.15,0.15,0.15,0.1],
                 [0.25,0.25,0.25,0.1],[0.2,0.2,0.2,0.1],[0.15,0.15,0.15,0.1],
                 [0.25,0.25,0.25,0.1],[0.2,0.2,0.2,0.1],[0.15,0.15,0.15,0.1],
                 [0.25,0.25,0.25,0.1],[0.2,0.2,0.2,0.1],[0.15,0.15,0.15,0.1]]

list_of_file_names = "test_lin.txt" # this is the file you put into the .sub file queue statement
g = open(list_of_file_names,"w")
for tissue in tissues:
    # loop through the network structures
    num_tis = 3
    for z in range(1):
        # momentum
        for momentum in momentums:
            # l2_rs
            for l2_r in l2_rs:
                # batch sizers
                for batch_size in batch_sizes:
                    # optimizers
                    for optimizer in optimizers:
                        # learning rate
                        for learning_rate in learning_rates:
                            # patiences
                            for patience in patiences:
                                # network structure
                                for i in range(len(network_structures)):
                                    file_name = tissue + "_" + str(run_id_base+run_id_count) # run id
                                    # create the directory for the run (will have logs and results)
                                    parent = os.getcwd() + "/" + tissue + "/" 
                                    if not os.path.exists(parent) and mode == 0:
                                        os.mkdir(parent)
                                    path = os.path.join(parent, file_name)
                                    if not os.path.exists(path) and mode == 0:
                                        os.mkdir(path)
                                    # create the input file
                                    if mode == 0:
                                        f = open(tissue + "/" + file_name + "/" + file_name + ".in", "w")
                                        f.write(tissue)
                                        f.write(",")
                                        # write the file names
                                        tmp = tissue
                                        f.write(tmp + "_filled.csv,")
                                        f.write(tmp + "_filled_glucose.csv,")
                                        f.write(tmp + "_filled_sex.csv,")
                                        f.write(str(momentum)+",")
                                        f.write(str(l2_r)+",")
                                        f.write(str(batch_size) + ",")
                                        f.write(str(learning_rate) + ",")
                                        f.write(str(optimizer) + ",")
                                        f.write(str(num_layers[i]) + ",")
                                        f.write(str(patience) + ",")
                                        f.write(file_name)
                                        for j in range(num_layers[i]):
                                            f.write("," + str(network_structures[i][j]))
                                        for j in range(num_layers[i]):
                                            f.write("," + str(dropout_rates[i][j]))
                                        f.close()
                                        run_id_count +=1

                                        g.write(file_name + "," +path+","+ path + "/" + file_name + ".in,"+tissue + "," + str(num_tis) + "\n")
                                        num_tis += 1
                                        num_tis = num_tis % 5
                                        if num_tis == 0:
                                            num_tis = 1
                                    else:
                                        if os.path.exists(tissue + "/" + file_name + "/" + file_name + ".out"):
                                            f = open(tissue + "/" + file_name + "/" + file_name + ".out", "r")
                                            #output = open("islet_mult.csv", "a+")
                                            #output.write("Runid: " + file_name +", Network Structure" + str(network_structures[i]) +  ", LR: " + str(learning_rate)+ "\n")
                                            lines = f.readlines()
                                            lastlines = lines[-10:] # for a 9-way-CV sets
                                            #output.write(lastlines[0])
                                            #output.write("\n")
                                            output = open("islet_mult.csv", "a+")
                                            csvwriter =csv.writer(output, delimiter=',')
                                            csvwriter.writerow(lastlines[0][:-1].split(',')+[file_name])
                                            f.close()
                                            output.close()

                                        num_tis += 1
                                        num_tis = num_tis % 5
                                        if num_tis == 0:
                                            num_tis = 1
                                        run_id_count +=1
g.close()
