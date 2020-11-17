# multiprocessing-template 
<p align="center">
  <img src="logo.png">
</p>


Provides parallel and async execution of multiple methods, and processing of results in real time.

`AsyncWorker` provides two types of runners : 
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
    async_worker = AsyncWorker(2) # number of workers as param, (max = os.cpu_count())

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
    async_worker = AsyncWorker(4) # number of workers as param, (max = os.cpu_count())

    '''
    Add methods and params to worker
    '''
    async_worker.add(f_1, {"arg1" : "foo"})
    async_worker.add(f_1, {"arg1" : "bar"})
    async_worker.add(f_2, {"arg1" : "foo", "arg2" : "bar"})
    async_worker.add(f_3, {"arg" : "foobar"})

    output = async_worker.run()
```

