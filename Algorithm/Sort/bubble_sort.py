""""
冒泡排序是交换排序的一种
循环比较数组中相邻的两个值的大小，符合条件就直接交换
"""
from utils import swap, rand_li


def bubble_sort(li):
    length = len(li)
    for i in range(length):
        for j in range(length-i-1):
            if li[j] > li[j+1]:
                swap(li, j, j+1)

li = rand_li()
bubble_sort(li)
print(li)