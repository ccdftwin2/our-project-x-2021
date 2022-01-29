# List the tissues
import os
tissues = ["adi", "gas", "islet", "liver", "kid"]
tissues = ["adi", "islet"]
run_id_base = 40
run_id_count = 0
network_structures = [[20000, 10000, 5000, 1000, 200], [20000, 20000, 10000, 5000, 1000, 200],[20000,  10000, 1000, 200]]
momentums = [0.9]
l2_rs = [0.3]
batch_sizes = [100]
learning_rates = [0.0001, 0.00001, 0.00005]
optimizers = ["adam"]
num_layers = [len(net) for net in network_structures]
patiences = [3]
dropout_rates = [[0.25,0.25,0.25,0.25,0.1],[0.25,0.25,0.25,0.25,0.25,0.1],[0.25,0.25,0.25,0.1]]
list_of_file_names = "test_net.txt" # this is the file you put into the .sub file queue statement
g = open(list_of_file_names,"w")
for tissue in tissues:
    # loop through the network structures
    num_tis = 1
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
                                    if not os.path.exists(parent):
                                        os.mkdir(parent)
                                    path = os.path.join(parent, file_name)
                                    if not os.path.exists(path):
                                        os.mkdir(path)
                                    # create the input file
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
                                    num_tis = num_tis % 6
g.close()
