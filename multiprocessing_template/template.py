from multiprocessing import Pool 
import multiprocessing as mp 
import functools
import time
import os
import threading


class Method : 
    '''
    Method init 
    '''
    def __init__(self, method, input_params): 
        self.partial_method = functools.partial(method, **input_params)

        self.method = method
        self.input_params = input_params

class AsyncWorker: 
    '''
    AsyncWorker init a pool of pool_size processes for multiple input method, and run in parallel each method, asynchronously
    '''

    def __init__(self, pool_size):

        if (pool_size > os.cpu_count()) :
            self.pool_size = os.cpu_count() 
        else : 
            self.pool_size = pool_size 

        self.methods = []
        self.partial_methods = []
        self.output_buffer = []

    def add(self, method, input_params): 
        '''
        add a method and a set of params to the worker
        '''
        new_method = Method(method, input_params)
        self.methods.append(new_method)
        self.partial_methods.append(new_method.partial_method)

    def smap(self, f):
        return f()

    def run(self):
        '''
        Init and run a pool of async tasks in parallel
        return the result when all task are finished
        '''
        p = Pool(self.pool_size)
        output = p.map_async(self.smap, self.partial_methods)

        p.close()
        p.join()
        return output.get()

    def stream_run(self, consumer): 
        '''
        Init and run a pool of async tasks in parallel 
        As soon as the result of a task is available, 
        consumer is executed on it and it is also sent to the output_buffer
        '''
        p = Pool(self.pool_size)

        pool_output_buffer = []

        for method in self.methods : 
            pool_output_buffer.append(p.apply_async(method.method, kwds=method.input_params))
        
        while(len(pool_output_buffer) > 0 ): 
            for pool_task_output in pool_output_buffer : 
                if (pool_task_output.ready()): 
                    consumer(pool_task_output.get())
                    self.output_buffer.append(pool_task_output.get())
                    pool_output_buffer.remove(pool_task_output)
        p.close()
        p.join()


'''
DEPRECATED
'''
class Worker:
    '''
    Worker init a pool of pool_size processes for input method, and run in parallel each input configuration for input method
    '''

    def __init__(self, pool_size, method, input_params):
        self.pool_size = pool_size 
        self.method = method
        self.input_params = input_params

    def task(self, input_config):
        '''
        task called in each process
        '''
        self.method(**input_config)


    def run(self): 
        '''
        Init and run the pool of tasks in parallel for each configuration of input_params 
        '''
        p = Pool(self.pool_size)
        p.map(self.task, self.input_params)

