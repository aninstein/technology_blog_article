# 时间复杂度O(N)的排序：计数排序，桶排序，基数排序
---

* [时间复杂度O(N)的排序：计数排序，桶排序，基数排序](#时间复杂度on的排序计数排序桶排序基数排序)
	* [1. 计数排序](#1-计数排序)
	* [2. 桶排序](#2-桶排序)
	* [3. 基数排序](#3-基数排序)
	* [4. 本文代码链接：https://github.com/aninstein/HappyPython](https://github.com/aninstein/HappyPython/blob/c123a7064b0c9f5213d8f3b4bd905927f5f504fb/python/algorithm_sort/function_sort_On.py)
---
## 1. 计数排序
计数排序，顾名思义，这个排序的主要作用并不是排序，而是进行计数。
计数排序用于**数据量内容固定，且数据范围较小**的情况，对需要排序的数列进行计数；比如对学生考试分数进行排序，分数值是一个固定的范围0-100，且数据范围不大，则可以使用计数排序。
计数排序步骤：
1. 如果数据内容是正整数，则可以创建一个数组，如果是其他类型的数据，则可以创建一个map
2. 遍历需要排序的数据，按照下标或者map的key，计算同一个数据出现的次数
3. 遍历数组或者map，按照排序结果生成数据

```python
def count_sort(data, start=0, end=100):
    """
    计数排序
    :param data:
    :param start: 数据范围起始
    :param end: 数据范围结束
    :return:
    """
    count_list = [0 for i in range(end-start)]
    for i in data:
        count_list[i-start] += 1

    ret_data = []
    for i, count in enumerate(count_list):
        if not count:
            continue
        ret_data.extend([i+start] * count)
    return ret_data
```
输出结果：
```linux
input: [1, 4, 5, 1, 5, 8, 7, 5, 9, 6, 7, 4, 5, 6, 7, 0]
output: [0, 1, 1, 4, 4, 5, 5, 5, 5, 6, 6, 7, 7, 7, 8, 9]
```

## 2. 桶排序
桶排序，先准备好一个数据范围，先把相关的数据分在不同的“桶”中，再对桶中的小批量数据进行输出排序输出。
1. 准备好固定的数据范围，比如输入数据范围是：1-10000，我们可以准备100个桶，即第一个桶范围是1-100，第二个桶是101-200···
2. 遍历数据，把对应范围的数据放到桶中
3. 遍历桶，取出桶中的数据，然后进行排序输出

有此我们可以把桶排序的算法分为三部分：
- 生成桶：针对数据范围生成合适的桶这个操作是决定桶排序的时间复杂度的主要因素
- 把数据放进对应的桶中：数据放入桶中的操作算法有很多，比如：
	- 除了if/else if语句
	- switch/case语句
	- 向下取整求取浮点数范围的方法
	- 除以10、100、1000这样的大范围数划分范围
- 对于已经放进桶中的数据进行排序：因为此时桶中的数据内容已经相对来说比较小了，可以使用插入排序等排序方法，当然要是不嫌麻烦也可以使用快排等时间复杂度为O(nlogn)的方法

桶排序适用于：
- 数据内容不固定，可以是浮点的也可以是整型的，只需要动态计算桶的大小即可
- 数据的范围有限
```python
# -*- coding: utf-8 -*-
# author: www.lichangan.com

"""
桶排序
1）在额外空间充足的情况下，尽量增大桶的数量
2）使用的映射函数能够将输入的 N 个数据均匀的分配到 K 个桶中
  个人理解，如果都是整数还可以用计数排序来计数统计然后排序，但是如果是一个连续空间内的排序，即统计的是一个浮点类型的数组成的数组，那么，就无法开辟一个对应的空间使其一一对应的存储。此时，我们需要新建一个带有存储范围的空间，来存储一定范围内的元素
空间复杂度：O(n)
时间复杂度: O(n)
稳定
"""


def bucket_sort(arr, max_num):
    """
    本算法是对浮点数进行排序，此处的放入桶中的方法为对浮点数取整
    """
    buf = {i: [] for i in range(int(max_num)+1)}  # 不能使用[[]]*(max+1)，这样新建的空间中各个[]是共享内存的
    arr_len = len(arr)
    for i in range(arr_len):
        num = arr[i]
        buf[int(num)].append(num)  # 将相应范围内的数据加入到[]中
    arr = []
    for i in range(len(buf)):
        if buf[i]:
            arr.extend(sorted(buf[i]))  # 这里还需要对一个范围内的数据进行排序，然后再进行输出
    return arr


if __name__ == "__main__":
    lis = [3.1, 4.2, 3.3, 3.5, 2.2, 2.7, 2.9, 2.1, 1.55, 4.456, 6.12, 5.2, 5.33, 6.0, 2.12]
    print(bucket_sort(lis, max(lis)))
```
输出结果：
```linux
input: [3.1, 4.2, 3.3, 3.5, 2.2, 2.7, 2.9, 2.1, 1.55, 4.456, 6.12, 5.2, 5.33, 6.0, 2.12]
output: [1.55, 2.1, 2.12, 2.2, 2.7, 2.9, 3.1, 3.3, 3.5, 4.2, 4.456, 5.2, 5.33, 6.0, 6.12]
```

## 3. 基数排序
基数排序(LDS)，**只适用于整型排序，或者有固定小数点位数的浮点型数据排序**，其概念就是，根据不同位数的数字进行排序，最终得到排序结果。
1. 先从最小的位数开始进行排序，对于排序的结果存于对应的队列中
2. 遍历0-9的栈，把数据弹出成为新的数列
3. 对下一个位数的数据重复上述操作
4. 直到所有的位数的都被轮完，从队列里面取出的数据即有序数据
```python
def radix_sort(data):

    if not data:
        return []
    max_num = max(data)  # 获取当前数列中最大值
    max_digit = len(str(abs(max_num)))  # 获取最大的位数

    dev = 1  # 第几位数，个位数为1，十位数为10···
    mod = 10  # 求余数的除法
    for i in range(max_digit):
        radix_queue = [list() for k in range(mod * 2)]  # 考虑到负数，我们用两倍队列
        for j in range(len(data)):
            radix = int(((data[j] % mod) / dev) + mod)
            radix_queue[radix].append(data[j])

        pos = 0
        for queue in radix_queue:
            for val in queue:
                data[pos] = val
                pos += 1

        dev *= 10
        mod *= 10
    return data
```
结果：
```linux
input: [58, 14, 5, 16, 78, 2, 123, 158, 753, 32, 1, 9, 5]
output: [1, 2, 5, 5, 9, 14, 16, 32, 58, 78, 123, 158, 753]
```
