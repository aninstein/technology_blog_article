# Top k 问题
---

* [Top k 问题](#top-k-问题)
	* [1. 问题描述](#1-问题描述)
		* [数据内容](#数据内容)
	* [2. 小顶堆](#2-小顶堆)
	* [3. 优先队列（本质也是堆）](#3-优先队列本质也是堆)
	* [4. 桶排序](#4-桶排序)
	* [5. 分治法](#5-分治法)
	* [6. BigMap](#6-bigmap)
	* [7. 其他代码](#7-其他代码)
		* [7.1 公共方法](#71-公共方法)
		* [7.2 测试代码](#72-测试代码)
   * [代码链接：https://github.com/aninstein/HappyPython/](https://github.com/aninstein/HappyPython/blob/b52cab3e4453412ddba2c679dd5f01a8f413a879/python/algorithm_sort/learn_top_k.py)

---
## 1. 问题描述
对于前K个问题，描述很简单，即有一个相对较大的数据，求其中前K个大的数据，比如：
```linux
问题：当前有10w个数据，求出其中前100大的数据，或者求其中第100大的数据
```
常见解决前K个问题的主要有以下的解决方案：
- 小顶堆（求top K用小顶堆，求last K用大顶堆）
- 优先队列（本质上也是堆）
- 桶排序
- 分治法
- Bigmap


==注意：此问题的通用解法是使用**分治法**，如果数据重复性高的话可以使用bigmap==

### 数据内容
我们首先生成10w条数据，求其中前100个：
```python
def create_test_data():
    number = 100000
    return [random.randint(1, number) for i in range(number)]
```

## 2. 小顶堆
对于堆排序，堆的调整，在以下的文章中已经详细说明了，这个地方不再细说，直接使用：[堆排序说明传送门](https://blog.csdn.net/aninstein/article/details/110282314)

因为需要求取前k个最大或者最小的值，那么按照堆的性质，如果需要求找前k个最大的数据，则我们需要构建一个小顶堆，**堆顶元素就是这第k个数的最小值**.，只要这个数据比堆顶元素大，堆顶元素就应该弹出，对当前数据进行**自顶向下**操作，得到的**新的堆顶元素就是这第k个数的新最小值**。
 
构建一个长度为k的堆，然后使用data里面的数据遍历的与这个堆的堆顶元素进行比较，如果大于堆顶元素，则弹出堆顶，当前值换到堆顶元素上，并且进行**自顶向下**的堆调整，**即进行一次堆的插入操作**

然后求解前k个数据的问题：
```python
def top_k_to_heap(data, k):
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


## 3. 优先队列（本质也是堆）
我们可以使用优先队列解决这个问题，优先队列本质上也是堆，优先级队列是不同于先进先出队列的另一种队列。每次从队列中取出的是具有**最高优先权的元素**。

在我们说堆的存储当中，一般使用数组来存储堆，即对于小顶堆：
```
           1
         /   \
        2     3
      /  \   /  \
     4    5 6    7     
```
我们可以表示为：
```
min_heap = [1, 2, 3, 4, 5, 6, 7]
```
而对于**优先队列，它的最高权值即小顶堆的堆顶元素，可以认为优先队列的权值是按照小顶堆的下标决定的。**，所以如果我们往队列中存入：[1, 3, 5, 10, 2]，自动会被排列[1, 2, 3, 5, 10]

不同语言使用了一些包可以直接调度用优先队列，比如java的import java.util.PriorityQueue，python的import heapq。这里使用heapq。
```python
def top_k_to_priority_queue(data, k):
    """
    优先队列
    :param data:
    :param k:
    :return:
    """
    if not data:
        data = create_test_data()

    queue = []
    for i in range(k):
        heapq.heappush(queue, data[i])

    for i in range(k, len(data)):
        num = data[i]
        if num < queue[0]:
            continue
        heapq.heappop(queue)
        heapq.heappush(queue, num)
    return queue
```


## 4. 桶排序
使用桶排序完成前K个问题，只是在数据比较**分散相对能够提高一定速度，数据内容主要集中在某一个范围内，那么效率则跟排序算法差不多**。使用桶排序的求前K个问题步骤：
1. 先按照当前数据范围进行分桶
2. 遍历数据，进行数据落桶
3. 计算每个桶中数据的数量，当第一个桶数据量小于K，继续到下一个桶
4. 直到加上某一个桶中的数据超过了K值，这时候再对这个桶中的数据进行桶排序，重复1-3的流程
5. 最后到桶排序的数据量到一个较小的可控范围（100左右）的时候，直接使用其他的比较排序法取得前K个

代码：
```python
def top_k_to_bucket_sort(data, k):
    """
    桶排序求Top K
    :param data: len(data) > 10000
    :param k:
    :return:
    """
    if not data:
        data = create_test_data()

    data_max = max(data)
    data_len = len(data)
    limit_num = data_len // 100  # 一个可控范围的值

    # 生成桶
    key_list = list(range(((data_max + 1) // k) + 1))  # 划定桶的范围，我们取最大值除以k
    bucket = {i: [] for i in key_list}  
    
    # 数据入桶
    for i in data:
        key = i // k
        bucket[key].append(i)

    now_len = k  # 距离k个数据的剩余值
    ret_data = []
    for i in range(len(key_list) - 1, -1, -1):
        now_bucket = bucket[key_list[i]]
        bucket_len = len(now_bucket)
        if now_len >= bucket_len:
            ret_data.extend(now_bucket)
            now_len -= bucket_len

            if now_len == 0:
                return ret_data

            # 如果这个数据在一个可接受的范围内，到下一个bucket数据中去取剩余值
            if now_len < limit_num:
                pre = 0 if i-1 == 0 else i-1
                now_bucket = bucket[key_list[pre]]
                extend_data = sort_cut_top_k(now_bucket, now_len)
                ret_data.extend(extend_data)
                return ret_data
            continue
        
        # now_len < bucket_len
        extend_data = sort_cut_top_k(now_bucket, now_len)
        ret_data.extend(extend_data)
    return ret_data
```

## 5. 分治法
分治法求解Top k问题是最常用的方法，与[快速排序](https://blog.csdn.net/aninstein/article/details/108552587)不一样的是，我们只需要求一半的快速排序，主要步骤：

1. 分治法，选择主元，大于主元的放在右边，小于主元的放在左边
2. 从右边的数据选择主元，继续（1）的操作
3. 每一次遍历都判断右边的数据长度，如果右边数据长度折半之后将会小于k，而当前又大于k，则进入第4步
4. 对剩余的右边的数据进行排序，然后截取前k个数据

代码：
```python
def top_k_to_divide(data, k):
    """
    分治法
    :param data:
    :param k:
    :return:
    """
    if not data:
        data = create_test_data()

    return divide_function(data, 0, len(data) - 1, k)


def divide_function(data, left, right, k):
    """
    实际调用的分治法方法
    :param data:
    :param left:
    :param right: 一直是len(data) - 1
    :param k:
    :return:
    """
    if left < right and k < right - left:
        pos = divide_position(data, left, right)
        # 当发现当前的数据已经小于k的时候，已经没有办法分治，此时数据量接近k，直接排序截取即可
        if k >= (right - pos):
            cut_data = data[left:]
            return sort_cut_top_k(cut_data, k)
        return divide_function(data, pos + 1, right, k)


def divide_position(data, left, right):
    index = data[right]  # 取最后一个当做主元
    i = left - 1  # 第一个数据项，由于left加进来之后+1了，这里-1
    for j in range(left, right):
        if index > data[j]:  # 如果比主元小，那么放到左边
            i += 1
            data[i], data[j] = data[j], data[i]
    # 最后调换主元与第i+1个的数据，此时的第i+1个数据肯定比主元大，放在最后面也就没啥问题了
    data[i + 1], data[right] = data[right], data[i + 1]
    return i + 1
```


## 6. BigMap
bigmap处理大数据的方法，适用的场景更大一些，比如有1亿数据，需要找出其中的前1000个数据，这时候就需要考虑到进程能够分配多少内存的问题了
```linux
题目：当我有1亿个浮点型数据，大概是0.913GB的数据，只给你1MB的内存空间，求前1000个数据
```
这个数据量在我们硬盘中是一个非常大的数据集合
我们只给进程分配1MB的内存，是肯定无法一次把所有数据内容都读取到内存中的
因此第一个需要做的，应该是把这个数据先拆分成一个个小的文件，步骤如下：
1. 把大量数据拆分成小的文件，尽管文件是小的，但是里面的数据长度还是大于k
	把数据拆分成小的文件算法：
	1）顺序读文件中，对于每个词c，取hash(c)%2000，然后按照该值存到2000个小文件中。这样每个文件大概是500k左右
	2）如果其中的有的文件超过了1M大小，还可以按照类似的方法继续往下分，直到分解得到的小文件的大小都不超过1M
2. 我们开始对拆分过后的每个文件，进行计数统计
3. 根据计数结果，取每一个小的文件的前k个数据，把这前k个数据更新到计数map
4. 遍历N个小文件之后，这个计数map被更新了N次
5. 遍历这个计数map，取出前k个数据

这个代码示例相对来说比较复杂，这里就不提供了。


## 7. 其他代码
### 7.1 公共方法
```python
def sort_cut_top_k(data, k):
    """
    排序截取前top个
    :param data: len(data) > k
    :param k:
    :return:
    """
    data = sorted(data)
    return data[len(data) - k:]


def cmp_list(list1, list2):
    """
    比对两个乱序的list内的数是否是一样的
    :param list1:
    :param list2:
    :return:
    """
    count_map1 = {}
    count_map2 = {}
    data_len = len(list1)
    if data_len != len(list2):
        return False

    for i in range(data_len):
        append_count_map(count_map1, list1[i])
        append_count_map(count_map2, list2[i])
    return operator.eq(count_map1, count_map2)
```
### 7.2 测试代码
```python
if __name__ == '__main__':
    data = create_test_data(number=30)
    print(data)
    k = 8

    heap_res = top_k_to_heap(copy.deepcopy(data), k)
    priority_res = top_k_to_priority_queue(copy.deepcopy(data), k)
    bucket_res = top_k_to_bucket_sort(copy.deepcopy(data), k)
    divide_res = top_k_to_divide(copy.deepcopy(data), k)

    print("heap_res", heap_res)
    print("priority_res", priority_res)
    print("bucket_res", bucket_res)
    print("divide_res", divide_res)

    print("heap_res is", cmp_list(priority_res, heap_res))
    print("bucket_res is", cmp_list(priority_res, bucket_res))
    print("divide_res is", cmp_list(priority_res, divide_res))
```
