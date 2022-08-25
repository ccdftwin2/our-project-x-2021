import os
import csv

for i in range(33):
    path = "/home/hlin324/our-project-x-2021/CHTC_scripts/individual/input/kid/kid_508/kid_508_" + str(i)+ ".out" 
    f = open(path,"r")
    lines = f.readlines()
    line = lines[-5][1:-2]
    output = open("./kid_modules_result.csv", "a+")
    csvwriter =csv.writer(output, delimiter=',')
    csvwriter.writerow(line.split(','))
    f.close()
    output.close()