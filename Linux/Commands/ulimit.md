# ulimit(User Limit)

ulimit 查看设置用户资源使用限制.

配置文件: /etc/security/limits.conf, /etc/security/limits.d/*.


limits.d 目录下文件按字母顺序加载. 后加载的文件配置可以覆盖先加载的
文件中相同的配置. 范围不等时, 范围越小优先级越高.

每行的结构为: `<domain> <type>  <item>  <value>`

domain 的可选值为:

- 用户名
- 组名, 使用 @group 语法标识为组
- 通配符 `*`, 默认值
- 通配符 `%`, can be also used with %group syntax,
         for maxlogin limit

type 的可选值为:

- `soft`: 执行软限制
- `hard`: 执行硬限制

item 的可选值为:

- `core` - limits the core file size (KB)
- `data` - max data size (KB)
- `fsize` - maximum filesize (KB)
- `memlock` - max locked-in-memory address space (KB)
- `nofile` - max number of open file descriptors
- `rss` - max resident set size (KB)
- `stack` - max stack size (KB)
- `cpu` - max CPU time (MIN)
- `nproc` - max number of processes
- `as` - address space limit (KB)
- `maxlogins` - max number of logins for this user
- `maxsyslogins` - max number of logins on the system
- `priority` - the priority to run user process with
- `locks` - max number of file locks the user can hold
- `sigpending` - max number of pending signals
- `msgqueue` - max memory used by POSIX message queues (bytes)
- `nice` - max nice priority allowed to raise to values: [-20, 19]
- `rtprio` - max realtime priority

## Command

命令结构: `ulimit [-HSTabcdefilmnpqrstuvx [limit]]`

命令参数:

- H: 硬限制(严格的设定, 不能/无法超过这个值)
- S: 软限制(警告的设定, 超过这个值会发出警告)
- a: All current limits are reported(打印所有资源使用情况)
- b: The maximum socket buffer size
- c: The maximum size of core files created(核心文件的最大占用空间)
- d: The maximum size of a process's data segment(进程段最大占用空间)
- e: The maximum scheduling priority ("nice")(最大 `nice` 值)
- f: The maximum size of files written by the shell and its children
- i: The maximum number of pending signals
- l: The maximum size that may be locked into memory
- m: The maximum resident set size (many systems do not honor this limit)
- n: The maximum number of open file descriptors (most systems do not allow this value to be set)
- p: The pipe size in 512-byte blocks (this may not be set)
- q: The maximum number of bytes in POSIX message queues
- r: The maximum real-time scheduling priority
- s: The maximum stack size
- t: The maximum amount of cpu time in seconds
- u: The maximum number of processes available to a single user
- v: The maximum amount of virtual memory available to the shell and, on some systems, to its children
- x: The maximum number of file locks
- T: The maximum number of threads
