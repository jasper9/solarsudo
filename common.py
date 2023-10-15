import logging

logging.basicConfig(filename="/var/log/solarsudo.log",
                    filemode='a',
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

lines = "--------------------------------------------------------------------------------"
#logging.info(lines)


