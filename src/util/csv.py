import csv
from numpy import loadtxt

def readData(fileName):
    """
    Read a CSV file using csv.DictReader from the given file name
    """
    with open(fileName) as fileObj:
        _readDataFromFileObj(fileObj)

def _readDataFromFileObj(fileObj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(fileObj, delimiter=',')
    for line in reader:
        print("x=", float(line["x"]), ", y=", float(line["y"])),

def readArrayData(fileName, skipRows = 1):
    """
    Reads the given csv file with header (skipping the given rows number) and returns 
    the read data of x and y pairs as an double array
    """
    file = open(fileName, 'rb')
    return loadtxt(file, delimiter = ",", skiprows=skipRows)
