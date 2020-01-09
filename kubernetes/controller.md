# 控制器管理器及控制器

## 控制循环

控制器通过控制循环, 使对象的 status 不断向 spec 变化, 从而使对象达到用户期望的状态.
控制循环由以下三个逻辑组件组成:

1. 控制器(Controller)
   > 控制器通过给对象的 status 和 spec 做 diff, 并决定对对象的操作.
   > 相应的控制操作执行完成后会产生对应的输出.

2. 被控制的对象

3. 传感器(Sensor)
   > 传感器通过调用系统接口, 获取资源的数据.
   > 并将资源信息与资源事件存入队列中.

![控制循环](./images/control_loop.png)

### Sensor

传感器主要由 Reflector(反射器), Informer(通知器), Indexer(指示器) 组成.

1. 获取资源(对象)状态
   > Reflector 通过 list 和 watch api-server 来获取资源的数据.
   > list: Controller 重启和 watch 中断时实现对资源的全量更新.
   > watch: 在多次 list 之间进行资源的增量更新.

2. Add Delta
   > Reflector 获取资源数据后, **将资源对象信息本身以及资源对象事件类型**.
   > 存入 Delta 队列(可以保证队列中同一个对象只有一条记录).

3. Pop delta and Store object
   > Informer 不断从 Delta Queue 弹出对象记录
   > 一方面将事件交给事件处理的回调函数.
   > 另一方面将资源对象交给 Indexer
   > Indexer 将资源对象(对象的最新状态)记录在缓存中.
   > 缓存默认以资源对象的命名空间作为 key, 并且可以被多个 Controller 共享.

![sensor](./images/sensor.png)

### Controller

- 事件处理函数
   > 监听 Informer 中资源的新增, 更新, 删除等事件,
   > 并根据控制器的逻辑决定是否要处理该事件.
   > 对于需要处理的事件, 会把事件关联资源的命名空间和名字存入工作队列中.
- worker
   > 由 worker 池中的一个 worker 进行处理.
   > 从缓存中获取最新的资源状态, 并通过对比 spec 和 status 确定相应的操作.
   > 并由 worker 执行相应操作.

### 控制循环举例 -- 扩容

![扩容 yaml](./images/rs_scale.png)

![阶段1](./images/scale_step1.png)

![阶段2](./images/scale_step2.png)
