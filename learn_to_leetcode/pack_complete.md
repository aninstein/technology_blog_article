# 背包问题（二）-完全背包-史上最详细解答
---
* [1. 题目](#1-题目)
* [2. 分析](#2-分析)
	* [2.1 状态表示](#21-状态表示)
	* [2.2 状态计算](#22-状态计算)
* [3. 实现](#3-实现)
* [4. 优化](#4-优化)
	* [4.1 去除k循环（时间复杂度优化）](#41-去除k循环时间复杂度优化)
		* [4.1.1 数学推算【1】](#411-数学推算1)
		* [4.1.2 代码实现](#412-代码实现)
	* [4.2 转化成一维数组解法（空间复杂度优化）](#42-转化成一维数组解法空间复杂度优化)
* [5. 测试](#5-测试)
* [参考链接](#参考链接)
---
## 1. 题目
- 问题描述：有n件物品和容量为m的背包，给出i件物品的重量以及价值value，还有数量number，求解让装入背包的物品重量不超过背包容量W，且价值V最大 。
- 特点：题干看似与01一样，但它的特点是每个物品可以无限选用。

## 2. 分析
### 2.1 状态表示
一般用dp数组来计算动态规划问题，从以下两个方面对动态规划问题进行表示
-  集合
   - v集合：物品价值
   - w集合：物品重量
   - 从前i个物品里面选取总重量<=j的所有物品的选法，**与01背包的区别在于，每一种物品是可以无限选择的**

- 属性
	- max
	- min
	- count

本题属性是属于求最大价值，为max

### 2.2 状态计算
对于完全背包的问题，遵从01背包的策略，是选择放或者不放两个状态，但是每一种物品可以放无限个，**因此可以转换为：实际上我们对于一个物品的选择就是放多少个的问题**：
我们假设一种物品选择k个（**因为背包本身是有重量限制的，所以是k个而不是无限个**）

- 选择放进去
如果选择放进去，还需要考虑放进去多少个，即：
1, 2, 3, ···, k-1, k个
表示在上一个物品的状态的时候，我的当前背包重量**j**需要减去当前**k**个物品的重量**k*w[i]**，并且整个背包的价值需要加上当前**k**个物品的价值**k*v[i]**，则状态方程为：

```python
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
dp[i][j] = max(dp[i-1][j-k*w[i]] + k*v[i], dp[i-1][j])
```

## 3. 实现
根据上面的状态转移方程我们可以得到完全背包的解法：
```python
def _complete_two_dim_k_function(data, number, total_weight):
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
        for j in range(1, col):
            for k in range(1, j):
                if j > k * w:
                    input_val = dp[i - 1][j - k*w] + k*v
                    noput_val = dp[i - 1][j]
                    dp[i][j] = max(input_val, noput_val)
                else:
                    dp[i][j] = dp[i - 1][j]
    return dp[number-1][total_weight]
```


## 4. 优化
### 4.1 去除k循环（时间复杂度优化）
#### 4.1.1 数学推算[【1】](#参考链接)
其实在上面的三层循环是一个圈复杂度比较高的代码，我们观察上述的状态方程：
```python
# 选择不放进去
dp[i][j] = dp[i-1][j]

# 选择放进去
dp[i][j] = dp[i-1][j-k*w[i]] + k*v[i]
```

k循环其实是为了寻找当前第i轮物品，选取多少个能够达到最优的值的问题，即【式子1】：
```python
# 0 < k & k*w[i] <= j
dp[i-1][j-k*w[i]] + k*v[i] = max{
	dp[i-1][j-1*w[i]] + 1*v[i],
	dp[i-1][j-2*w[i]] + 2*v[i],
	···
	dp[i-1][j-(k-1)*w[i]] + (k-1)*v[i],
	dp[i-1][j-k*w[i]] + k*v[i],
}
```

整理上面的式子，<b>使得整体减掉一个v[i]</b>可得【式子2】：
```python
# 1 < k & k*w[i] <= j
dp[i-1][j-k*w[i]] + (k-1)*v[i] = max{
	dp[i-1][j-w[i]] + 0*v[i],
	dp[i-1][j-2*w[i]] + 1*v[i],
	dp[i-1][j-3*w[i]] + 2*v[i],
	···
	dp[i-1][j-(k-1)*w[i]] + (k-2)*v[i],
	dp[i-1][j-k*w[i]] + (k-1)*v[i]
}
```

我们设dp[i-1][j-k*w[i]] + (k-1)*v[i]得到得最大值为：**Z**
则原先的状态转移方程则可以表示为：
```python
dp[i][j] = max(Z+v[i], dp[i-1][j])
```

从上述的【式子2】中，我们单独的把“j-w[i]”看做一个整体，比做大写的:**X**，可以得到【式子3】：
```python
# 0 < (k-1) & k*w[i] <= j
X = j-w[i]
dp[i][j] = dp[i-1][j-k*w[i]] + k*v[i] = max{
	dp[i-1][X-0*w[i]] + 0*v[i],
	dp[i-1][X-1*w[i]] + 1*v[i],
	dp[i-1][X-3*w[i]] + 2*v[i],
	···
	dp[i-1][X-(k-1)*w[i]] + (k-1)*v[i]  # 此处最多只能到k-1个
} + v[i]
```
对于单独的表示dp[i][j-w[i]]，是【式子4】：
```python
# 0 < k & (k+1)*w[i] <= j
dp[i][X] = dp[i-1][X-k*w[i]] + k*v[i]  # 即上述【式子4】中的max部分
```

可以看到【式子3】的k范围是： 0 < (k-1) & k*w[i] <= j
我们使**大写K = k-1**
则有【式子5】：
```python
# 0 < (k-1) & k*w[i] <= j
K = k - 1
# 1 < k & (k+1)*w[i] <= j
dp[i][j] = dp[i-1][j-k*w[i]] + k*v[i] = max{
	dp[i-1][X-0*w[i]] + 0*v[i],
	dp[i-1][X-1*w[i]] + 1*v[i],
	dp[i-1][X-3*w[i]] + 2*v[i],
	···
	dp[i-1][X-K*w[i]] + K*v[i]
} + v[i] = dp[i][X] + v[i]
```

则【式子4】和【式子5】则可以得到
dp[i][j-w[i]]选k-1个与dp[i][j]选k个的结果是完全一样的
因此可以得到，实际上我们赋值dp[i][j]的时候只需要从“dp[i][j-w[i]]+v[i]”和“dp[i-1][j]”中选择即可，即优化后的状态转移方程：
```python
dp[i][j] = max(dp[i-1][j], dp[i][j-w[i]]+v[i])
```

#### 4.1.2 代码实现
根据上述的新的状态转移方程，可以得到新的实现：
```python
def _complete_two_dim_function(data, number, total_weight):
    """
    时间复杂度优化，去除了k循环
    状态转移方程：
    dp[i][j] = max(dp[i][j-w[i]] + v[i], dp[i-1][j])
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
        for j in range(w, col):
            if j >= w:
                input_val = dp[i][j - w] + v
                noput_val = dp[i - 1][j]
                dp[i][j] = max(input_val, noput_val)
            else:
                dp[i][j] = dp[i - 1][j]
                break  # 如果w >= j了这个循环就没必要继续了
    return dp[number - 1][total_weight]
```


### 4.2 转化成一维数组解法（空间复杂度优化）
和01背包的优化逻辑一样，**i**这个变量其实就是表示“第i个”的一个递增序列，实际的这个**背包的当前的状态只有重量（w）和价值（v）**
根据刚才的状态方程：
```python
# 不放进去
dp[i][j]=dp[i-1][j]

# 放进去
dp[i][j]=dp[i][j-w[i]] + v[i]
```
观察两个状态方程，可以看到对于背包重量的状态**j**是与**i**无关，因此可以把上述方程简化为：
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
def _complete_one_dim_function(data, number, total_weight):
    """
    状态转移方程：
    i：表示第几个物品
    k：表示重量几许
    dp[k] = max(value[i]+dp[k-weight[i]], dp[k])
    :param data:
    :param number:
    :param total_weight:
    :return:
    """
    # 由于数据从1开始计算因此+1
    row = number + 1
    col = total_weight + 1
    dp = np.array([0] * col)
    for i in range(1, row):
        if i == len(data):
            break
        item = data[i]
        # 这个地方需要正序列遍历，原因是因为完全背包算法实际上是需要进行自我比对的
        # 也就是说我当前的这一轮可以被重复，也就是说一个物品可以放进去多次
        v = item.get("value")
        w = item.get("weight")
        for j in range(w, col):
            dp[j] = max(dp[j - w] + v, dp[j])
    return dp[total_weight]
```
此处为何与01背包不同（[01背包链接](https://blog.csdn.net/aninstein/article/details/108061603)），是**正序列遍历j**
首先我们观察优化后和优化前的状态转移方程：
```python
# 优化之前
dp[i][j] = max(dp[i][j-w[i]] + v[i], dp[i-1][j])

# 优化之后
dp[j] = max(dp[j-w[i]] + v[i], dp[j])
```

因此实际上优化后的状态转移方程是：
```
dp[j](第i轮的新值) = max(dp[j-w[i]] + v[i]（第i轮的新值）, dp[j]（第i-1轮的旧值）)
```

对比01背包的状态转移方程[【2】](#参考链接)：
```
dp[j](第i轮的新值) = max(dp[j-w[i]] + v[i]（第i-1轮的旧值）, dp[j]（第i-1轮的旧值）)
```

我们从01背包中可以知道，想要保证每个物品只被使用一次，就要保证每一次与**第i轮**比较的数据都是第**第i-1轮**的旧数据。因此在01背包中需要逆序。

但是在完全背包中，需要与当前**第i轮**比较的数据也是**第i轮**的，这就刚好使用正序遍历即可。原因是<b>j-w[i]</b>是做减法的，而这个**j**又是数组的下标，做**减法**之后就表示是之前的数据。因此此处正序遍历，这个数据就已经是**第i轮**更新的数据与**第i轮**的数据进行比较了。



## 5. 测试
我们给出01背包的测试数据
```
{
	"things_num": 10,
	"items": [{
		"value": 86,
		"number": 999999,
		"weight": 28
	}, {
		"value": 553,
		"number": 999999,
		"weight": 7
	}, {
		"value": 27,
		"number": 999999,
		"weight": 29
	}, {
		"value": 246,
		"number": 999999,
		"weight": 33
	}, {
		"value": 55,
		"number": 999999,
		"weight": 62
	}, {
		"value": 403,
		"number": 999999,
		"weight": 77
	}, {
		"value": 234,
		"number": 999999,
		"weight": 19
	}, {
		"value": 216,
		"number": 999999,
		"weight": 30
	}, {
		"value": 481,
		"number": 999999,
		"weight": 1
	}, {
		"value": 387,
		"number": 999999,
		"weight": 42
	}],
	"total_weight": 331
}
```
输出：
```
159211
```

## 参考链接
[【1】时间复杂度优化： https://blog.csdn.net/ACM_hades/article/details/89190424](https://blog.csdn.net/ACM_hades/article/details/89190424)

[【2】01背包详解：https://blog.csdn.net/aninstein/article/details/108061603](https://blog.csdn.net/aninstein/article/details/108061603)


## 下一章：[背包问题（三）-多重背包（简单）-史上最详细解答](https://blog.csdn.net/aninstein/article/details/108114814)