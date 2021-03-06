# Mysql 客户端使用

> mysql 命令中的选项都可以直接指定在配置文件(默认：/etc/my.cnf) 中的 [client] 域中。将常用命令写入配置，可以提高使用效率。 mysqldump mysqladmin 等共享

## command

```shell
# 创建用户并设置密码
CREATE USER 'cbuser'@'localhost' IDENTIFIED BY 'cbpass';

# 授予权限
GRANT ALL ON cookbook.* TO 'cbuser'@'localhost';

# 退出 mysql 客户端
exit;quit;bye; # Ctrl + D

# my.cnf 格式
[client] # 该域中的配置对 mysql 命令生效
name=value  # name 为 mysql 使用的选项，value 为选项的值
## name 和 value 可以和 '=' 以多个空格分开，多个 name 指定时只有最后一个生效
## 当 value 需要包含空格时，可以使用单引号或双引号括起来
; mysql 配置文件中';' 在行首可以起到注释作用。# 在任何位置都起注释作用
name = value

# 输出默认使用的选项，以及对应的值
mysql --print-defaults

# 打印配置文件中指定域中的内容
my_print_defaults client

# 显式指定不输入密码
mysql --skip-password

# 显示表结构
show FULL COLUMNS from ${table_name};
DESC ${table_name};
DESCRIBE ${table_name};

# linux 命令行直接执行 SQL 语句
mysql -e "${statement1};${statement2}"

# linux 命令行执行 SQL 文件
mysql < ${file}
cat ${file} | mysql

# mysql 命令行执行 SQL 文件
mysql> source ${file}; #或
mysql> \. ${file};

# 输出结果不包含字段名
mysql --skip-column-names
mysql -ss

# 使用用户变量保存 SQL 执行的结果
mysql> SELECT @var := ${column} FROM ${table}

# 直接设置变量
mysql> SET @var = ${value}
mysql> SET @var = ${SQL}
!! 变量只能出现在允许表达式的语句中。需要常量和文本标识符的场景使用变量无法起作用。如建表语句中使用变量来代替表名就会报错。
```
