# 背包算法（一）-01背包-史上最详细解答
---
* [1. 题目](#1-题目)
* [2. 分析](#2-分析)
	* [2.1 状态表示](#21-状态表示)
	* [2.2 状态计算](#22-状态计算)
* [3. 实现](#3-实现)
* [4. 优化](#4-优化)
* [5. 测试](#5-测试)
---
## 1. 题目
- 问题描述：有n件物品和容量为m的背包，给出i件物品的重量以及价值value，还有数量number，求解让装入背包的物品重量不超过背包容量W，且价值V最大 。
- 特点:这是最简单的背包问题，特点是每个物品只有一件供你选择放还是不放。

## 2. 分析
### 2.1 状态表示
一般用dp数组来计算动态规划问题，从以下两个方面对动态规划问题进行表示
-  集合
   - v集合：物品价值
   - w集合：物品重量
   - 从前i个物品里面选取总重量<=j的所有物品的选法

- 属性
	- max
	- min
	- count

本题属性是属于求最大价值，为max

### 2.2 状态计算
对于0和1背包的问题，我们计算的只是两个状态，**即对于第i个物品选择放进去或者不放进去的问题。**
- 选择放进去
表示在上一个物品的状态的时候，我的当前背包重量**j**需要减去当前这个物品的重量**w[i]**，并且整个背包的价值需要加上当前这个物品的价值**v[i]**，则状态方程为：
```python
dp[i][j] = dp[i-1][j-w[i]] + v[i]
```

- 选择不放进去
实际上如果选择不放进去的时候，表示**需要减去的w[i]和需要加上的v[i]都为0**选择不放进去的状态方程则为：
```python
# dp[i][j] = dp[i-1][j-0] + 0
dp[i][j] = dp[i-1][j]
```

由此我们可以得到状态转移方程：
```python
dp[i][j] = max(dp[i-1][j-w[i]] + v[i], dp[i-1][j])
```

## 3. 实现
根据上面的状态转移方程我们可以得到01背包的二维解法：
```python
def bag_two_2_0and1(items, weight):
    # 数据是从1开始的
    data_len = len(items)
    row = data_len + 1
    col = weight + 1

    # 生成二维数组
    # 原生的Python可以这么写：
    # dp = [[0] * col for _ in range(row)]
    # 使用numpy生成一个dp数组
    dp = np.array([0] * (row * col)).reshape(row, col)
    for i in range(1, row):
        if i == data_len:
            break
        item = items[i]
        v = item.get("value")
        w = item.get("weight")
        for j in range(1, col):
            if j >= w:
                no_input = dp[i-1][j]
                yes_input = dp[i-1][j-w] + v
                dp[i][j] = max(yes_input, no_input)
            else:
                dp[i][j] = dp[i-1][j]
    return dp[data_len-1][weight]
```

## 4. 优化
可以看的出来**i**这个变量其实就是表示“第i个”的一个递增序列，实际的这个**背包的当前的状态只有重量（w）和价值（v）**
根据刚才的状态方程：
```python
# 不放进去
dp[i][j]=dp[i-1][j]

# 放进去
dp[i][j]=dp[i-1][j-w[i]] + v[i]
```
观察两个状态方程，可以看到对于背包重量的状态**j**与**i**无关，因此可以把上述方程简化为：
```python
# 不放进去时候，重量不变，价值不变
dp[j] = dp[j] 

# 放进去的时候，背包重量和价值的变化
dp[j] = dp[j-w[i]] + v[i]
```
因此可以得到状态转移方程为：
```python
dp[j] = max(dp[j-w[i]] + v[i], dp[j])
```
根据上述的状态转移方程来实现代码：
```python
def bag_one_dim_0and1(items, weight):
    # 数据是从1开始的
    data_len = len(items)
    row = data_len + 1
    col = weight + 1

    # 生成一维数组
    # 原生的Python可以这么写：
    # dp = [[0] * col]
    # 使用numpy生成一个dp数组
    dp = np.array([0] * col)
    for i in range(1, row):
        if i == data_len:
            break
        item = items[i]
        v = item.get("value")
        w = item.get("weight")
        for j in range(weight, w, -1):
            dp[j] = max(dp[j-w]+v, dp[j])
    return dp[weight]
```
[【1】此处为何倒序遍历呢？](https://www.cnblogs.com/qie-wei/p/10160169.html)
首先我们观察优化后和优化前的状态转移方程：
```python
# 优化之前
dp[i][j] = max(dp[i-1][j-w[i]] + v[i], dp[i-1][j])

# 优化之后
dp[j] = max(dp[j-w[i]] + v[i], dp[j])
```
因此实际上优化后的状态转移方程是：
```
dp[j](第i轮的新值) = max(dp[j-w[i]] + v[i]（第i-1轮的旧值）, dp[j]（第i-1轮的旧值）)
```
优化后的状态转移方程实际上就是**用最新的值把上一轮的值覆盖掉**，所以可以在一个一维数组中完成状态转移，而且得保证：**这一轮状态只能是由上一轮的状态推出来的。**
为什么需要逆序遍历，此处如果从背包问题的物理操作去解释不好解释，简单的从数学上去理解就是：

我们这个<b>j-w[i]</b>是做减法的，而这个**j**又是数组的下标，做**减法**之后就表示是之前的数据。由于需要用新的值把旧的值进行覆盖，就需要保证在此数据是没有被改动过的，也就是原封不动**第i-1轮**的数据与当前**第i轮**的数据进行比较。因此此处如果是顺序的话，这个数据就已经是**第i轮**更新的数据与**第i轮**的数据进行比较了。



## 5. 测试
我们给出01背包的测试数据
```
{
	'items': [{
		'number': 1,
		'weight': 49,
		'value': 241
	}, {
		'number': 1,
		'weight': 25,
		'value': 724
	}, {
		'number': 1,
		'weight': 91,
		'value': 780
	}, {
		'number': 1,
		'weight': 76,
		'value': 824
	}, {
		'number': 1,
		'weight': 92,
		'value': 968
	}, {
		'number': 1,
		'weight': 53,
		'value': 276
	}, {
		'number': 1,
		'weight': 6,
		'value': 492
	}, {
		'number': 1,
		'weight': 53,
		'value': 745
	}, {
		'number': 1,
		'weight': 62,
		'value': 136
	}, {
		'number': 1,
		'weight': 94,
		'value': 568
	}],
	'total_weight': 200,
	'things_num': 10
}
```
输出：
```
3008
```


## 下一章：[背包问题（二）-完全背包-史上最详细解答](https://editor.csdn.net/md/?articleId=108091495)