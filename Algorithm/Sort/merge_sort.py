"""
归并归并：先归再并

"""

from utils import swap, rand_li


def merge(li, p, q, r):
    """
    并：将一个由两个有序数组拼接成的数组经行排序
    li: 待排序数组
    p: 第一个有序子数组的下标
    q: 第二个有序子数组的下标
    r: 第二个有序子数组的结尾下标
    """
    # 先将两个子数组提取出来
    sub_l, sub_r = li[p:q+1], li[q+1:r+1]

    # 对比两个数组的最小元素，更小的元素放入原始列表的开始位置
    start, i, j = p, 0, 0
    len_l, len_r = len(sub_l), len(sub_r)

    while i < len_l and j < len_r:
        if sub_l[i] <= sub_r[j]:
            li[start] = sub_l[i]
            i += 1
        else:
            li[start] = sub_r[j]
            j += 1
        start += 1

    # 将剩余的块直接填充
    if i < len_l:
        li[start:r+1] = sub_l[i:len_l]
    if j < len_r:
        li[start:r+1] = sub_r[j:len_r]


def merge_sort(li, p, r):
    if p >= r: return
    if p < r:
        q = (p + r) // 2
        merge_sort(li, p, q)
        merge_sort(li, q+1, r)
        merge(li, p, q, r)

li = rand_li()
merge_sort(li, 0, 9)
print(li)