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
log.info("Read the input data. Data information:")
data = csvUtil.readArrayData(wc.getTestData())
log.info(data)

# 3. preparing world, bots, epochs etc
context = model.PopulationContext()\
    .costFunction(fun.cost)\
    .botSolveFunction(wc.getSolveFunction())\
    .botsNumberInPopulation(wc.getSize())\
    .botsChromosomeSize(wc.getChromosomeSize())\
    .epochsNumber(wc.getNumberOfEpochs())\
    .data(data)\
    .botsNumberToReproduce(wc.getBestAmountToReproduce())

log.info("Prepared context for population")

log.info("Start world emulation...")
bestBotEstimation = model.runPopulation(context, lambda estimation, epoch: fun.drawEstimation(drawEpoch, estimation, epoch, context))
bestBot = bestBotEstimation.getBot()

# 5. print out the best result
log.info(f"Best result: gens: {bestBot.getGens()}")
# 6. print out the hypothesis string
printFunction = wc.getPrintFunction()
log.info(f"Hypothesis: {printFunction(bestBot.getGens())}")

log.info("Emulation is finished")


drawFinal = draw.Draw('Result')
x = context.data[:,0]
y = context.data[:,1]
yH = bestBotEstimation.getValues()
drawFinal.draw('Original', x, y)
drawFinal.draw('Hypothesis', x, yH)

drawEpoch.finish()
drawFinal.finish()
