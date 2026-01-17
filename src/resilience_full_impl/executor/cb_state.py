import time


class cb_state:
    state:str="CLOSED"
    failure_count:int=0
    last_failure_time:time.time()
