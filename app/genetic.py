# This is main python script.
import logging
import algorithm.model as model
from logconfig.logconfig import LogConfig
from config.config import WorldConfiguration
import util.csv as csvUtil
import algorithm.function as fun
import graphics.draw as draw

logConfig = LogConfig()
log = logging.getLogger("main")
drawEpoch = draw.Draw('Epochs')

# 1. reading and vailidating configuration
log.info("Start genetic world emulation...")

log.debug("Read the configuration of world emulation:")
wc = WorldConfiguration("genetic.yml")

# 2. reading input data
log.debug("Read the input data. Data information:")
data = csvUtil.readArrayData(wc.getTestData())
print(data)

# 3. preparing world, bots, epochs etc
context = model.PopulationContext()\
    .costFunction(fun.cost)\
    .botSolveFunction(fun.polymon)\
    .botsNumberInPopulation(wc.getSize())\
    .botsChromosomeSize(8)\
    .epochsNumber(wc.getNumberOfEpochs())\
    .data(data)\
    .botsNumberToReproduce(wc.getBestAmountToReproduce())

log.info("Prepared context for population")

log.info("Start world emulation...")
bestBotEstimation = model.runPopulation(context, lambda estimation, epoch: fun.drawEstimation(drawEpoch, estimation, epoch, context))
bestBot = bestBotEstimation.getBot()

# 5. print out the best result
print(f"Best result: gens: {bestBot.getGens()}")
log.info("Emulation is finished")


drawFinal = draw.Draw('Result')
x = context.data[:,0]
y = context.data[:,1]
yH = bestBotEstimation.getValues()
drawFinal.draw('Original', x, y)
drawFinal.draw('Hypothesis', x, yH)

drawEpoch.finish()
drawFinal.finish()
