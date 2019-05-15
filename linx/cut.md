### cut, 打印每行中选定的列
```
DESCRIPTION
       Print selected parts of lines from each FILE to standard output.

       Mandatory arguments to long options are mandatory for short options too.

       -b, --bytes=LIST   一个字节为一列
              select only these bytes

       -c, --characters=LIST  一个字符为一列
              select only these characters

       -d, --delimiter=DELIM 分隔符
              use DELIM instead of TAB for field delimiter

       -f, --fields=LIST  选中的范围
              select only these fields;  also print any line that contains no delimiter character, unless the -s option is specified

       -n     with -b: don't split multibyte characters 选中的范围

       --complement
              complement the set of selected bytes, characters or fields

       -s, --only-delimited 不显示没有制定分隔符的行
              do not print lines not containing delimiters

       --output-delimiter=STRING
              use STRING as the output delimiter the default is to use the input delimiter
```
- 范围的几种表示(可以混用)
  1. n 只选中第n列
  2. n,m,k,l.... 选中第n m k l...列
  3. n-m 选中第n至m列


- 示例
  1. -b 与 -c 的区别
  ```
    [root@izwz957vusqd7v0aumdakpz ~]# echo '你好，China'
    你好，China
    [root@izwz957vusqd7v0aumdakpz ~]# echo '你好，China' | cut -c1-2
    你好
    [root@izwz957vusqd7v0aumdakpz ~]# echo '你好，China' | cut -c1,2
    你好
    [root@izwz957vusqd7v0aumdakpz ~]# echo '你好，China' | cut -c1,3
    你，
    [root@izwz957vusqd7v0aumdakpz ~]# echo '你好，China' | cut -b1
    root@izwz957vusqd7v0aumdakpz ~]# echo '你好，China' | cut -b1-2
    [root@izwz957vusqd7v0aumdakpz ~]# echo '你好，China' | cut -b1-3
    你
  ```
  2. -d 与 -f 的用法
  ```
    [root@izwz957vusqd7v0aumdakpz ~]# cat /etc/passwd
    root:x:0:0:root:/root:/bin/bash
    bin:x:1:1:bin:/bin:/sbin/nologin
    daemon:x:2:2:daemon:/sbin:/sbin/nologin
    adm:x:3:4:adm:/var/adm:/sbin/nologin
    lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
    sync:x:5:0:sync:/sbin:/bin/sync
    ...
    [root@izwz957vusqd7v0aumdakpz ~]# cut -d":" -f1,7 /etc/passwd
    root:/bin/bash
    bin:/sbin/nologin
    daemon:/sbin/nologin
    adm:/sbin/nologin
    lp:/sbin/nologin
    sync:/bin/sync
    ...
  ```