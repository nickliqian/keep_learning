import logging


logging.basicConfig(level=logging.DEBUG, filename="log.txt", format='%(asctime)s - %(name)s - %(funcName)s - %(levelno)s - %(pathname)s- %(filename)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(console)

logger.info("Start print log")
logger.debug("Do something")
logger.warning("Something maybe fail")
logger.error("Something maybe fail")
logger.critical("Something maybe fail")
logger.info("Finish")
