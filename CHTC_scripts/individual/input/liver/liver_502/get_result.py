import os
import csv

for i in range(23):
    path = "/home/hlin324/our-project-x-2021/CHTC_scripts/individual/input/liver/liver_502/liver_502_" + str(i)+ ".out" 
    f = open(path,"r")
    lines = f.readlines()
    line = lines[-5][1:-2]
    output = open("./liver_modules_result.csv", "a+")
    csvwriter =csv.writer(output, delimiter=',')
    csvwriter.writerow(line.split(','))
    f.close()
    output.close()
