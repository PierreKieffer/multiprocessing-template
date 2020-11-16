# multiprocessing-template 
Provides parallel and async execution of multiple methods, and processing of results in real time.

`AsyncWorker` provides two runners : 
Both runners init and run a pool of async tasks (same / different ones) in parallel. 

- stream runner : 
Provides a way to consume results in real time, asynchronously. 

- standard runner : 
Returns the result when all task are finished.


* [Install](#install)
* [Usage](#usage)
	* [Required](#required)
	* [AsyncWorker](#asyncworker)
		* [Stream runner](#stream-runner)
		* [Standard runner](#standard-runner)
	* [Worker (! deprecated, refer to AsyncWorker !)](#worker-deprecated-refer-to-asyncworker-)


## Install 
```bash
pip install .
```

## Usage 

### Required 
The executed methods must respect the following format:

```python
def method(**kwargs): 
	'''
	do something ... 
	'''
```
### AsyncWorker

#### Stream runner 

Inits and runs a pool of async tasks (same / different ones) in parallel. 
Provides a way to consume results in real time, asynchronously. 

`stream_run()` takes a method as param, to consume results in real time. 

As soon as the result of a task is available, the method of consumption of the result, passed in parameter of `stream_run`, is executed and the result is also sent to the `output_buffer`.

- Import 
```python
from multiprocessing_template.template import AsyncWorker
```

- Methods example 
```python 
def f_1(arg1 = "default_value"): 
    time.sleep(5)
    return arg1

def f_2(arg1 = "default_value", arg2 = "default_value"):
    time.sleep(1)
    return arg1 + arg2
```

- Custom results consumer
```python
def consumer(data): 
    print("consumed data : {}".format(data))
```

```python 
if __name__=="__main__":

    '''
    Init
    '''
    async_worker = AsyncWorker(2)

    '''
    Add methods and params to worker
    '''
    async_worker.add(f_1, {"arg1" : "foo"})
    async_worker.add(f_2, {"arg1" : "foo", "arg2" : "bar"})

    async_worker.stream_run(consumer)

    print(async_worker.output_buffer)
```

- Output 
```bash 
consumed data : foobar
consumed data : foo
['foobar', 'foo']
```

#### Standard runner
Inits and runs a pool of async tasks in parallel.
Returns the result when all task are finished.

- Import 
```python
from multiprocessing_template.template import AsyncWorker
```
- Methods example 
```python
def f_1(arg1 = "default_value"): 
    print(arg1)

def f_2(arg1 = "default_value", arg2 = "default_value"): 
    print(arg1)
    print(arg2)

def f_3(**kwargs): 
    print(kwargs.get("arg"))
```

```python
`if __name__=="__main__":

    '''
    Init worker
    '''
    async_worker = AsyncWorker(4)

    '''
    Add methods and params to worker
    '''
    async_worker.add(f_1, {"arg1" : "foo"})
    async_worker.add(f_1, {"arg1" : "bar"})
    async_worker.add(f_2, {"arg1" : "foo", "arg2" : "bar"})
    async_worker.add(f_3, {"arg" : "foobar"})

    output = async_worker.run()
```


### Worker (! deprecated, refer to AsyncWorker !)
Worker allows parallel execution of the same method for several configurations

- Import 

```python
from multiprocessing_template.template import Worker
```
- Method example 
```python
def method(**kwargs) : 
        print("arg_1 = {}".format(kwargs.get("arg_1")))
        print("arg_2 = {}".format(kwargs.get("arg_2")))
```

- Worker
```python
if __name__=="__main__": 

    '''
    Init configuration for each process and init input_configuration tuple 
    '''
    conf_1 = {"arg_1" : 10, "arg_2" : "foo"}
    conf_2 = {"arg_1" : 20, "arg_2" : "bar"}
         
    input_configuration = (conf_1, conf_2)

    '''
    Init Worker(number of processes, input_method, input_configuration)
    '''
    worker= Worker(2, method, input_configuration)
    worker.run()

```

