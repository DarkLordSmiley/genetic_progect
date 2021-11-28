import yaml 
import os.path as path
import algorithm.function as fun

class WorldConfiguration:
    def __new__(cls, fileName):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WorldConfiguration, cls).__new__(cls)
        return cls.instance 

    def __init__(self, fileName):
        """
        Reads the genetic configuration yaml file into internal config field.
        Also performs a validation upon the loaded configuration
        """
        print("WC INIT!!!")
        with open(fileName) as file:
            geneticConf = yaml.load(file, Loader=yaml.FullLoader)

        self.config = geneticConf
        self._validate()

    def _validate(self):
        if not path.isfile(self.config['configuration']['data']['train']):
            raise Exception("Train data file is not found")
        
        bestAmountToReproduce = self.getBestAmountToReproduce()
        size = self.getSize()
        if bestAmountToReproduce >= size:
            raise Exception(f"Param bestAmountToReproduce must be less than population size {size}")

    def getSolveFunction(self):
        functionName = self.config['configuration']['population']['solveFunction']
        return getattr(fun, functionName)

    def getBestAmountToReproduce(self):
        value = self.config['configuration']['population']['bestAmountToReproduce']
        return int(value)

    def getSize(self):
        value = self.config['configuration']['population']['size']
        return int(value)

    def getChromosomeSize(self):
        value = self.config['configuration']['population']['chromosomeSize']
        return int(value)
    
    def getNumberOfEpochs(self):
        value = self.config['configuration']['population']['numberOfEpochs']
        return int(value)

    def getTestDataAmount(self):
        value = self.config['configuration']['data']['testPercent']
        return int(value)

    def getTestData(self):
        return self.config['configuration']['data']['train']
