import os
import csv

for i in range(37):
    path = "/home/hlin324/our-project-x-2021/CHTC_scripts/individual/input/adi/adi_501/adi_501_" + str(i)+ ".out" 
    f = open(path,"r")
    lines = f.readlines()
    line = lines[-5][1:-2]

    output = open("./adi_modules_result.csv", "a+")
    csvwriter =csv.writer(output, delimiter=',')
    csvwriter.writerow(line.split(','))
    f.close()
    output.close()
