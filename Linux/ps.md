# ps(Process Status)

## 输出

### 输出列含义

- F: Flag
- STAT: 进程状态
- UID: 程序执行者的 ID
- PID: 进程 ID
- PPID: 父进程 ID
- C/%CPU: CPU 使用率百分比
- %MEM: 内存使用率百分比
- PRI: 优先执行序
- NI: Nice 值
- VSZ: 进程可以访问的所有内存
- RSS(Resident Set Size): 常驻内存集，实际使用的物理内存
- WCHAN: 表示是否在运作(- 表示正在运作)
- TTY: 登录者的终端号
- TIME: 使用掉的 CPU 时间
- CMD: 执行的命令

### 进程状态

- D: 不可中断
- R: runnable(on run queue)
- S: Sleeping
- T: 停止
- Z: 僵死

## 使用
