# This is main python script.
import logging
import algorithm.model as model
from logconfig.logconfig import LogConfig
from config.config import WorldConfiguration
import util.csv as csvUtil
import algorithm.function as fun

logConfig = LogConfig()
log = logging.getLogger("main")

# 1. reading and vailidating configuration
log.info("Start genetic world emulation...")

log.debug("Read the configuration of world emulation:")
wc = WorldConfiguration("genetic.yml")
print("wc=", wc)
wc1 = WorldConfiguration("genetic.yml")
print("wc1=", wc1)
print(wc.config)
print(wc.getSolveFunctions())

# 2. reading input data
log.debug("Read the input data. Data information:")
data = csvUtil.readArrayData("test.csv")
print(data)

# 3. preparing world, bots, epochs etc
context = model.PopulationContext()\
    .costFunction(fun.cost)\
    .botSolveFunction(fun.polymon)\
    .botsNumberInPopulation(wc.getSize())\
    .botsChromosomeSize(4)\
    .epochsNumber(wc.getNumberOfEpochs())\
    .data(data)\
    .botsNumberToReproduce(wc.getBestAmountToReproduce())

log.info("Prepared context for population")

log.info("Start world emulation...")
bestBotEstimation = model.runPopulation(context)
bestBot = bestBotEstimation.getBot()

# 5. print out the best result
print(f"Best result: gens: {bestBot.getGens()}")
log.info("Emulation is finished")
