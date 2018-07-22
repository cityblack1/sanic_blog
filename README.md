## 构建性能极高的后端代码

异步后端代码需要注意以下几点：
* 所有涉及到 IO 的操作，都用 async / await 去进行修饰
* 防止阻塞代码的使用

对于本项目：
* 使用 sanic 框架作为后端服务器，据说 sanic 的性能是可以媲美 Go 的
* 使用 aiomysql 进行 Mysql 查询，并在原有 api 上用元编程进行封装，以便于人类使用
* 使用 aioredis 进行 redis 查询
* 使用 react + restful api 的方式进行前后端分离逻辑