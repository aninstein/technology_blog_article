# 背包问题（三）-多重背包（简单）-史上最详细解答
---

* [1. 题目](#1-题目)
* [2. 分析](#2-分析)
	* [2.1 状态表示](#21-状态表示)
	* [2.2 状态计算](#22-状态计算)
* [3. 实现](#3-实现)
* [4. 优化](#4-优化)
	* [4.1 去除k循环（时间复杂度优化）](#41-去除k循环时间复杂度优化)
	* [4.2 转化成一维数组解法（空间复杂度优化）](#42-转化成一维数组解法空间复杂度优化)
* [5. 测试](#5-测试)
* [参考链接](#参考链接)
* [进阶：多重背包（中等）](#进阶多重背包中等)

---
## 1. 题目
- 问题描述：有n件物品和容量为m的背包，给出i件物品的重量以及价值value，还有数量number，求解让装入背包的物品重量不超过背包容量W，且价值V最大 。
- 特点 ：它与完全背包有类似点，特点是每个物品都有了一定的数量。

## 2. 分析
### 2.1 状态表示
一般用dp数组来计算动态规划问题，从以下两个方面对动态规划问题进行表示
-  集合
   - v集合：物品价值
   - w集合：物品重量
   - 从前i个物品里面选取总重量<=j的所有物品的选法，**与[完全背包](https://blog.csdn.net/aninstein/article/details/108091495)的区别在于，每一种物品是有个数限制的，不能无限选择**
   - 因此此处需要多一个num集合：每个物品的数量

- 属性
	- max
	- min
	- count

本题属性是属于求最大价值，为max

### 2.2 状态计算
对于多重背包的问题，遵从01背包的策略，是选择放或者不放两个状态，但是每一种物品可以放最多num[i]个，**因此可以转换为：实际上我们对于一个物品的选择就是放多少个的问题，最多放num[i]个的问题**：
我们假设一种物品选择k个（**除了背包本身重量限制，k还受到每一类物品数量num[i]的限制**），则k的范围为：**0 < k && k * w[i] <= j &&  k <= num[i]**

- 选择放进去
如果选择放进去，还需要考虑放进去多少个，即：
1, 2, 3, ···, k-1, k个且（0 < k && k * w[i] <= j &&  k <= num[i]）
表示在上一个物品的状态的时候，我的当前背包重量**j**需要减去当前**k**个物品的重量**k*w[i]**，并且整个背包的价值需要加上当前**k**个物品的价值**k*v[i]**，则状态方程为：

```python
# 0 < k && k * w[i] <= j &&  k <= num[i]
dp[i][j] = dp[i-1][j-k*w[i]] + k*v[i]
```

- 选择不放进去
实际上如果选择不放进去的时候，表示**放进去的是0个，需要减去的k*w[i]和需要加上的k*v[i]都为0**选择不放进去的状态方程则为：
```python
# dp[i][j] = dp[i-1][j-0*w[i]] + 0*v[i]
dp[i][j] = dp[i-1][j]
```

由此我们可以得到状态转移方程：
```python
# 0 < k && k * w[i] <= j &&  k <= num[i]
dp[i][j] = max(dp[i-1][j-k*w[i]] + k*v[i], dp[i-1][j])
```

## 3. 实现
根据上面的状态转移方程我们可以得到多重背包的解法：
```python
def _multiple_two_dim_k_function(data, number, total_weight):
    """
    状态转移方程：
    dp[i][j] = max(dp[i-1][j-k*w[i]] + k*v[i], dp[i-1][j]) (0<k<=num[i])
    :param data:
    :param number:
    :param total_weight:
    :return:
    """
    # 由于数据从1开始计算因此+1
    row = number + 1
    col = total_weight + 1
    # dp = [[0] * col for _ in range(row)]
    dp = np.array([0] * (row * col)).reshape(row, col)
    for i in range(1, row):
        if i == len(data):
            break
        item = data[i]
        v = item.get("value")
        w = item.get("weight")
        num = item.get("number")
        for j in range(1, col):
            for k in range(1, num + 1):  # 最多只能到num[i]
                if j >= k * w:
                    input_val = dp[i - 1][j - k * w] + k * v
                    noput_val = dp[i - 1][j]
                    dp[i][j] = max(input_val, noput_val)
                else:
                    dp[i][j] = dp[i - 1][j]
                    break  # 如果k * w >= j了这个循环就没必要继续了
    return dp[number - 1][total_weight]
```


## 4. 优化
### 4.1 去除k循环（时间复杂度优化）
==此处不能够去除K循环！！==
在完全背包算法中我们用简单的替换，可以把状态转移方程中的k给去除，原因**是每一个物品的k的范围是固定的，我们可以把k当做公因式进行提取。**
而在多重背包当中，因为**k不仅与重量j有关，还与当前物品的最多可以选择的数量有关，因此k是不能够被当做公因式处理**，也就不能够用完全背包的化简方式进行去除。


### 4.2 转化成一维数组解法（空间复杂度优化）
和01背包的优化逻辑一样，**i**这个变量其实就是表示“第i个”的一个递增序列，实际的这个**背包的当前的状态只有重量（w）和价值（v）**
根据刚才的状态方程：
```python
# 不放进去
dp[i][j]=dp[i-1][j]

# 放进去
dp[i][j]=dp[i-1][j-k*w[i]] + k*v[i]
```
观察两个状态方程，可以看到对于背包重量的状态**j**是与**i**无关，因此可以把上述方程简化为：
```python
# 不放进去时候，重量不变，价值不变
dp[j] = dp[j] 

# 放进去的时候，背包重量和价值的变化
dp[j] = dp[j-k*w[i]] + k*v[i]
```
因此可以得到状态转移方程为：
```python
# 0 < k & k*w[i] <= j && k <= num[i]
dp[j] = max(dp[j-k*w[i]] + k*v[i], dp[j])
```
根据上述的状态转移方程来实现代码：
```python
def _multiple_one_dim_k_function(data, number, total_weight):
    """
    状态转移方程：
    空间复杂度优化，一维数组实现法
    dp[j] = max(dp[j-k*w[i]] + k*v[i], dp[j]) (0 < k && k * w[i] <= j && k <= num[i])
    :param data:
    :param number:
    :param total_weight:
    :return:
    """
    # 由于数据从1开始计算因此+1
    row = number + 1
    col = total_weight + 1
    # dp = [[0] * col for _ in range(row)]
    dp = np.array([0] * col)
    for i in range(1, row):
        if i == len(data):
            break
        item = data[i]
        v = item.get("value")
        w = item.get("weight")
        num = item.get("number")
        for j in range(col, w, -1):
            for k in range(1, num + 1):
                if j >= k * w:
                    dp[j] = max(dp[j - k * w] + k * v, dp[j])
    return dp[total_weight]
```
此处为何与01背包[【1】](#参考链接)相同，和完全背包[【2】](#参考链接)不同？，此处又是**逆序列遍历j**
首先我们观察优化后和优化前的状态转移方程：
```python
# 0 < k && k * w[i] <= j && k <= num[i]
# 优化之前
dp[i][j] = max(dp[i-1][j-k*w[i]] + k*v[i], dp[i-1][j])

# 优化之后
dp[j] = max(dp[j-k*w[i]] + k*v[i], dp[j])
```

因此实际上优化后的状态转移方程是：
```
dp[j](第i轮的新值) = max(dp[j-k*w[i]] + k*v[i]（第i-1轮的旧值）, dp[j]（第i-1轮的旧值）)
```

对比01背包的状态转移方程：
```
dp[j](第i轮的新值) = max(dp[j-w[i]] + v[i]（第i-1轮的旧值）, dp[j]（第i-1轮的旧值）)
```
由状态转移方程可以看出来，多重背包和01背包都需要保证每一次与**第i轮**比较的数据都是第**第i-1轮**的旧数据。
原因是<b>j-k*w[i]</b>是做减法的，而这个**j**又是数组的下标，做**减法**之后就表示是之前的数据。因此此处逆序遍历，数据才能保证是**第i轮**更新的数据与**第i-1轮**的旧数据进行比较。



## 5. 测试
我们给出01背包的测试数据
```json
{
	"things_num": 10,
	"items": [{
		"value": 7,
		"number": 5,
		"weight": 1
	}, {
		"value": 13,
		"number": 2,
		"weight": 4
	}, {
		"value": 18,
		"number": 1,
		"weight": 1
	}, {
		"value": 5,
		"number": 1,
		"weight": 7
	}, {
		"value": 20,
		"number": 3,
		"weight": 10
	}, {
		"value": 19,
		"number": 1,
		"weight": 9
	}, {
		"value": 6,
		"number": 5,
		"weight": 10
	}, {
		"value": 12,
		"number": 4,
		"weight": 9
	}, {
		"value": 8,
		"number": 1,
		"weight": 3
	}, {
		"value": 10,
		"number": 4,
		"weight": 6
	}],
	"total_weight": 37
}
```
输出：
```
92
```

## 参考链接
[【1】01背包详解：https://blog.csdn.net/aninstein/article/details/108061603](https://blog.csdn.net/aninstein/article/details/108061603)

[【2】完全背包详解：https://blog.csdn.net/aninstein/article/details/108091495](https://blog.csdn.net/aninstein/article/details/108091495)

## 进阶：[多重背包（中等）]()
