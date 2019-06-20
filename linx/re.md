# Linux 正则

- posix charactes(只能出现在[]中)
  - [:alnum:] == [a-zA-Z0-9] :alphabet or num
  - [:alpha:] == [a-zA-Z] :alphabet
  - [:blank:] == [ \t] :space or tab
  - [:cntrl:] == [\x00-\x1F\x7F] :control character
  - [:digit:] == [0-9] :num
  - [:graph:]  : 可视字符
  - [:print:] : 可视字符或space
  - [:lower:] == [a-z]
  - [:upper:] == [A-Z]
  - [:punct:] == [][!"#$%&'()*+,./:;<=>?@\^_`{|}~-] : 标点符号
  - [:space:] : 空白字符
  - [:xdigit:] : 十六进制数
  - [:word:] == [[:alnum:][:]]
