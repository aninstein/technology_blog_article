# 堆排序
---

* [堆排序](#堆排序)
	* [1. 什么是堆？](#1-什么是堆)
	* [2. 堆的存储](#2-堆的存储)
		* [2.1 根节点存储堆](#21-根节点存储堆)
		* [2.2 使用数组法存储堆](#22-使用数组法存储堆)
	* [3. 堆的调整](#3-堆的调整)
		* [3.1 堆的调整方法（以小顶堆为例）](#31-堆的调整方法以小顶堆为例)
			* [（1）自顶向下](#1自顶向下)
			* [（2）自底向上](#2自底向上)
	* [4. 堆的构建和删除节点](#4-堆的构建和删除节点)
		* [4.1 插入节点进堆](#41-插入节点进堆)
		* [4.2 构建堆](#42-构建堆)
		* [4.3 删除堆的节点](#43-删除堆的节点)
	* [5. 堆排序](#5-堆排序)
	* [6. 前k个问题](#6-前k个问题)
	* [本文的代码链接](#本文的代码链接)

---
## 1. 什么是堆？
堆就是一棵完全二叉树，分为**大顶堆**和**小顶堆**
- 大顶堆：每一个父节点都比其子节点大，故根节点为最大
```
           7
         /   \
        6     5
      /  \   /  \
     4    3 2    1     
```

- 小顶堆：每一个父节点都比其子节点小，故根节点为最小
```
           1
         /   \
        2     3
      /  \   /  \
     4    5 6    7     
```
注意，这里说的是只是与当前节点得父节点比较，因此比如以下这个，也是小顶堆
```
            1
         /     \
      100       3
      /  \     /  \
    101  1005 6    700     
```
## 2. 堆的存储
### 2.1 根节点存储堆
由于堆其实就是一棵完全二叉树，因此我们可以用树的存储的方式，节点类：
```python
class HeapNode(object):
    def __init__(self):
        self.val = 0
        self.left_child = None
        self.right_child = None
```
使用根节点存储堆，需要记录最后一个节点，合适进行不断拓展和不断调整的堆
### 2.2 使用数组法存储堆
使用数组存储堆，这是我们一般使用的方法，这种方法一般是在堆排序中进行使用，其好处是方便定位到相关的节点位置，对于上述小顶堆，存储格式为：
```python
min_heap = [1, 2, 3, 4, 5, 6, 7]
```
其中：
- 第0个结点左右子结点下标分别为1和2
- 第i节点父结点下标：(i–1)/2
- 第i节点左孩子下标：2∗i+1
- 第i节点右孩子下标：2∗i+2

本文主要是使用数组存储堆的方式

## 3. 堆的调整
对于堆的调整，涉及到三个问题：
1. **调整堆**，插入堆之后，对插入的节点使用调整算法进行调整。堆的调整算法，分为两个：
- **自顶向下**：主要用于堆删除节点，删除结点之后把最后一个节点替换到，当前根节点位置，对此节点进行自顶向下操作
- **自底向上**：主要用于节点的插入，当一个节点插入到这个堆之后，向上调整堆，堆还能符合大顶堆或者小顶堆的定义。
2. **插入堆**，把需要插入的节点放在堆的最后一个节点之后的位置，对当前插入的这个节点进行**自底向上**的调整
3. **删除堆的节点**，删除堆节点的操作，**只能够删除根节点**，把根节点和最后一个节点交换位置之后，然后弹出最后一个节点，并且对当前堆进行**自顶向下**的操作


### 3.1 堆的调整方法（以小顶堆为例）

#### （1）自顶向下
自顶向下调整堆流程：
1. 从第一个节点，即i=0节点开始，记节点为==parent==，记当前下标为==index==。
2. 找到其左右==children==中的最小值，记为==min==。
3. 比较 ==parent== 和 ==min== 的值，如果 ==min < parent== ，**则交换==min==和==data[index]==**，并且**把==index==移动到==min==的下标，继续向下比较**。

4. 当出现==data[index]== 没有比 ==parent== 小的子节点，或者没有子节点（即计算出的子节点下标比==data_len==大），此时需要交换最后一次，即**把==parent==位置的数据，与当前==index==指向的数据交换**，结束循环
5. 处理完当前节点之后，从parent的下一个节点出发，重复上述流程，一直遍历完每一个节点。
 ```python
def min_adjust_heap_top2down(data, index):
    """
    调整堆，自顶向下，用于堆化数组
    :param data: List[int]
    :param index: 调整第几个节点，一般是从第0个节点开始
    :return:
    """
    if not data:
        return
    data_len = len(data)
    node = data[index]
    left_child = 2 * index + 1
    right_child = 2 * index + 2
    while left_child < data_len:

        # 找左右节点中小的那个进行比较
        if right_child < data_len and data[left_child] > data[right_child]:
            min_child = right_child
        else:
            min_child = left_child

        # 如果没有比当前节点更小的子节点，则返回
        if data[min_child] > node:
            break

        # 交换父子节点
        data[index], data[min_child] = data[min_child], data[index]
        # index指向当前min，继续对子节点进行比较
        index = min_child
        left_child = 2 * index + 1
        right_child = 2 * index + 2

    # 与比较到最后一个节点进行交换
    data[index] = node
 ```
 
 
#### （2）自底向上
自底向上调整堆，则相对的要比较简单一些，一般用于堆的插入，只要不断的和父节点比较即可，步骤如下：
1. 从最后一个节点开始，记为==children== 
2. 计算此节点的父节点（父节点下标：(i-1)/2），下标记为 ==index==，如果 ==children < data[index]==，则**把此处的节点与==children==交换**，然后使 ==index==指向它的父节点，继续向上比较
3. 当得到 ==parent < data[index]==，或者没有父节点了（即计算出来的父节点的值<0），此时需要交换最后一次，即**把==parent==位置的数据，与当前==index==指向的数据交换**，结束循环
4. 处理完当前节点之后，从children的上一个节点继续出发，重复上述流程
5. 如果是插入节点，则完成流程
```python
def min_adjust_heap_bottom2up(data, index):
    """
    调整堆，自底向上调整，用于插入堆
    :param data: List[int]
    :param index: 调整第几个节点，一般是最后一个节点
    :return:
    """
    if not data:
        return
    node = data[index]
    parent = (index - 1) // 2
    while parent >= 0:
        # 如果父节点比当前节点小，则直接返回了
        if data[parent] < node:
            break

        # 交换父子节点
        data[index], data[parent] = data[parent], data[index]

        # 继续向上与父节点比较
        index = parent
        parent = (index - 1) // 2

    # 与比较到最后一个节点进行交换
    data[index] = node
```

## 4. 堆的构建和删除节点
以小顶堆为例，使用上述的堆的调整方法构建堆
### 4.1 插入节点进堆 
假设有如下的堆
```linux
[0, 1, 2, 7, 4, 3, 5, 8, 9, 6]
```
需要把下面三个节点插入到堆中
```python
insert_data = [8, 9, 0]
```
只要遍历这三个数，然后不断的进行**自底向上调整堆**即可，步骤如下：
 1. 先把数据插入到最后一个叶子节点上
 2. 进行自底向上的调整
 3. 调整到父节点比当前节点小，或者调到根节点，完成插入
```python
for i in (8, 9, 0):
	insert_heap(data, i)

def insert_heap(heap_data, node):
    """
    插入数据
    1. 先把数据插入到最后一个叶子节点上
    2. 进行自底向上的调整
    3. 调整到父节点比当前节点小，或者调到根节点，完成插入
    :param heap_data:
    :param node:
    :return:
    """
    if not heap_data:
        return [node, ]
    data_len = len(heap_data)
    if data_len == 1:
        return [heap_data[0], node] if heap_data[0] < node else [node, heap_data[0]]

    heap_data.append(node)
    last_index = data_len  # (data_len - 1) + 1，这个+1是因为append了node
    min_adjust_heap_bottom2up(heap_data, last_index)
    return heap_data
```
输出结果：
```linux
[0, 1, 2, 7, 4, 3, 5, 8, 9, 6]
```

### 4.2 构建堆
当我有如下数据，需要构建成为一个小顶堆
```
data = [7, 6, 5, 1, 4, 3, 2]
```
遍历每一个数据，进行对一个空堆进行插入操作，即可完成堆的构建
```python
def make_heap(data):
    """
    构建堆
    1. 一般都用数组来表示堆
    2. i结点的父结点下标就为(i–1)/2
    3. 它的左右子结点下标分别为
        （1）左孩子2∗i+1
        （2）右孩子2∗i+2
        （3）如第0个结点左右子结点下标分别为1和2。
    :param data:
    :return:
    """
    if not data:
        return []
    data_len = len(data)
    if data_len == 1:
        return data
    elif data_len == 2:
        return data if data[0] < data[1] else [data[1], data[0]]
	
	# 超过3长的数据再需要插入
    heap_data = []
    for i in range(data_len):
        heap_data = insert_heap(heap_data, data[i])
    return heap_data
```
输出结果：
```linux
[1, 4, 2, 7, 5, 6, 3]
```


### 4.3 删除堆的节点
我们继续对上面的计算结果进行操作，需要删除堆的节点，只能够删除根节点，步骤如下：
1. 删除对顶元素的时候，就会变成两个二叉树
2. 把最后一个节点last移动到root节点(一定要用最后一个元素填补root，原因是删除root之后的剩余部分还是保持的堆的特性的，用最后一个值进行调整可以只调整一次)
3. 对last节点进行自顶向下的调整，完成堆的调整
```python
def pop_heap(heap_data):
    """
    我们只能够删除堆顶部的元素，也就是根节点的元素
    1. 删除对顶元素的时候，就会变成两个二叉树
    2. 把最后一个节点last移动到root节点(一定要用最后一个元素填补root，原因是删除root之后的剩余部分还是保持的堆的特性的，用最后一个值进行调整可以只调整一次)
    3. 对last节点进行自顶向下的调整，完成堆的调整
    :param heap_data:
    :return: top, new_heap
    """
    if not heap_data:
        return None, heap_data
    data_len = len(heap_data)
    if data_len == 1:
        return heap_data[0], []
    elif data_len == 2:
        return heap_data[0], [heap_data[1]]
    elif data_len == 3:
        ret_heap = [heap_data[1], heap_data[2]] if heap_data[1] < heap_data[2] else [heap_data[2], heap_data[1]]
        return heap_data[0], ret_heap

    top = heap_data[0]
    heap_data[0] = heap_data[data_len-1]
    heap_data = heap_data[:-1]
    min_adjust_heap_top2down(heap_data, 0)
    return top, heap_data
```
进行删除节点操作：
```python
print("heap data: ", data)
ret, data = pop_heap(data)
print("pop node, top: ", ret, " heap data: ", data)
ret, data = pop_heap(data)
print("pop node, top: ", ret, " heap data: ", data)
```
输出结果：
```linux
heap data: [0, 1, 2, 7, 4, 3, 5, 8, 9, 6]
pop node, top:  0  heap data:  [1, 4, 2, 7, 6, 3, 5, 8, 9]
pop node, top:  1  heap data:  [2, 4, 3, 7, 6, 9, 5, 8]
```
## 5. 堆排序
堆排序需要分为两个步骤：
1. 用当前需要排序的数据构建一个堆
2. 就是不断的弹出当前堆的堆顶元素，因为小顶堆的堆顶一定是最小的，即可以用于排序。
堆排序的本质就是，把数据构建成堆之后，弹出堆顶元素，然后互换堆顶和最后一个数据，不断对当前堆进行**自顶向下**的堆的调整，然后继续弹出
有示例数据：
```python
def heap_sort(data):
    """
    堆排序，堆排序其实就是不断弹出堆顶元素完成的排序
    :param data: 
    :return: 
    """
    if not data:
        return []
    ret_data = []
    top, data = pop_heap(data)
    ret_data.append(top)
    while top and data:
        top, data = pop_heap(data)
        ret_data.append(top)
    return ret_data
```
输入数据：
```linux
[7, 6, 5, 1, 4, 3, 2]
```
执行结果：
```linux
[1, 2, 3, 4, 5, 6, 7]
```

## 6. 前k个问题
```linux
问题：当前有10w个数据，求出其中前100大的数据，或者求其中第100大的数据
```

这个地方因为需要求取前k个最大或者最小的值，那么按照堆的性质，如果需要求找前k个最大的数据，则我们需要构建一个小顶堆，**堆顶元素就是这第k个数的最小值**.，只要这个数据比堆顶元素大，堆顶元素就应该弹出，对当前数据进行**自顶向下**操作，得到的**新的堆顶元素就是这第k个数的新最小值**。
 
构建一个长度为k的堆，然后使用data里面的数据遍历的与这个堆的堆顶元素进行比较，如果大于堆顶元素，则弹出堆顶，当前值换到堆顶元素上，并且进行**自顶向下**的堆调整，**即进行一次堆的插入操作**

我们首先生成10w条数据：
```python
def create_test_data():
    number = 100000
    return [random.randint(1, number) for i in range(number)]
```

然后求解前k个数据的问题：
```python
def no_k_question(data, k):
    """
    前k个问题
    问题描述：当前有100000个数据，求出其中前100大的数据，或者求其中第100大的数据
    1. 如果求前k大，则构造小顶堆
    2. 如果求前k小，则构建大顶堆
    3. 比较堆顶元素，因为堆顶元素就是第k个元素

    本题求解的是第K个大的问题
    :param data: 数据集合
    :param k: k的长度
    :return:
    """
    if not data:
        data = create_test_data()

    # 构建一个长度为k的堆
    heap_data = make_heap(data[:k])

    # 对剩余数据，与堆顶元素比较
    for i in range(k, len(data)):
        num = data[i]
        if num < heap_data[0]:  # 不能等于，因为前k个可能有重复的
            continue
        heap_data[0] = num
        min_adjust_heap_top2down(heap_data, 0)
    return heap_data
```
当然，为了节省时间，这个地方就用100条数据前10个当作测试了，输出结果：
```linux
big data:  [40, 93, 57, 25, 85, 12, 95, 33, 88, 86, 75, 58, 28, 58, 20, 23, 33, 52, 87, 77, 30, 84, 18, 26, 27, 45, 39, 32, 6, 73, 28, 68, 94, 14, 48, 8, 88, 57, 88, 43, 83, 67, 26, 54, 70, 71, 46, 91, 47, 58, 90, 95, 2, 85, 65, 84, 85, 48, 34, 18, 39, 31, 77, 21, 31, 77, 45, 55, 8, 6, 77, 99, 95, 85, 31, 80, 62, 85, 96, 24, 16, 65, 35, 97, 46, 26, 52, 32, 43, 23, 96, 77, 24, 82, 72, 23, 21, 86, 4, 95]
big data sort:  [99, 97, 96, 96, 95, 95, 95, 95, 94, 93, 91, 90, 88, 88, 88, 87, 86, 86, 85, 85, 85, 85, 85, 84, 84, 83, 82, 80, 77, 77, 77, 77, 77, 75, 73, 72, 71, 70, 68, 67, 65, 65, 62, 58, 58, 58, 57, 57, 55, 54, 52, 52, 48, 48, 47, 46, 46, 45, 45, 43, 43, 40, 39, 39, 35, 34, 33, 33, 32, 32, 31, 31, 31, 30, 28, 28, 27, 26, 26, 26, 25, 24, 24, 23, 23, 23, 21, 21, 20, 18, 18, 16, 14, 12, 8, 8, 6, 6, 4, 2]
res data sort:  [99, 97, 96, 96, 95, 95, 95, 95, 94, 93]
```


## 本文的代码链接
[https://github.com/aninstein/HappyPython/blob/master/python/algorithm_tree/learn_heap_on_tree.py](https://github.com/aninstein/HappyPython/blob/master/python/algorithm_tree/learn_heap_on_tree.py)