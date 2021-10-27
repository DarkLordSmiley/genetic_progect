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
polynomPopulation = model.generatePopulation(fun.cost, fun.polymon, wc.getSize(), 4)
log.info("Prepared bots, population")#, polynomPopulation)

# 4. run the prepared world with interactive output
log.info("Start world emulation...")
for e in range(0, wc.getNumberOfEpochs()):
    bestBotEstimation = polynomPopulation.selectBestAndGenerate(data, wc.getBestAmountToReproduce())
    print(f"Epoch: {e}, best error: {bestBotEstimation.getErrors()[0]}")
bestBot = bestBotEstimation.getBot()
print(f"Best result: gens: {bestBot.getGens()}")

# 5. print out the best result
log.info("Emulation is finished")
