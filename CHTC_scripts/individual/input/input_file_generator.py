# List the tissues
import os
tissues = ["adipose", "gas", "islet", "liver", "kidney"]
run_id_base = 1
run_id_count = 0
network_structures = [[1000, 1000, 500, 100]]
momentums = [0.9]
l2_rs = [0.5]
batch_sizes = [100]
learning_rates = [0.01]
optimizers = ["adam"]
num_layers = [len(net) for net in network_structures]
patiences = [3]
dropout_rates = [[0.3,0.3,0.1,0]]
list_of_file_names = "test_1.txt" # this is the file you put into the .sub file queue statement
g = open(list_of_file_names,"w")
for tissue in tissues:
    # loop through the network structures
    for structure in network_structures:
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
                                    if tissue == "adipose":
                                        tmp = "adi"
                                    elif tissue == "kidney":
                                        tmp = "kid"
                                    else:
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
                                        f.write("," + str(structure[j]))
                                    for j in range(num_layers[i]):
                                        f.write("," + str(dropout_rates[i][j]))
                                    f.close()
                                    run_id_count +=1

                                    g.write(file_name + "," +path+","+ path + "/" + file_name + ".in,"+tissue + "\n")
g.close()
