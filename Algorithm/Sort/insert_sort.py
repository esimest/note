""""
插入排序: 将一个元素插入一个已经排好序的数组中
"""

from utils import swap, rand_li


def insert_sort(li):
    out = []
    for ele in li:
        length = len(out)
        index = 0
        while index < length and out[index] < ele:
            index += 1
        if index < length:
            out.insert(index, ele)
        else:
            out.append(ele)
    return out


# 交换实现
def insert_sort_1(li):
    length = len(li)
    for i in range(1, length):
        j = i - 1
        """
        一般形式
        while j >= 0 and li[j] > li[j+1]:
            swap(li, j, j+1)
            j -= 1
        """
        # python 风格
        while j >= 0 and li[j] > li[i]:
            j -= 1
        li.insert(j+1, li[i])
        del li[i+1]



li = rand_li()
insert_sort_1(li)
print(li)