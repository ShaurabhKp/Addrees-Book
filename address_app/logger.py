import logging

def log(): 

# Create and configure logger
    logging.basicConfig(filename="newfile.log",
                        format='%(asctime)s %(message)s',
                        level=logging.DEBUG,
                        filemode='w')
    
    # Creating an object
    logger = logging.getLogger()
    return logger