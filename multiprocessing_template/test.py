from template import AsyncWorker
import time

def f_1(arg1 = "default_value"): 
    time.sleep(5)
    return arg1

def f_2(arg1 = "default_value", arg2 = "default_value"):
    time.sleep(1)
    return arg1 + arg2

def consumer(data): 
    print("consumed data : {}".format(data))

    # Example : Write to file concurrently

if __name__=="__main__":

    ''' 
    Init
    ''' 
    async_worker = AsyncWorker(2) # number of workers as param, (max = os.cpu_count())

    ''' 
    Add methods and params to worker
    ''' 
    async_worker.add(f_1, {"arg1" : "foo"})
    async_worker.add(f_2, {"arg1" : "foo", "arg2" : "bar"})

    async_worker.stream_run(consumer)

    print(async_worker.output_buffer)

