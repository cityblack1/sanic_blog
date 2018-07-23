## 什么是 Sanic？

Sanic 是新一代 Python web 框架，[项目地址](https://github.com/channelcat/sanic)。Sanic 自从 2016 年 11 月从 github 发布第一版以来，已经有了将近 10k 的 stars。

Sanic 是一个异步驱动的框架，基于 Python 3.5+ 的 async / await 语法。


## 为什么用 Sanic？

Sanic 使用 C 重写了 python 原生的 event loop，http parser，性能有了巨大的飞跃。

Sanic 是目前所有 Python 生态圈中性能最高的 web 框架。其性能甚至可以媲美 Go 语言的框架。能短时间内处理海量的并发请求。

Sanic 还是一个 flask-like 的框架，在保留了 flask 简洁特性的同时，更进一步简化了 api。使得开发代码的时候更加的人性化。


## 异步编程

异步编程是 python 未来的风向标，不管是 python 3.5 引入的 asyncio 库，还是 async / await 语法糖，甚至是一直讨论中的 ASGI，都表明了官方的态度。

Python 3.5 新引入的标准库 asyncio 大大简化了我们使用异步代码的方式。

异步 IO 的原理是利用 CPU 可以和 IO 能同时干活的特性，当触发一个函数触发 IO 的时候，CPU 把触发 IO 挂起，去执行其他可以执行的函数。

为了方便理解，我们分别用 python 3.5 之前的方式写同步代码和异步代码，来简要分析下他们的区别。
```python
# 同步代码
from somewhere import some_fds, some_callback1
     
     
for fd in some_fds:
    fd.send('some bytes', block=False)
    data = fd.resv(block=True)  # 假设这个时间是 1 s
    some_callback1(data)
```
```python
# 异步代码
from select import epoll

from somewhere import some_fds, EVENT1, EVENT2, some_callback1,\
     some_callback2, balabala


_epoll = epoll()

for fd in some_fds:
        fd.sned('some bytes', block=False)

def eventloop():
    for fd in some_fds:
        _epoll.register(fd, EVENT1)

    while True: 
        events = _epoll(timeout=2)
        for fd, event in events:   
            yield fd, event
        
event_loop = eventloop()
        
for fd, event in event_loop:
    if fd in balabala():
        data = fd.resv(block=False)
        some_callback1(data)
    if event == EVENT1:
        data = fd.resv(block=False)
        some_callback2(data)
    if event == EVENT2:
        data = fd.resv(block=False)
        balabala(data)
```

上面这段代码有几个关键概念需要理解：

* event_loop：又叫事件循环。顾名思义，就是一个不断执行的循环。
* 事件注册：将对应的文件描述符注册特定的事件，比如 准备写，准备读 等等。
* 事件监听：事件监听就是 epoll 去监听内核传递的消息，比如我们之前注册了"准备读"这个事件。当文件描述符收到数据的时候，内核就会传递一个信号，能被 epoll 监听到。
* 回调函数：当任务满足特定的条件，被 check 成功的时候执行的相应的代码块

fd.sned('some bytes') 模拟 IO 中发送消息的过程，我们假设我们收到发送的消息需要 1 秒，处理消息的事件是 0 秒（通常来说 cpu 处理的速度远快于 io）。如果是同步代码，我们发完了消息就必须阻塞，直到我们接受到消息才能处理数据并发送下一个。这样我们发送 3 个消息并处理 3 个消息需要 3 秒

可如果是异步代码，我们可以一口气把所有消息都发送出去，然后靠内核给我们发送相应的事件，来调用对应的回调函数，从而节省了同步调用中等待 io 收到消息的时间。这样无论我们同时执行多少任务都只需要 1 秒。

## sanic 和 asyncio

asyncio 其实就是对传统方式写异步代码的一种封装，让我们写异步代码的时候更加方便。当然其中的概念非常复杂，复杂到我也不想去，也感觉没必要去关心。
简要来说 asyncio 你可以理解有一个摩天轮，他会不停的转，下面有一个按钮，有个管理员会管理这个按钮。一旦有人想乘坐某一个指定的车厢，等那个车厢转到地面上，管理员就按下按钮，摩天轮停止。当人都上去以后，管理员弹起按钮，摩天轮继续转动。
所以我们 asyncio 中的一些概念就能理解了：
* io_loop 就相当于那个摩天轮，如果没有管理员的指令，他就会不停的转
* task 相当于摩天轮上挂着的车厢。空车厢代表 task 没执行。人装满了代表 task 执行完毕
* event 相当于按下按钮和弹起按钮。按下按钮表示有人，也就是 task 可以被继续执行。弹起按钮代表人没了，表示这个 task 阻塞了，应该让摩天轮继续转，直到凑够下一波人。
* 程序操控 代表了是管理员控制摩天轮的停止和开启，而不是摩天轮自己想停就停，想开就开。




