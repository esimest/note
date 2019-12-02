"""
快排是交换排序的一种
"""

from utils import swap, rand_li

def quick_sort(li):
    if len(li) <= 1:
        return li
    else:
        ele, equal, smaller, bigger = li[0], [], [], []
        for i in li:
            if ele == i: equal += [ele]
            elif ele > i: smaller += [i]
            else: bigger += [i]
        return quick_sort(smaller) + equal + quick_sort(bigger)

# 交换实现
def quick_sort_1(li, start=0, end=None):
    end = end or len(li) - 1
    if start >= end: return

    lower, upper = start, end
    while lower < upper:
        if li[lower] >= li[lower+1]:
            swap(li, lower, lower+1)
            lower += 1
        else:
            swap(li, lower+1, upper)
            upper -= 1
    quick_sort_1(li, start=start, end=lower-1)
    quick_sort_1(li, start=lower+1, end=end)


li = rand_li()
quick_sort_1(li)
print(li)
# result = quick_sort(li)
# print(result)