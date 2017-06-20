# 软件工程上机报告3

## Introduction

In a box(3D) bounded by [-1, 1], given m balloons(they cannot overlap) with variable radio r and position mu. And some tiny blocks are in the box at given position {d};balloons cannot overlap with these blocks. find the optimal value of r and mu which maximizes sum r^2

## Algorithm

这个项目是项目二的扩展，算法框架不变，只是数据增加了一个维度，解方程时多了一个变量而已。

首先我们为这个区域建立一个空间直角坐标系，原点为(0,0), 盒子的范围为 $-1 \leq x,y,z \leq 1$, 用四元组表示球，即(x,y,z,r), 其中(x,y,z)是坐标，r是半径。把障碍物视为半径为0的球。

整个过程会出现5种区域，比平面的情况多了一种：

1. 6个面围成的区域

   这块区域并无作用，仅作为初始条件。

2. 一个球和三个面围成的区域

   对应于项目二中一个圆两条边的区域。

3. 两个球和两个面围成的区域

   这是三维情况下多出来的一种情况，求解方式不变。

4. 三个球和一条边围成的区域

   对应于项目二中两个圆一条边的区域。

5. 四个球围成的区域

   对应于项目二中三个圆围成的区域。



在这几种区域中最大的球，仍然是寻找与所有边界相切的球，可以通过列出4个方程求解。假设内球为(x,y,z,r)。

1. 一个球和三个面围成的区域

   已知球为$(x_1,y_1,z_1,r_1)$,  三个面分别为$x=x_2$, $y=y_3$, $z=z_4$, 用平面的一般方程来表示更利于代码实现（代码简洁），即$A_1x+B_1y+C_1z+D=0$,$A_2x+B_2y+C_2z+D=0$,$A_3x+B_3y+C_3z+D=0$, 可列出一下四个方程：

   $(x-x_1)^2 + (y-y_1)^2 + (z-z_1)^2=(r+r_1)^2$ 

   $\frac{|A_1x+B_1y+C_1z+D}{\sqrt{A_1^2+B_1^2+C_1^2}} = r$ 

   $\frac{|A_2x+B_2y+C_2z+D}{\sqrt{A_2^2+B_2^2+C_2^2}} = r$

   $\frac{|A_3x+B_3y+C_3z+D}{\sqrt{A_3^2+B_3^2+C_3^2}} = r$

   解上面的方程组即可得到內球$(x,y,z,r)$。方程的求解使用 `scipy.optimize`包中的`fsolve`函数，这个函数通过迭代法逼近方程的解。迭代的初始值对迭代的收敛性有很大影响。

   设初始值为$(x_0,y_0,r_0)$ , 其中 $ x_0=\frac{x_1+x_2}{2}$,  $y_0=\frac{y_1+y_2}{2}$,  $z_0=\frac{z_1+z_2}{2}$, $r_0=\min_{i=0,1,2} di$, 其中`d1`,`d2`和`d3`分别表示三个平面到点$(x_0,y_0,z_0)$的距离。

2. 两个球和两个面围成的区域

   已知两个球为$(x_1, y_1, z_1, r_1)$,$(x_2, y_2, z_2, r_2)$, 两个面的一般方程为$A_1x+B_1y+C_1z+D=0$, $ A_2x+B_2y+C_2z+D=0$ 可列方程组如下：

   $(x-x_1)^2 + (y-y_1)^2 + (z-z_1)^2=(r+r_1)^2$

   $(x-x_2)^2 + (y-y_2)^2 + (z-z_2)^2 =(r+r_2)^2$

   $\frac{|A_1x+B_1y+C_1z+D_1}{\sqrt{A_1^2+B_1^2+C_1^2}} = r$

   $\frac{|A_2x+B_2y+C_2z+D_2}{\sqrt{A_2^2+B_2^2+C_2^2}} = r$ 

   利用`fsolve`求解方程组，赋初始值为$(x_0,y_0,z_0,r_0)$, 其中$ x_0=\frac{x_1+x_2}{2}$, $y_0=\frac{y_1+y_2}{2}$,  $z_0=\frac{z1+z2}{2}$, 这表示初始值在两球心中点位置，显然这样离结果还较远，方程有三个收敛方向，所以我们应该视情况将初始点向两个面的方向移动一下。

   移动逻辑如下：

   如果平面方程为$x=x_*$, 则$x_0 = \frac{x_0 + x_*}{2}$, 如果平面方程为$y=y_*$, 则$y_0=\frac{y_0+y_*}{2}$, 如果平面方程为$z=z_*$, 则$z_0=\frac{z_0+z_*}{2}$。半径$r_0=\min_{i=0,1,2} di$, 其中`d1`,`d2`分别表示两个个平面到点$(x_0,y_0,z_0)$的距离。

   对于两个平面，都按上述移动算法处理一下初始值。

3. 三个球和一个面围成的区域

   已知三个球为$(x_1, y_1, z_1, r_1)$,$(x_2, y_2, z_2, r_2)$, $(x_3,y_3,z_3,r_3)$, 平面的一般方程为$Ax+By+Cz+D=0$, 可列方程组如下：

   $(x-x_1)^2 + (y-y_1)^2 + (z-z_1)^2=(r+r_1)^2$

   $(x-x_2)^2 + (y-y_2)^2 + (z-z_2)^2 =(r+r_2)^2$

   $(x-x_3)^2 + (y-y_3)^2 + (z-z_3)^2=(r+r_3)^2$

   $\frac{|Ax+By+Cz+D}{\sqrt{A^2+B^2+C^2}} = r$

   利用`fsolve`求解方程组，赋初始值为$(x_0,y_0,z_0,r_0)$, 其中$x_0=\frac{x_1+x_2+x_3}{2}$, $y_0=\frac{y_1+y_2+y_3}{2}$, $z_0=\frac{z_1+z_2+z_3}{2}$, 并且需视情况向平面移动，移动逻辑同2。

4. 四个球围成的的区域

   这种区域非常简单，只用距离和半径的关系列出四个个方程即可解得內球球心。

   $(x-x_1)^2 + (y-y_1)^2 + (z-z_1)^2=(r+r_1)^2$

   $(x-x_2)^2 + (y-y_2)^2 + (z-z_2)^2 =(r+r_2)^2$

   $(x-x_3)^2 + (y-y_3)^2 + (z-z_3)^2=(r+r_3)^2$

   $(x-x_4)^2 + (y-y_4)^2 + (z-z_4)^2=(r+r_4)^2$

   用`fsolve`求解方程组，赋初始值为$(x_0,y_0,z_0,r_0)$,  其中$(x_0,y_0,z_0)$为任意两个心的球中点，半径$r_0$等于两个球半径的均值。



对于包含障碍作为边界的区域，必须要做一些处理。在这些区域中加入一个球之后，区域的边界与球相切，而障碍作为一个点，恰好在球表面上。它已经不能再与內球构成新的区域，且它与其它的球或平面构成的区域也会失效。其它区域中与之相切的条件转化为与这个內球相切。解决方案为，在球集中剔除所有在新产生的內球上的障碍。



在这几种区域中填入一个內球后，依然会会产生三个新的区域，且区域的类型固定。

1. 区域类型1可产生一个类型1和两个类型2
2. 区域类型2可产生两个类型2和一个类型3
3. 区域类型3可产生三个类型3

算法执行的过程如下

1. 把障碍点看做半径为0的球加入球的集合，把六个平面加入面的集合。

2. 将球集和面集中的元素做排列组合，可以组合成4种类型的区域，每种区域的取法如下

   - 一个球和三个面围成的区域

     从球集中任取一个球，从面集中任取三个面，判断三个面是否两两相交，如果不相交，重新取三个面。

   - 两个球和两个面围成的区域

     从球集中任取两个球，从面集中任取两个面，判断两个面是否相交，如果不想交，重新取两个面。

   - 三个球和一个面围成的区域

     从球集中任取三个球，从面集中任取一个面。

   - 四个球围成的区域

     从球集中任取四个球。

3. 对于步骤2中的每一个组合成的区域，计算区域的內球，取半径最大的內球和它对应的区域，每次计算要保证这个內球不与球集中任何一个球（或障碍）想交，且不与平面相交（这种情况主要是因为解方程收敛到错误的结果）。

4. 将步骤3取得的球加入球集，遍历这个区域所包含的球，找出所有半径为0的，把它们从球集中移除。

5. 重复步骤2~4，知道找到m个满足条件的球。



### 算法实现

环境 

- Python 2.7.13
- Jupyter notebook 4.3.0

依赖 

- scipy.optmize，用于解方程
- itertools，用于排列组合
- ivisual，用于绘制三维图像



1. 数据结构定义

   ```python
   class Point(object):
       def __init__(self, x, y, z):
           self.x = x
           self.y = y
           self.z = z
   ```

2. 各种情况下的内球求解


   ```python
    # 一个球三个平面围成的区域
      def one_sphere_three_plane(sphere1, plane1, plane2, plane3):
          x1, y1, z1, r1 = sphere1.x, sphere1.y, sphere1.z, sphere1.r
          planes = [plane1, plane2, plane3]
          plane1, plane2, plane3 = plane_A_neq_0(planes), plane_B_neq_0(planes),\ 															plane_C_neq_0(planes)
          x2 = -plane1.D / plane1.A
          y3 = -plane2.D / plane2.B
          z4 = -plane3.D / plane3.C
          # 迭代初始值
          x0 = (x1 + x2) / 2
          y0 = (y1 + y3) / 2
          z0 = (z1 + z4) / 2
          r0 = min(plane1.dist_to_point(x0, y0, z0), plane2.dist_to_point(x0, y0, z0),\ 													plane3.dist_to_point(x0, y0, z0))
      	# 定义方程组
          def equations(p):
              x, y, z, r = p
              return (pow(x - x1, 2) + pow(y - y1, 2) + pow(z - z1, 2) - pow(r + r1, 2),
                      plane1.dist_to_point(x, y, z) - r,
                      plane2.dist_to_point(x, y, z) - r,
                      plane3.dist_to_point(x, y, z) - r)
      	# 用 fsolve 解方程
          x, y, z, r = fsolve(equations, (x0, y0, z0, r0))
          return Sphere(x, y, z, r)

      # 两个球两个平面围成的区域
      def two_sphere_two_plane(sphere1, sphere2, plane1, plane2):
          x1, y1, z1, r1 = sphere1.x, sphere1.y, sphere1.z, sphere1.r
          x2, y2, z2, r2 = sphere2.x, sphere2.y, sphere2.z, sphere2.r
      	# 迭代初始值
          x0 = (x1 + x2) / 2
          y0 = (y1 + y2) / 2
          z0 = (z1 + z2) / 2
      	# 初值想平面1移动
          if plane1.A != 0:
              x3 = -plane1.D / plane1.A
              x0 = (x0 + x3) / 2
          elif plane1.B != 0:
              y3 = -plane1.D / plane1.B
              y0 = (y0 + y3) / 2
          elif plane1.C != 0:
              z3 = -plane1.D / plane1.C
              z0 = (z0 + z3) / 2
      	# 初值向平面2移动
          if plane2.A != 0:
              x3 = -plane2.D / plane2.A
              x0 = (x0 + x3) / 2
          elif plane2.B != 0:
              y3 = -plane2.D / plane2.B
              y0 = (y0 + y3) / 2
          elif plane2.C != 0:
              z3 = -plane2.D / plane2.C
              z0 = (z0 + z3) / 2

          r0 = min(plane1.dist_to_point(x0, y0, z0), plane2.dist_to_point(x0, y0, z0))
      	# 定义方程组
          def equations(p):
              x, y, z, r = p
              return (pow(x - x1, 2) + pow(y - y1, 2) + pow(z - z1, 2) - pow(r + r1, 2),
                      pow(x - x2, 2) + pow(y - y2, 2) + pow(z - z2, 2) - pow(r + r2, 2),
                      plane1.dist_to_point(x, y, z) - r,
                      plane2.dist_to_point(x, y, z) - r)
      	# 用 fsolve 解方程
          x, y, z, r = fsolve(equations, (x0, y0, z0, r0))
          return Sphere(x, y, z, r)

      # 三个球和一个平面围成的区域
      def three_sphere_one_plane(sphere1, sphere2, sphere3, plane):
          x1, y1, z1, r1 = sphere1.x, sphere1.y, sphere1.z, sphere1.r
          x2, y2, z2, r2 = sphere2.x, sphere2.y, sphere2.z, sphere2.r
          x3, y3, z3, r3 = sphere3.x, sphere3.y, sphere3.z, sphere3.r
      	# 迭代初始值
          x0 = (x1 + x2 + x3) / 3
          y0 = (y1 + y2 + y3) / 3
          z0 = (z1 + z2 + z3) / 3
          if plane.A != 0:
              x4 = -plane.D / plane.A
              x0 = (x0 + x4) / 2
          elif plane.B != 0:
              y4 = -plane.D / plane.B
              y0 = (y0 + y4) / 2
          elif plane.C != 0:
              z4 = -plane.D / plane.C
              z0 = (z0 + z4) / 2
      	
          r0 = plane.dist_to_point(x0, y0, z0)
      	# 定义方程组
          def equations(p):
              x, y, z, r = p
              return (pow(x - x1, 2) + pow(y - y1, 2) + pow(z - z1, 2) - pow(r + r1, 2),
                      pow(x - x2, 2) + pow(y - y2, 2) + pow(z - z2, 2) - pow(r + r2, 2),
                      pow(x - x3, 2) + pow(y - y3, 2) + pow(z - z3, 2) - pow(r + r3, 2),
                      plane.dist_to_point(x, y, z) - r)
      	# 用 fsolve 解方程
          x, y, z, r = fsolve(equations, (x0, y0, z0, r0))
          return Sphere(x, y, z, r)

      # 四个球围成的区域
      def four_sphere(sphere1, sphere2, sphere3, sphere4):
          sphere1, sphere2, sphere3, sphere4 = sorted([sphere1, sphere2, \
                                                       sphere3, sphere4])

          x1, y1, z1, r1 = sphere1.x, sphere1.y, sphere1.z, sphere1.r
          x2, y2, z2, r2 = sphere2.x, sphere2.y, sphere2.z, sphere2.r
          x3, y3, z3, r3 = sphere3.x, sphere3.y, sphere3.z, sphere3.r
          x4, y4, z4, r4 = sphere4.x, sphere4.y, sphere4.z, sphere4.r
      	# 迭代初始值
          x0 = (x1 + x2) / 2
          y0 = (y1 + y2) / 2
          z0 = (z1 + z2) / 2
          r0 = (r1 + r2) / 2
      	# 定义方程组
          def equations(p):
              x, y, z, r = p
              return (pow(x - x1, 2) + pow(y - y1, 2) + pow(z - z1, 2) - pow(r + r1, 2),
                      pow(x - x2, 2) + pow(y - y2, 2) + pow(z - z2, 2) - pow(r + r2, 2),
                      pow(x - x3, 2) + pow(y - y3, 2) + pow(z - z3, 2) - pow(r + r3, 2),
                      pow(x - x4, 2) + pow(y - y4, 2) + pow(z - z4, 2) - pow(r + r4, 2))
      	# 用 fsolve 解方程
          x, y, z, r = fsolve(equations, (x0, y0, z0, r0))
          return Sphere(x, y, z, r)
   ```

   ​

3. 对区域的抽象描述

   ```python
   class Area(object):
       def __init__(self, atype, planes, spheres):
           self.atype = atype
           self.planes = planes
           self.spheres = spheres
           self.in_sphere = None
   	
       # 区域的四种类型
       class Type(object):
           ONE_SPHERE_THREE_PLANE = 0
           TWO_SPHERE_TWO_PLANE = 1
           THREE_SPHERE_ONE_PLANE = 2
           FOUR_SPHERE = 3

       def inner_sphere(self):
           if self.in_sphere is None:
               if self.atype == Area.Type.ONE_SPHERE_THREE_PLANE:
                   self.in_sphere = one_sphere_three_plane(self.spheres[0],\ 									self.planes[0], self.planes[1], self.planes[2])
               elif self.atype == Area.Type.TWO_SPHERE_TWO_PLANE:
                   self.in_sphere = two_sphere_two_plane(self.spheres[0], \
                           self.spheres[1], self.planes[0], self.planes[1])
               elif self.atype == Area.Type.THREE_SPHERE_ONE_PLANE:
                   self.in_sphere = three_sphere_one_plane(self.spheres[0],\ 									self.spheres[1], self.spheres[2],self.planes[0])
               elif self.atype == Area.Type.FOUR_SPHERE:
                   self.in_sphere = four_sphere(self.spheres[0], self.spheres[1],\ 							self.spheres[2], self.spheres[3])
           return self.in_sphere
   ```



4. 贪心算法的实现

   ```python
   def compute(m, blocks):
       point1 = Point(1, 1, 1)
       point2 = Point(1, 1, -1)
       point3 = Point(1, -1, 1)
       point4 = Point(1, -1, -1)
       point5 = Point(-1, 1, 1)
       point6 = Point(-1, 1, -1)
       point7 = Point(-1, -1, 1)
       point8 = Point(-1, -1, -1)

       plane1 = Plane(point1, point2, point3)  # x = 1
       plane2 = Plane(point5, point6, point7)  # x = -1
       plane3 = Plane(point1, point2, point5)  # y = 1
       plane4 = Plane(point3, point4, point7)  # y = -1
       plane5 = Plane(point1, point3, point5)  # z = 1
       plane6 = Plane(point2, point4, point6)  # z = -1
   	# 初始化平面集
       planes = [plane1, plane2, plane3, plane4, plane5, plane6]

       block_filter(blocks, planes)

       spheres = [] + blocks

       while m > 0:
           max_sphere_area = None
           max_sphere = Sphere(0, 0, 0, 0)

           # 四个球围成的区域
           for four_sphere in itertools.combinations(spheres, 4):
               # 任取四个球组成一个新的区域
               area = Area(Area.Type.FOUR_SPHERE, [], four_sphere)
               # 计算区域的内球，取半径最大的那个
               if area.inner_sphere().r > max_sphere.r and \
               		check_area(area, spheres, planes):
                   max_sphere_area = area
                   max_sphere = area.inner_sphere()

           # 一个面，三个球
           for plane in planes:
               # 任取三个球
               three_spheres = itertools.combinations(spheres, 3)
               for three_sphere in three_spheres:
                   # 三个球和一个面组成一个新的区域
                   area = Area(Area.Type.THREE_SPHERE_ONE_PLANE, [plane, ], three_sphere)
                   # 计算区域的内球，取半径最大的那个
                   if area.inner_sphere().r > max_sphere.r and \
                   		check_area(area, spheres, planes):
                       max_sphere_area = area
                       max_sphere = area.inner_sphere()

           # 两个面，两个球
           # 任取两个面
           for two_plane in itertools.combinations(planes, 2):
               # 判断两个面相交
               if not two_plane[0].parallel_to(two_plane[1]):
                   # 任取两个球
                   two_spheres = itertools.combinations(spheres, 2)
                   for two_sphere in two_spheres:
                       # 两个球和两个面组成一个新的区域
                       area = Area(Area.Type.TWO_SPHERE_TWO_PLANE, two_plane, two_sphere)
                       # 计算区域的内球，取最大的那个
                       if area.inner_sphere().r > max_sphere.r and \
                       		check_area(area, spheres, planes):
                           max_sphere_area = area
                           max_sphere = area.inner_sphere()

           # 三个面，一个球
           # 任取三个面
           for three_plane in itertools.combinations(planes, 3):
               # 判断三个面两两相交
               if not three_plane[0].parallel_to(three_plane[1]) and \
                       not three_plane[1].parallel_to(three_plane[2]) and \
                       not three_plane[2].parallel_to(three_plane[0]):
                   # 任取一个球
                   for sphere in spheres:
                       # 三个面和一个球组成一个新区域
                       area = Area(Area.Type.ONE_SPHERE_THREE_PLANE, \
                                   three_plane, [sphere, ])
                       # 计算区域的内球，取最大的那个
                       if area.inner_sphere().r > max_sphere.r and \
                       		check_area(area, spheres, planes):
                           max_sphere_area = area
                           max_sphere = area.inner_sphere()

           if max_sphere_area is not None:
               # 找到了当前最大的球
               # 移除球面上的障碍，这些点已经不能看作半径为 0 的球了
               for c in max_sphere_area.spheres:
                   if c.r == 0:
                       spheres.remove(c)
               spheres.append(max_sphere)
               m -= 1

       # 移除所有障碍
       for c in spheres:
           if c.r == 0:
               spheres.remove(c)
       return spheres
   ```



## Experiment

运行方式

1. 在命令行中输入

   ```shell
   jupyter notebook
   ```

2. 在 notebook 的界面中，进入 proj3/ 目录

   ![Jupyter notebook](http://oih52y89x.bkt.clouddn.com/jupyter_1.png)

3. 点击 new -> Python 2

4. 在 cell 中输入

   ```shell
   %run -i main.py
   ```

   ![Jupyter notebook](http://oih52y89x.bkt.clouddn.com/jupyter_2.png)

5. 等待一段时间，可以看到结果如下

   ![Jupyter notebook](http://oih52y89x.bkt.clouddn.com/jupyter_3.png)



## Conclusion

从项目二到项目三的迁移过程比较简单，短时间内顺利完成，主要的变化是运算增加了一个维度，需要对已有代码做很多重构，包括增加字段，修改变量名，修改方程等。还有产生的新区域方面，比二维多了一种。已有的算法框架基本不做太多修改。

变化更大的地方就是数据可视化的方式，之前的二维图形可视化用的是很简单的海龟作图，三维图形可视化则需要用上复杂的图形库，为了简化这方面的代码，我选择了 VPython 这个可视化工具，这个工具编码简单，但是只能在 jupyter notebook 环境中运行，使用 WebGL 进行图形渲染。

## Appendix

```shell
commit 035cbd2146baacbc5950ab2c32df558e1b7a524b
Author: WqyJh <781345688@qq.com>
Date:   Sun Jun 18 12:15:09 2017 +0800

    Finished proj3

commit fe13795a99b4dcb18baf7d3331d7fe7f1d3c2b9f
Author: WqyJh <781345688@qq.com>
Date:   Sun Jun 18 11:44:14 2017 +0800

    Proj3 Passed

commit 8779646acdb6743159c8d45e800e226542d9488f
Author: WqyJh <781345688@qq.com>
Date:   Sun Jun 18 10:47:46 2017 +0800

    Finished 3d algorithm

commit b1f1ea25f6e11023ceb0be54381dbeaff6c958cf
Author: WqyJh <781345688@qq.com>
Date:   Sun Jun 18 00:45:24 2017 +0800

    Refact 2d code to 3d

```

