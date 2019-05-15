# find
- 用法   
  >find [-H] [-L] [-P] [-D debugopts] [-Olevel] [starting-point...] [expression]    
  > starting-point 没指定时为当前目录
  > expression   
- 大写参数(<font color=red>写在要查找的路径前面</font>) 
   > man说明中的command-line 参数实指 starting-point  
   > 如果同时指定了PLH三个参数，出现在命令行最后一个的生效
   1. -P 不查找链接文件所指向的文件或目录(默认参数)
   2. -L 查找链接文件所指向的目录，并以该链接文件为base目录
   3. -H 不查找链接文件，除非后面的starting-point是链接文件
   4. -D 打印诊断信息，后接具体的诊断方式
   5. -O 选择优化级别，后接具体的级别[1~3]