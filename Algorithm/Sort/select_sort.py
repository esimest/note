""""
快速选择排序是选择排序的一种
先选择一个值(一般选li[0]) 认定为最大值
然后遍历数组与最大值做比较，如果比最大值大
就将最大值下标替换，直到该次循环结束
就可以选出该次循环的最大值
"""

from utils import swap, rand_li

def select_sort(li):
    length = len(li)
    for i in range(length):
        max = 0
        for j in range(length-i-1):
            if li[j] > li[max]:
                max = j
        swap(li, max, length-1-i)

li = rand_li()

select_sort(li)

print(li)