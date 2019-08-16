# Python 线程

## RLock

> reentrant lock(可重入锁), 一个线程可多次获取该锁，每次 count + 1, 必须每次释放已获得的锁。释放时 -1
