import logging

def init():
    print("Control module initialized")
    logging.info("Control module initialized")
    start()

def start():
    print("Control module started")
    logging.info("Control module started")

def stop():
    print("Control module stopped")
    logging.info("Control module stopped")
