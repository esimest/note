from random import randint

# 随机生成指定长度的数组，默认长度为 10
def rand_li(length=10):
    return [randint(1, 998) for _ in range(length)]


# 交换数组 li 中 i 和 j 两个位置对应的值
def swap(li, i, j):
    li[i], li[j] = li[j], li[i]