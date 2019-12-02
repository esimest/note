""""
堆排序(完全二叉树版本)：
  由于堆结构的第一位一定是数组中的最大/小值，
  因此可以通过递归的执行li[0] + heapify(li[1:])
  来使用对结构的特性来对数组进行排序
  heapify(构造堆): 堆的结构特性是第一个节点是数组中的最大/最小值。
  通过二叉树的实现大顶堆就是: a[i] >= a[2*i +1] and a[i] >= a[2*i +2]
  又因为二叉树可以通过递归的方式定义，因此可以使用递归的方式去定义堆
"""

from .utils import swap, rand_li

def heapify(li :list, n :int, i :int):
    """
    heapify: 在左孩子和有孩子树(若存在)是堆结构的情况下，将将父节点和左右孩子树一起构成堆结构
    li: 原始数组
    n: 要做 heapify 的长度(n >= len(li))
    i: 要构成堆的树的根节点(i <= n)
    """

    if i > n: return

    max = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and li[left] > li[max]:
        max = left
    if right < n and li[right] > li[max]:
        max = right

    if max != i:
        swap(li, i, max)
        heapify(li, n, max)

def build_heap(li, n):
    """
    build_heap: 将一个无序的数组构造成堆结构
    li: 需要构造的数组
    n: 需要构造的长度
    """
    last = n -1
    parent = (last -1) // 2

    for i in range(parent, -1, -1):
        heapify(li, n, i)

def heap_sort(li):
    """
    heap_sort: 使用 build_heap 构造堆，然后将 li[0] 和 li[-1] 调换
    可以确保li[-1] 最大，然后对 li[:-1] 进行同样的操作，由于只改变了根节点
    所以根节点的两个子树是堆结构因此只需要执行一次 heapify 就行了
    """
    length = len(li)
    build_heap(li, length)
    for i in range(length):
        heapify(li, length-i, 0)
        li[length-i-1], li[0] = li[0], li[length-i-1]



li = rand_li()

heap_sort(li)
print(li)
