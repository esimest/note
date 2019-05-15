#!/bin/bash
# validAlphaNum  --  确保输入内容仅限于字母和数字

function validAlphaNum(){
    # 返回值：如果输入内容全部都是字母和数字，那么返回0；否则，返回 1.

    # 删除所有不符合要求的字符。
    validchars="$(echo $1 | sed 's/[^[:alnum:]]//g')"

    if [ "$validchars" = "$1" ] ; then
        return 0
    else
        return 1
    fi
}

# main
/bin/echo -n "Enter input: "
read input
# 验证输入
if ! validAlphaNum "$input" ; then
    echo "Your input must consist of only letters and numbers. " >&2
    exit 1
else
    echo "Input is valid."
fi
exit 0
