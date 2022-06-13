import os
import csv

for i in range(29):
    path = "/home/hlin324/our-project-x-2021/CHTC_scripts/individual/input/islet/islet_520/islet_520_" + str(i)+ ".out" 
    f = open(path,"r")
    lines = f.readlines()
    line = lines[-5][:-1]
    output = open("./adi_modules_result.csv", "a+")
    csvwriter =csv.writer(output, delimiter=',')
    csvwriter.writerow(line.split(' '))
    f.close()
    output.close()
