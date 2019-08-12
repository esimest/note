from random import randint


def make_list(length=10):
    li = []
    for i in range(length):
        li += [randint(1, 11011)]
    return li


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


if __name__ == '__main__':
    result = quick_sort(li=make_list())
    breakpoint()
    print(result)
