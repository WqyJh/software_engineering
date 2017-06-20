# 软件工程上机文档1
## introduction
In a box bounded by [-1, 1], given m balloons(they cannot overlap) with variable radio r and position mu, find the optimal value of r and mu which maximize sum r².

## Algorithm
这是一个典型的布局优化问题，目前还没有非常有效的算法可以在短时间内求得最优解。我采用贪心算法来逼近最优解，具体就是每次都取空闲区域中最大的那个圆，即与区域边界相切的那个圆。


首先我们为这个区域建立一个平面直角坐标系，原点为(0,0), 盒子的范围为 -1<x<1, -1<y<1， 用三元组表示圆，即(x,y,r), 其中(x,y)是坐标，r是半径。

整个过程中会出现四种区域：
1. 盒子的边界形成的矩形区域
  ![盒子边界区域](http://oih52y89x.bkt.clouddn.com/area_rect.png)
2. 由一个圆和两条边围成的区域
  ![一个圆和两条边](http://oih52y89x.bkt.clouddn.com/area_on_circle.png)
3. 由两个圆和一条边围成的区域
  ![两个圆和一条边](http://oih52y89x.bkt.clouddn.com/area_two_circle.png)
4. 由三个圆围成的区域
  ![三个圆](http://oih52y89x.bkt.clouddn.com/area_three_circle.png)




在这几种区域中寻找一个与边界相切的圆并不复杂。第一种区域只有一个圆(0,0,1), 之后的选择中，不再会出现此类区域。其他几种区域可以通过列方程求解。假设內圆坐标为(x, y, r)

1. 一个圆两条边围成的区域

   已知圆为$(x_1, y_1, r_1)$, 两条边分别为$x=x_2$, $y=y_3$, 则有內圆半径$r=\frac{\sqrt2 - 1}{\sqrt2 +1}*r_1$, $x=x_2 \pm r$, $ y=y3 \pm r$ 。

2. 两个圆一条边围成的区域

   已知圆为$(x_1, y_1, r_1)​$,$(x_2, y_2, r_2)​$, 一条边为 $ x=x_3​$ 或 $y=y_3​$, 则有$r=\frac{\sqrt{r_1 r_2}}{\sqrt{r_1}+ \sqrt{r_2}}​$, 而x，y的值可以由直线到圆心的距离等于r求得，当直线方程为 $x=x_3​$ 时，有$x=x_3 \pm r​$ ，再由两圆心距离等于两半径之和可列一个方程$(x-x_1)^2 + (y-y_1)^2=(r+r_1)^2​$, 可解 y 的值。当直线方程为 $ y=y_3​$ 时同理。

3. 三个圆围成的区域

   这种区域非常简单，只用距离和半径的关系列出三个方程即可解得內圆圆心。

   $(x-x_1)^2 + (y-y_1)^2=(r+r_1)^2$

   $(x-x_2)^2 + (y-y_2)^2=(r+r_2)^2$

   $(x-x_3)^2 + (y-y_3)^2=(r+r_3)^2$

   联立以上三个方程即可解得$(x,y,r)$。



在这几种区域中填入一个內圆后，均会产生三个新的区域，且区域的类型固定。

1. 区域类型1可产生一个类型1和两个类型2
2. 区域类型2可产生两个类型2和一个类型3
3. 区域类型3可产生三个类型3



算法执行的过程如下

1. 第一个圆选(0,0,1), 填充完这个圆之后，生成了四个1型区域，将这四个区域加入队列。
2. 遍历队列，计算每一个区域的內圆的大小，取最大的那个圆，对应的区域出队，将产生的三个新区域加入队列。
3. 重复2步骤，直到选出 m 个圆。
4. 计算 m 个圆的半径之和 $\sum r^2 $。 
5. 以不同的 m 值，重复1~3过程，可以得到 m 与 $\sum r^2$ 的函数关系。



### 算法实现

环境 Python 2.7.13

依赖 

- scipy.optmize，用于解方程
- turtle，用于绘制二维图像
- canvasvg，用于将图像导出为svg格式
- matplotlib，用于绘制坐标图

数据结构定义， 点(Point) 用二维坐标表示，圆(Circle) 用三维坐标表示，边(Edge) 用直线的一般方程($Ax+By+C=0$)表示。

```python
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r


class Edge(object):
    def __init__(self, point1, point2):
        self.A = point2.y - point1.y
        self.B = point1.x - point2.x
        self.C = point2.x * point1.y - point1.x * point2.y
```

各种情况下的內圆求解

```python
# 求解一个圆与两条边类型的区域的內圆
def one_circle_two_edge(circle1, edge1, edge2):
    if edge1.A == 0:
        edge1, edge2 = edge2, edge1
    # 用公式求半径 r
    r = (math.sqrt(2) - 1) / (math.sqrt(2) + 1) * circle1.r
    x2 = -edge1.C / edge1.A
    y3 = -edge2.C / edge2.B
    # 根据上面推倒的式子计算 x 和 y
    x = x2 - r if x2 > circle1.x else x2 + r
    y = y3 - r if y3 > circle1.y else y3 + r
    return Circle(x, y, r)

# 求解两个圆与一条边类型的区域的內圆
def two_circle_one_edge(circle1, circle2, edge):
    r1, r2 = circle1.r, circle2.r
    x1, x2 = circle1.x, circle2.x
    y1, y2 = circle1.y, circle2.y
    # 用公式求半径 r
    r = pow(math.sqrt(r1 * r2) / (math.sqrt(r1) + math.sqrt(r2)), 2)
    x = y = 0
    # 边界的直线方程为 y=y3 的情况
    if edge.A == 0:
        y3 = -edge.C / edge.B
        y = y3 + r if y3 < circle1.y else y3 - r
        # 手工推导得到的 x 的解析式
        x = (-2 * (y1 - y2) * y + 2 * (r2 - r1) * r + r2 * r2 - r1 * r1 + x1 * x1 - x2 * x2 + y1 * y1 - y2 * y2) / (
            2 * (x1 - x2))
    # 边界的直线方程为 x=x3 的情况
    if edge.B == 0:
        x3 = -edge.C / edge.A
        x = x3 + r if x3 < circle1.x else x3 - r
        # 手工推导的得到的 y 的解析式
        y = (-2 * (x1 - x2) * x + 2 * (r2 - r1) * r + r2 * r2 - r1 * r1 + x1 * x1 - x2 * x2 + y1 * y1 - y2 * y2) / (
            2 * (y1 - y2))
    return Circle(x, y, r)

# 求解三个圆类型的区域的內圆，用了 scipy.optimize 包中的 fsolve 函数
# 该函数利用迭代法逼近方程的解
def three_circle(circle1, circle2, circle3):
    x1, y1, r1 = circle1.x, circle1.y, circle1.r
    x2, y2, r2 = circle2.x, circle2.y, circle2.r
    x3, y3, r3 = circle3.x, circle3.y, circle3.r
	
    # 定义方程组
    def equations(p):
        x, y, r = p
        return (pow(x - x1, 2) + pow(y - y1, 2) - pow(r + r1, 2),
                pow(x - x2, 2) + pow(y - y2, 2) - pow(r + r2, 2),
                pow(x - x3, 2) + pow(y - y3, 2) - pow(r + r3, 2))

    c1, c2, c3 = circle1, circle2, circle3
    # 将 c1, c2, c3 从小到大排列
    if c1.r > c2.r:
        c1, c2 = c2, c1
    if c2.r > c3.r:
        c2, c3 = c3, c2
        
	# 利用迭代法求解方程，迭代法的初值设为较小的两个圆的圆心的中点
    x, y, r = fsolve(equations, (((c1.x + c2.x) / 2), (c1.y + c2.y) / 2, (c1.r + c2.r) / 2))
    return Circle(x, y, r)
```

对区域的抽象描述

```python
class Area(object):
    def __init__(self, atype, edges, circles):
        self.atype = atype
        self.edges = edges
        self.circles = circles
        self.in_circle = None
	# 描述区域的类型，一共三种
    class Type(object):
        ONE_CIRCLE_TWO_EDGE = 0
        TWO_CIRCLE_ONE_EDGE = 1
        THREE_CIRCLE = 2
	
    # 调用之前实现的內圆求解函数来计算该区域的內圆
    def inner_circle(self):
        if self.in_circle is None:
            if self.atype == Area.Type.ONE_CIRCLE_TWO_EDGE:
                self.in_circle = one_circle_two_edge(self.circles[0], self.edges[0], self.edges[1])
            elif self.atype == Area.Type.TWO_CIRCLE_ONE_EDGE:
                self.in_circle = two_circle_one_edge(self.circles[0], self.circles[1], self.edges[0])
            elif self.atype == Area.Type.THREE_CIRCLE:
                self.in_circle = three_circle(self.circles[0], self.circles[1], self.circles[2])
        return self.in_circle

    # 返回填充內圆后产生的三个新区域
    def new_areas(self, inner_circle):
        # 区域类型1的情况
        if self.atype == Area.Type.ONE_CIRCLE_TWO_EDGE:
            # 产生一个类型1和两个类型2
            return [Area(Area.Type.ONE_CIRCLE_TWO_EDGE, self.edges, (inner_circle,)),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, (self.edges[0],),\
                         (self.circles[0], inner_circle)),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, (self.edges[1],),\
                         (self.circles[0], inner_circle))]
        # 区域类型2的情况
        elif self.atype == Area.Type.TWO_CIRCLE_ONE_EDGE:
            # 产生两个类型2和一个类型3
            return [Area(Area.Type.THREE_CIRCLE, (), \
                         (self.circles[0], self.circles[1], inner_circle)),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, (self.edges[0],),\
                         (self.circles[0], inner_circle)),
                    Area(Area.Type.TWO_CIRCLE_ONE_EDGE, (self.edges[0],),\
                         (self.circles[1], inner_circle))]
        # 区域类型3的情况
        elif self.atype == Area.Type.THREE_CIRCLE:
            # 产生三个类型3
            return [Area(Area.Type.THREE_CIRCLE, (), \
                         (self.circles[0], self.circles[1], inner_circle)),
                    Area(Area.Type.THREE_CIRCLE, (), \
                         (self.circles[0], self.circles[2], inner_circle)),
                    Area(Area.Type.THREE_CIRCLE, (), \
                         (self.circles[1], self.circles[2], inner_circle))]

```

贪心算法的实现

```python
def main(m):
    queue = [] # 用于保存区域的队列
    result = [] # 用于保存选中的圆的队列，按从大到小顺序排列
    circle0 = Circle(0, 0, 1) # 第一个圆(0,0,1)
    # 一下四行是四条边界
    edge1 = Edge(Point(1, 1), Point(1, -1))
    edge2 = Edge(Point(1, 1), Point(-1, 1))
    edge3 = Edge(Point(-1, 1), Point(-1, -1))
    edge4 = Edge(Point(-1, -1), Point(1, -1))
    result.append(circle0)
    # 添加第一个圆后生成四个区域1，把它们加入队列
    queue.append(Area(Area.Type.ONE_CIRCLE_TWO_EDGE, (edge1, edge2), (circle0,)))
    queue.append(Area(Area.Type.ONE_CIRCLE_TWO_EDGE, (edge2, edge3), (circle0,)))
    queue.append(Area(Area.Type.ONE_CIRCLE_TWO_EDGE, (edge3, edge4), (circle0,)))
    queue.append(Area(Area.Type.ONE_CIRCLE_TWO_EDGE, (edge4, edge1), (circle0,)))
    # 循环遍历队列，直到已经找到 m 个圆
    while len(queue) > 0 and m > 1:
        area = queue.pop() # 从队列中取出一个区域
        circle = area.inner_circle() # 计算区域的內圆
        for i in range(0, len(queue)):  # 选出圆面积最大的区域
            if queue[i].inner_circle().r > circle.r: # 与其他区域比较
                queue.append(area)
                area = queue.pop(i)
                circle = area.inner_circle()  # 总是取最大的这个圆
        # 已经找到了最大的圆
        areas = area.new_areas(circle) # 计算新产生的区域
        queue = queue + areas  # 将新产生的区域加到队列中
        result.append(circle) # 将找到的圆加到结果中
        m -= 1
    return result
```

## Experiment

运行截图如下。



填充10个圆

![填充10个圆](http://oih52y89x.bkt.clouddn.com/result10.svg)



填充20个圆

![填充20个圆](http://oih52y89x.bkt.clouddn.com/result20.svg填充30个圆

![填充30个圆](http://oih52y89x.bkt.clouddn.com/result30.svg)

填充50个圆

![填充50个圆](http://oih52y89x.bkt.clouddn.com/result50.svg)

填充100个圆

![填充100个圆](http://oih52y89x.bkt.clouddn.com/result100.svg)

填充500个圆

![填充500个圆](http://oih52y89x.bkt.clouddn.com/result500.svg)



## Conclusion

从实验结果可以看出，贪心算法具有较好的覆盖效果，具有较快的收敛速度，是一种不错的解法。算法的实现较为简单，主要的函数模块粒度适中，程序内聚性较好。

通过这次实验，锻炼了对具体需求的分析能力，建模能力与实际编码能力等，学会了使用git和github管理我的代码。

## Appendix

```shell
commit f8a3fb7e55be15d6519e1549a77900805c182b19
Author: WqyJh <781345688@qq.com>
Date:   Sun Jun 11 17:09:04 2017 +0800

    Add scale to plot function

commit cce52958f48e507330ce1874cfa84aa835a2920a
Author: WqyJh <781345688@qq.com>
Date:   Sun Jun 11 17:02:41 2017 +0800

    Fix plot and export image problem

commit ec409347336a79d8d60060494c44ca6a93b58040
Author: WqyJh <781345688@qq.com>
Date:   Sun Jun 11 16:30:07 2017 +0800

    Fix three_circle calculation problem

commit cc641a31f9eb5d5424c977112935061870f2fb5d
Author: WqyJh <781345688@qq.com>
Date:   Sun Jun 11 14:49:16 2017 +0800

    fix some gramma problem

commit 423b3f026891e76338f54992a555ddcb751cee8e
Author: WqyJh <781345688@qq.com>
Date:   Sun Jun 11 14:33:49 2017 +0800

    Finished proj1 algorithm

commit 38afeb5f6e974793b661cf84e62ca826a68071ce
Author: WqyJh <781345688@qq.com>
Date:   Sat Jun 10 20:59:50 2017 +0800

    Fix two_circle_one_edge()

commit f115c7ec6c74998aa0580eabd3b7feb504ed943b
Author: WqyJh <781345688@qq.com>
Date:   Sat Jun 10 17:35:50 2017 +0800

    Add basic data structures

```

