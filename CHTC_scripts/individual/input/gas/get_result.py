import os
import csv

for i in range(24):
    path = "/home/hlin324/our-project-x-2021/CHTC_scripts/individual/input/gas/gas_508/gas_508_" + str(i)+ ".out" 
    f = open(path,"r")
    lines = f.readlines()
    line = lines[-5][:-1]
    output = open("./gas_modules_result.csv", "a+")
    csvwriter =csv.writer(output, delimiter=',')
    csvwriter.writerow(line.split(' '))
    f.close()
    output.close()
