#!/usr/bin/env python
#-*-coding:utf-8-*-

import threading
import Queue

class ThreadPool(object):

    def __init__(self, pool_size=10):
        self.pool_size = pool_size
        self.task_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.tasks=[]
        self.initialized()
        
    def initialized(self):
        for i in range(self.pool_size):
            single_thread=SingleThread(self.task_queue,self.result_queue,'Thread-%s'%i)
            self.tasks.append(single_thread)

    def add_task(self, callable, *args, **kwargs):
        self.task_queue.put((callable,args,kwargs))

    def get_result(self):
        return self.result_queue.get(timeout=1)

    def close(self):
        while self.tasks:
            task = self.tasks.pop()
            task.join()
            if task.isAlive() and not self.task_queue.empty():
                self.tasks.append(task)

class SingleThread(threading.Thread):

    def __init__(self, task_queue, result_queue, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.setDaemon(True)
        self.start()

    def run(self):
        while True:
            try:
                callable, args, kwargs = self.task_queue.get(timeout=1)
                res = callable(*args,**kwargs)
                print 'ThreadName is %s,function is %s,args is %s,result is %s\n'%(self.name,callable.__name__,args,None)
                self.result_queue.put(res)
            except Queue.Empty:
                break
            except Exception as e:
                #TODO log exception
                print e

def fib(x):
    if x<2:return 1
    return fib(x-2)+fib(x-1)

def main():
    import random
    thread_pool = ThreadPool()
    for i in range(10):
        num = random.randint(1,10)
        thread_pool.add_task(fib,num)
    thread_pool.close()

    print '*'*100
    print 'get res from queue as:'
    while True:
        try:
            res  = thread_pool.get_result()
            print res
        except Queue.Empty:
            break
        except Exception as e:
            print e

if __name__ == "__main__":
    main()
    
