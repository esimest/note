# Linux用户与用户组管理

## 用户

### /etc/passwd(用户信息文件)，普通用户可以查阅
```
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
mysql:x:27:27:MySQL Server:/var/lib/mysql:/bin/false
redis:x:996:994:Redis Database Server:/var/lib/redis:/sbin/nologin
```
>/etc/passwd 每行代表一个用户的信息，由7部分组成，:为分隔符，含义分别为：

- &nbsp;用户名(必须唯一)
- &nbsp;用户密码替换符(用户密码加密后的值保存在/etc/shadow)
- &nbsp;uid(标识用户权限，0为超管，伪用户建议1~499,普通用户建议499+)
- &nbsp;gid(超级管理员组gid为0)
- &nbsp;root(用户描述信息)
- &nbsp;/root(用户宿主目录/家目录)
- &nbsp;/bin/bash(登录之后的shell,/sbin/nologin;/sbin/false无法登录)

### /etc/shadow(用户密码文件)，只有root对其有权限
```
root:$6$cVJpyLuL$oxxL4C.HO4uCPMlML/0uY3b0wf5s88wEUZjoy2Ghqe758zRQTDZzMYxB6x4rFte/iOvi9oHmUrC5qPfUeXkz01:17954:0:99999:7:::
bin:*:16659:0:99999:7:::
cheng:$6$F/E6pXDj$fpd9rrXhoJSpBQUtAmQ4NxH0ETRYds9Kr2W3i2eERC/RzmWJpK.MzcDeTTKggDT3YcP5XzOB2MMTkpiRm8Ote.:17965:0:99999:7:::
mysql:!!:17955::::::
```
>/etc/shadow 每行代表一个用户的信息，由9部分组成，含义分别为：
1. 用户名 
2. sha521加密后的密码(*/!!表示没有密码)
3. 两次修改密码间隔的最小天数(防止改完之后马上又改回来)
4. 两次修改密码间隔的最大天数(保证密码的时效性)
5. 密码的有效期
6. 密码到期之前提醒的天数
7. 密码到期后的宽限时间
8. 账号失效时间(忽略密码有效期)
9. 保留字段(暂时没有指定值)    
***<font color=red>注意：/etc/shadow中指定的绝对日期是从1970.1.1开始的天数</font>***
---
---
## setuid() setgid()和sticky bit

###### setuid (用法: chmod u+s/g+s file_name)
```
ll /etc/passwd   
-rw-r--r-- 1 root root 1418 Mar 12 14:23 /etc/passwd
```
> 除了root之外其他人不能修改该文件的内容
> 但是用户可以通过/bin/passwd来修改自己的用户密码
```
ll /bin/passwd  
-rwsr-xr-x. 1 root root 27832 Jun 10  2014 /bin/passwd
```
>设置setuid后，当普通用户执行passwd命令时，可以获取该命令的owner的权限   
***<font color=red>注意： 当文件属主不具备x权限时使用chmodu+s file_name或产生一个S权限，表示具备了setuid但是不具备x</font>***
---

###### sticky bit(用法: chmod +t dir_name)
``` 
ll -d /tmp
drwxrwxrwt. 22 root root  4096 Mar 12 09:05 tmp
```   
> 任意用户都可以对/tmp下的内容进行任意操作，会导致出现 a用户新建的目录悄悄被b删除    
> sticky bit 解决了这种现象。如果目录设置了 sticky bit则该目录下的文件或目录只有owner或root可以改动
---
---
## 虚拟用户 系统用户 伪用户
**/sbin/nologin 或 /sbin/false表示不能登录shell**
**不能登录就无法通过shell和内核沟通**
