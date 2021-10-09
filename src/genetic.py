# This is main python script.
import logging
from logconfig.logconfig import LogConfig
from config.config import WorldConfiguration
import util.csv as csvUtil

logConfig = LogConfig()
log = logging.getLogger("main")

# 1. reading and vailidating configuration
log.info("Start genetic world emulation...")

log.debug("Read the configuration of world emulation:")
wc = WorldConfiguration("/projects/Sascha/genetic_progect/src/genetic.yml")
print(wc.config)
print(wc.getSolveFunctions())

# 2. reading input data

log.debug("Read the input data. Data information:")
data = csvUtil.readArrayData("/projects/Sascha/genetic_progect/src/test.csv")
print(data)

# 3. preparing world, bots, epochs etc
log.debug("Prepared bots, world")

log.info("Prepared bots, world")

# 4. run the prepared world with interactive output
log.info("Start world emulation...")

# 5. print out the best result
log.info("Emulation is finished")
