#!/bin/bash
# validfloat -- 测试数字是否为有效的浮点数
# 注意，该脚本不接受科学记数法（1.304e5）

# 要测试输入的数字是否为有效的浮点数，需要将值分为两部分：整数部分
# 和小数部分。先测试第一部分是否为有效整数，然后测试第二部分是否
# 为大于或等于零的有效整数。因此-1.1是有效的，-1.-1是无效的

# 使用"."记法可以将另一个脚本包含到此脚本中

. validint

function validfloat{
    fvalue="$1"

    # 检查输入的数字是否有小数点。
    if [ ! -z $(echo $fvalue | sed 's/[^.]//g') ]; then
        
        # 提取小数点之前的部分。
        decimalPart="$(echo $favalue |cut -d. -f1)"

        # 提取小数点之后的部分。
        fractionalPart="${fvalue#\.}"

        # 验证小数点左侧的整数部分。
        if [ ! -z $decimalPart ]; then
            if ! validint "$decimalPart" "" "" ; then
                return 1
            fi
        fi

        # 验证小数点右侧的部分。
        
        # 小数点之后不能有负号，因此先测试负号。
        if [ "${fractionalPart:0:1}" -eq "-" ]; then
            echo "Invalid floating-point number: '-' not allowe \
                   after decimal point." >&2
            return 1
        fi

        if [ ! -z "$fractionalPart" ]; then
            # 判断小数部分是否为有效的整数
            if ! validint "$fractionalPart" "0" "" ; then
                return 1
            fi
    else
        # 如果输入的只有一个-号没有数字也是不行的
        if [ "$fvalue" -eq "-" ]; then
            echo "Invalid floating-point format." >&2
            return 1
        fi

        # 最后判断输入的数字是否为有效整数
        if ! validint "$fvalue" "" "" ; then
            return 1
        fi
    fi
    return 0
}
