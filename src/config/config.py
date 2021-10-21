import yaml 
import os.path as path
import algorithm.function as alg

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
        if not path.isfile(self.config['configuration']['data']['test']):
            raise Exception("Test data file is not found")
        
        bestAmountToReproduce = self.getBestAmountToReproduce()
        if bestAmountToReproduce > 0.1 or bestAmountToReproduce < 0.01:
            raise Exception("Param bestAmountToReproducePercent is invalid. Expected between: 0.01 and 1")

    def getSolveFunctions(self):
        functions = []
        for fun in self.config['configuration']['population']['enabled']:
            if (fun == 'polynom'):
                functions.append(alg.polymon)
            elif (fun == 'sincos'):
                functions.append(alg.sinCos)
        return functions

    def getBestAmountToReproduce(self):
        value = self.config['configuration']['population']['bestAmountToReproducePercent']
        return float(value)
