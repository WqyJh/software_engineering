# 软件工程上机报告2

## Introduction

In a box bounded by [-1, 1], given m balloons(they cannot overlap) with variable radio r and position mu. And some tiny blocks are in the box at given position {d};balloons cannot overlap with these blocks. find the optimal value of r and mu which maximizes sum r^2

## Algorithm

本项目采用与项目一类似的贪心算法，但有一些不同。

首先我们为这个区域建立一个平面直角坐标系，原点为(0,0), 盒子的范围为 -1<x<1, -1<y<1， 用三元组表示圆，即(x,y,r), 其中(x,y)是坐标，r是半径。

把障碍物视为半径为0的圆。由于有障碍物的阻挡，区域与区域之间不再是严格相切，而是可能留出空隙。



整个过程中会出现四种区域：

1. 盒子的边界形成的矩形区域
   ![盒子边界区域](http://oih52y89x.bkt.clouddn.com/area_rect.png)

2. 由一个圆和两条边围成的区域

   ![盒子边界区域](http://oih52y89x.bkt.clouddn.com/area_one_circle_2.png)

3. 由两个圆和一条边围成的区域

   ![盒子边界区域](http://oih52y89x.bkt.clouddn.com/area_two_circle_2.png)

4. 由三个圆围成的区域

   ![盒子边界区域](http://oih52y89x.bkt.clouddn.com/area_three_circle_2.png)

在这几种区域中寻找最大的圆，依旧是寻找与边界相切的圆，仍然可以通过列出3个方程求解內圆。假设內圆坐标为(x, y, r)。

1. 一个圆两条边的区域

   已知圆为$(x_1, y_1, r_1)$, 两条边分别为$x=x_2$, $y=y_3$, 用直线的一般方程来表示更利于代码实现（代码简洁），即$A_1x+B_1y+C_1=0$, $A_2x+B_2y+C_2=0$, 可列出以下三个方程：

   $(x-x_1)^2 + (y-y_1)^2=(r+r_1)^2$ 

   $\frac{|A_1x+B_1y+C_1}{\sqrt{A_1^2+B_1^2}} = r$ 

   $\frac{|A_2x+B_2y+C_2}{\sqrt{A_2^2+B_2^2}} = r$

   解上面的方程组即可得到內圆$(x,y,r)$。方程的求解使用 `scipy.optimize`包中的`fsolve`函数，这个函数通过迭代法逼近方程的解。迭代的初始值对迭代的收敛性有很大影响。

   设初始值为$(x_0,y_0,r_0)$ , 其中 $ x_0=\frac{x_1+x_2}{2}$,  $y_0=\frac{y_1+y_2}{2}$,  $r_0=\min{dist1, dist2}$, 其中`dist1`和`dist2`分别表示直线1和直线2到点$(x_0,y_0)$的距离。

2. 两个圆一条边的区域

   已知圆为$(x_1, y_1, r_1)$,$(x_2, y_2, r_2)$, 一条边为 $ x=x_3$ 或 $y=y_3$,  其一般方程为$Ax+By+C=0$,  可列方程组如下：

   $(x-x_1)^2 + (y-y_1)^2=(r+r_1)^2$

   $(x-x_2)^2 + (y-y_2)^2=(r+r_2)^2$

   $\frac{|Ax+By+C}{\sqrt{A^2+B^2}} = r$

   利用`fsolve`求解方程组，赋初始值为$(x_0,y_0,r_0)$, 其中$ x_0=\frac{x_1+x_2}{2}$, $y_0=\frac{y_1+y_2}{2}$,  这表示初始值在两圆心中点位置，显然这样离结果还较远，方程有两个收敛方向，所以我们应该再移动以下初始值点$(x_0, y_0)$， 如果直线方程为$x=x_3$ 则$x_0=x_0+x_3$, 如果直线方程为$y=y_3$ 则$y_0=y_0+y_3$。

3. 三个圆的区域

   这种区域非常简单，只用距离和半径的关系列出三个方程即可解得內圆圆心。

   $(x-x_1)^2 + (y-y_1)^2=(r+r_1)^2$

   $(x-x_2)^2 + (y-y_2)^2=(r+r_2)^2$

   $(x-x_3)^2 + (y-y_3)^2=(r+r_3)^2$

   用`fsolve`求解方程组，赋初始值为$(x_0,y_0,r_0)$,  其中$(x_0,y_0)$为两个圆心的中点，半径$r_0$等于直线到$(x_0,y_0)$的距离。

   ​



对于包含障碍作为边界的区域，必须要做一些处理。在这些区域中加入一个圆之后，区域的边界与圆相切，而障碍作为一个点，恰好在圆周上。它已经不能再与內圆构成新的区域，且它与其它的圆或边界构成的区域也会失效。其它区域中与之相切的条件转化为与这个內圆相切。解决方案为，在圆集中剔除所有在新产生的內圆上的障碍。



在这几种区域中填入一个內圆后，依然会会产生三个新的区域，且区域的类型固定。

1. 区域类型1可产生一个类型1和两个类型2
2. 区域类型2可产生两个类型2和一个类型3
3. 区域类型3可产生三个类型3



算法执行的过程如下

1. 把障碍点看做半径为0的圆加入圆的集合，把四条边加入边的集合。

2. 将圆集和边集中的元素做排列组合，可以组合成3种类型的区域，每种区域的取法如下

   - 一条边，两个圆的区域

     从边集中取出一条边，从圆集中任取两个圆。

   - 两条边，一个圆的区域

     从边集中取出两条相交的边，因为平行的边不能构成有效的区域，再从圆集中取出一个圆。

   - 三个圆的区域

     从圆集中任取三个圆。

3. 对于步骤2中的每一个组合成的区域，计算区域的內圆，取半径最大的內圆和它对应的区域，每次计算要保证这个內圆不与圆集中任何一个圆（或障碍）想交，且不与边相交（这种情况主要是因为解方程收敛到错误的结果）。

4. 将步骤3取得的圆加入圆集，遍历这个区域所包含的圆，找出所有半径为0的，把它们从圆集中移除。

5. 重复步骤2~4，知道找到m个满足条件的圆。



### 算法实现

环境 Python 2.7.13

依赖 

- scipy.optmize，用于解方程
- turtle，用于绘制二维图像
- canvasvg，用于将图像导出为svg格式
- matplotlib，用于绘制坐标图
- itertools，用于排列组合





1. 数据结构定义同项目一

2. 各种情况下的內圆求解

   ```python
   # 求解一个圆，两条边的区域的內圆
   def one_circle_two_edge(circle1, edge1, edge2):
       x1, y1, r1 = circle1.x, circle1.y, circle1.r
       if edge1.A == 0:
           edge1, edge2 = edge2, edge1

       x2 = -edge1.C / edge1.A
       y3 = -edge2.C / edge2.B
       # 赋初始值
       x0 = (x1 + x2) / 2
       y0 = (y1 + y3) / 2
       r0 = min(edge1.dist_to_point(x0, y0), edge2.dist_to_point(x0, y0))

       # 定义方程组
       def equations(p):
           x, y, r = p
           return (pow(x - x1, 2) + pow(y - y1, 2) - pow(r + r1, 2),
                   edge1.dist_to_point(x, y) - r,
                   edge2.dist_to_point(x, y) - r)
   	# 用 fsolve 迭代求解方程组
       ((x, y, r), info, status, mesg) = fsolve(equations, (x0, y0, r0), full_output=True)

       if status == 1:
           return Circle(x, y, r)
       else:
           return Circle(0, 0, 0)
       
   # 求解两个圆，一条边的区域的內圆
   def two_circle_one_edge(circle1, circle2, edge):
       x1, y1, r1 = circle1.x, circle1.y, circle1.r
       x2, y2, r2 = circle2.x, circle2.y, circle2.r

       # 估算圆心的值
       x0 = (x1 + x2) / 2
       y0 = (y1 + y2) / 2

       if edge.B == 0:
           x3 = -edge.C / edge.A
           x0 = (x0 + x3) / 2  # x0向x3方向移动
       else:
           y3 = -edge.C / edge.B
           y0 = (y0 + y3) / 2  # y0向y3方向移动
   	# 计算边到(x0, y0)的距离
       r0 = edge.dist_to_point(x0, y0)
   	
       # 定义方程组
       def equations(p):
           x, y, r = p
           return (pow(x - x1, 2) + pow(y - y1, 2) - pow(r + r1, 2),
                   pow(x - x2, 2) + pow(y - y2, 2) - pow(r + r2, 2),
                   edge.dist_to_point(x, y) - r)
   	# 用 fsolve 迭代求解方程组
       ((x, y, r), info, status, mesg) = fsolve(equations, (x0, y0, r0), full_output=True)

       if status == 1:
           return Circle(x, y, r)
       else:
           return Circle(0, 0, 0)
       
   # 求解三个圆的区域的內圆
   def three_circle(circle1, circle2, circle3):
       x1, y1, r1 = circle1.x, circle1.y, circle1.r
       x2, y2, r2 = circle2.x, circle2.y, circle2.r
       x3, y3, r3 = circle3.x, circle3.y, circle3.r

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
   	# 用 fsolve 求解方程组
       ((x, y, r), info, status, mesg) = fsolve(equations, \
            (((c1.x + c2.x) / 2), (c1.y + c2.y) / 2, (c1.r + c2.r) / 2), full_output=True)
       if status == 1:
           return Circle(x, y, r)
       else:
           return Circle(0, 0, 0)
   ```

   ​

3. 对区域的抽象描述

   ```python
   # 与项目一中不同，这里删除了 new_areas() 方法
   # 因为直接采用排列组合的方法选择区域
   # 而不是将已知区域保存到队列中
   class Area(object):
       def __init__(self, atype, edges, circles):
           self.atype = atype
           self.edges = edges
           self.circles = circles
           self.in_circle = None

       class Type(object):
           ONE_CIRCLE_TWO_EDGE = 0
           TWO_CIRCLE_ONE_EDGE = 1
           THREE_CIRCLE = 2

       def inner_circle(self):
           if self.in_circle is None:
               if self.atype == Area.Type.ONE_CIRCLE_TWO_EDGE:
                   self.in_circle = \
                   one_circle_two_edge(self.circles[0], self.edges[0], self.edges[1])
               elif self.atype == Area.Type.TWO_CIRCLE_ONE_EDGE:
                   self.in_circle = \
                   two_circle_one_edge(self.circles[0], self.circles[1], self.edges[0])
               elif self.atype == Area.Type.THREE_CIRCLE:
                   self.in_circle = \
                   three_circle(self.circles[0], self.circles[1], self.circles[2])
           return self.in_circle
   ```

   ​

4. 贪心算法的实现

   ```python
   def main(m, blocks):
       # 初始化边集，在坐标轴上以顺时针顺序依次加入边集
       # 保证按顺序取两条边，他们一定相交
       edge1 = Edge(Point(1, 1), Point(1, -1))
       edge2 = Edge(Point(1, -1), Point(-1, -1))
       edge3 = Edge(Point(-1, -1), Point(-1, 1))
       edge4 = Edge(Point(-1, 1), Point(1, 1))
       edges = [edge1, edge2, edge3, edge4]
       block_filter(blocks, edges)

       circles = [] + blocks

       while m > 0:
           max_circle_area = None
           max_circle = Circle(0, 0, 0)
           # 一条边，两个圆
           for edge in edges:
               # 任取两个圆，使用 itertools 生成圆集中所有2个圆的组合
               two_circles = itertools.combinations(circles, 2)
               for two_circle in two_circles:
                   # 一条边，两个圆组成一个区域
                   area = Area(Area.Type.TWO_CIRCLE_ONE_EDGE, (edge,), two_circle)
                   # 记录最大的內圆和它对应的区域
                   if area.inner_circle().r > max_circle.r and \
                   		check_area(area, circles, edges):
                       max_circle_area = area
                       max_circle = area.inner_circle()

           # 两条边，一个圆
           for two_edge in sequence_combination(edges, 2):
               # 优化运算，两条边只能与最近的一个圆组合成一个合法区域
               c = nearest_one_circle(two_edge[0], two_edge[1], circles)
               # 组合成一个区域
               area = Area(Area.Type.ONE_CIRCLE_TWO_EDGE, two_edge, (c,))
               # 记录最大的內圆和它对应的区域
               if area.inner_circle().r > max_circle.r and \
               		check_area(area, circles, edges):
                   max_circle_area = area
                   max_circle = area.inner_circle()

           # 三个圆
           for three_circle in itertools.combinations(circles, 3):
               # 任取三个圆组成的新区域
               area = Area(Area.Type.THREE_CIRCLE, (), three_circle)
               # 记录最大的內圆和它对应的区域
               if area.inner_circle().r > max_circle.r and \
               		check_area(area, circles, edges):
                   max_circle_area = area
                   max_circle = area.inner_circle()

           if max_circle_area is not None:
               # 找到了当前最大的圆
               # 移除圆周上的障碍，这些点已经不能看作半径为 0 的圆了
               for c in max_circle_area.circles:
                   if c.r == 0:
                       circles.remove(c)
               circles.append(max_circle)
               m -= 1

       return circles
   ```

   ​

## Experiment

运行截图如下。



1个障碍，填充30个圆

![1个障碍，填充30个圆](http://oih52y89x.bkt.clouddn.com/result1.svg)

2个障碍，填充30个圆

![2个障碍，填充30个圆](http://oih52y89x.bkt.clouddn.com/result2.svg)

3个障碍，填充30个圆

![3个障碍，填充30个圆](http://oih52y89x.bkt.clouddn.com/result3.svg)

4个障碍，填充30个圆

![4个障碍，填充30个圆](http://oih52y89x.bkt.clouddn.com/result4.svg)

5个障碍，填充30个圆

![5个障碍，填充30个圆](http://oih52y89x.bkt.clouddn.com/result5.svg)

## Conclusion

增加了障碍后问题的难度提升不少，首先要能想到把障碍看做半径为0的圆，其次在把它看做半径为0的圆后计算上有相同之处和不同之处都要考虑清楚。而且之前产生固定的区域，现在要用排列组合来确定区域。多个变化导致编码和调试难度大大增加。

## Appendix

```shell
commit f3a331f1c9e9e772e201abcaf54984222ce397f2
Author: WqyJh <781345688@qq.com>
Date:   Sat Jun 17 18:39:04 2017 +0800

    Finished proj2

commit 29a19b4c27b0f7a3f1188022462a93c666ca4e10
Author: WqyJh <781345688@qq.com>
Date:   Sat Jun 17 17:56:16 2017 +0800

    Add .gitignore

commit 697d3e01b9a8fd1deafa879dccc93e2f1228dce8
Author: WqyJh <781345688@qq.com>
Date:   Sat Jun 17 15:19:43 2017 +0800

    Seems got right result

commit e807e31edbeafc2686ff4ab716c44265b8c18050
Author: WqyJh <781345688@qq.com>
Date:   Sat Jun 17 14:54:23 2017 +0800

    Switch to combination algorithm

commit 7c868a7db3a18c966ddb34d60ef187914654731f
Author: WqyJh <781345688@qq.com>
Date:   Sat Jun 17 14:47:25 2017 +0800

    Modified some util functions

commit 8ed1253dce0103b0e563a887a60e65a7a12480c6
Author: WqyJh <781345688@qq.com>
Date:   Sat Jun 17 13:42:05 2017 +0800

    Finished with one block

commit df3e8279c354794119bb831e0bd9601664c1672f
Author: WqyJh <781345688@qq.com>
Date:   Sat Jun 17 11:35:49 2017 +0800

    Fix algorithm

commit 270fdcc198a25820e41ac4a1ba6c82c7c9e993d0
Author: WqyJh <781345688@qq.com>
Date:   Fri Jun 16 21:49:31 2017 +0800

    change algorithm back to proj1

commit d0d231c8c07fcbd2a59b8392ddc57830de883e55
Author: WqyJh <781345688@qq.com>
Date:   Fri Jun 16 20:51:59 2017 +0800

    save status

commit cdd386ae0dcc13fd0bfc675fcd55d3d113a12baf
Author: WqyJh <781345688@qq.com>
Date:   Fri Jun 16 20:21:21 2017 +0800

    Add nearest_two_circle

commit 95e4e3eb8fe3a5bc5eff131a9c89581e7c9c821a
Author: WqyJh <781345688@qq.com>
Date:   Fri Jun 16 19:20:43 2017 +0800

    Add project 2

```

