# 软件工程上机报告4

## Introduction

Update to a multi-process/thread/core implementation.In a box(3D) bounded by [-1, 1], given m balloons(they cannot overlap) with variable radio r and position mu. And some tiny blocks are in the box at given position {d};balloons cannot overlap with these blocks. find the optimal value of r and mu which maximizes 

## Algorithm

这个项目是在项目三的基础上增加多线程。

项目三主要的耗时运算在于贪心算法中的 while 循环，如下面代码所示，循环里的计算主要是四个大块，计算四个球围成的区域、计算一个面三个球围成的区域、计算两个面两个球围成的区域、计算三个面一个球围成的区域。这几个计算相互独立，并行执行。他们都需要用到 spheres 和 planes 两个参数，即当前的球集和面集，并且他们只是读取其中的值，并不写入。这样的结构非常适合使用多线程。

```python
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
```

由于 Python 语言的解释器是单进程运行的，而且由于全局解释器锁（GIL)的存在，在任意时刻 Python 解释器只能为一个线程工作，因此 Python 的线程库并不能实现真正的并行、多核计算，强行使用多进程会增加进程切换的开销，而且并不会提高性能。

另外，本项目所依赖的用于解方程的库`scipy.optimize`并不是线程安全的，在多线程计算的时候，有很大几率导致进程崩溃（亲测，在球的个数比大于15的时候，几乎都会崩溃），解决方案是在每一次调用`fsolve`之前获得一个全局的互斥锁，这样一来又大大降低了运算性能。

因此本项目采用 Python 的多进程模块来实现并行计算。具体而言是，

1. 分配一个大小为4的进程池
2. 将4个计算任务抽成4个函数，每个函数返回各自区域中的最大值
3. 将这4个函数应用到进程池里，然后主进程等待进程池运行结束
4. 主进程得到4个函数的返回值，比较得出最大值
5. 重复步骤3~4，直到找到 m 个球



### 算法实现

环境 

- Python 2.7.13
- Jupyter notebook 4.3.0

依赖 

- scipy.optmize，用于解方程
- itertools，用于排列组合
- ivisual，用于绘制三维图像
- multiprocessing，用于管理进程



1. 四个进程的工作函数，他们都接受两个参数 spheres 和 planes，返回各自类型区域中的最大值

   ```python
   def compute_four_sphere(spheres, planes):
       max_sphere_area = None
       max_sphere = Sphere(0, 0, 0, 0)
       for four_sphere in itertools.combinations(spheres, 4):
           area = Area(Area.Type.FOUR_SPHERE, [], four_sphere)
           if area.inner_sphere().r > max_sphere.r and 、
           		check_area(area, spheres, planes):
               max_sphere_area = area
               max_sphere = area.inner_sphere()
       return (max_sphere_area, max_sphere)

   def compute_three_sphere_one_plane(spheres, planes):
   	max_sphere_area = None
      	max_sphere = Sphere(0, 0, 0, 0)
      	for plane in planes:
          	three_spheres = itertools.combinations(spheres, 3)
          	for three_sphere in three_spheres:
              	area = Area(Area.Type.THREE_SPHERE_ONE_PLANE, [plane, ], three_sphere)
              	if area.inner_sphere().r > max_sphere.r and \
              			check_area(area, spheres, planes):
                  	max_sphere_area = area
                  	max_sphere = area.inner_sphere()
      	return (max_sphere_area, max_sphere)

   def compute_two_sphere_two_plane(spheres, planes):
   	max_sphere_area = None
      	max_sphere = Sphere(0, 0, 0, 0)
      	for two_plane in itertools.combinations(planes, 2):
       	if not two_plane[0].parallel_to(two_plane[1]):
              	two_spheres = itertools.combinations(spheres, 2)
              	for two_sphere in two_spheres:
                  	area = Area(Area.Type.TWO_SPHERE_TWO_PLANE, two_plane, two_sphere)
                  	if area.inner_sphere().r > max_sphere.r and \
                  			check_area(area, spheres, planes):
                      	max_sphere_area = area
                      	max_sphere = area.inner_sphere()
      	return (max_sphere_area, max_sphere) 

   def compute_one_sphere_three_plane(spheres, planes):
      	max_sphere_area = None
      	max_sphere = Sphere(0, 0, 0, 0)
      	for three_plane in itertools.combinations(planes, 3):
          	if not three_plane[0].parallel_to(three_plane[1]) and \
                  	not three_plane[1].parallel_to(three_plane[2]) and \
                  	not three_plane[2].parallel_to(three_plane[0]):
              	for sphere in spheres:
                  	area = Area(Area.Type.ONE_SPHERE_THREE_PLANE, three_plane, [sphere, ])
                  	if area.inner_sphere().r > max_sphere.r and \
                  			check_area(area, spheres, planes):
                      	max_sphere_area = area
                      	max_sphere = area.inner_sphere()
      	return (max_sphere_area, max_sphere)
   ```

2. 主线程逻辑函数


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

          planes = [plane1, plane2, plane3, plane4, plane5, plane6]

          block_filter(blocks, planes)

          spheres = [] + blocks
          output = []
      	# 创建线程池
          pool = multiprocessing.Pool(4)

          while m > 0:
              max_sphere_area = None
              max_sphere = Sphere(0, 0, 0, 0)
      		
              output.clear()
      		# 向进程池中指派计算任务，并获取异步返回值
              output.append(pool.apply_async(compute_four_sphere, (spheres, planes)))
              output.append(pool.apply_async(compute_three_sphere_one_plane, \
                                             (spheres, planes)))
              output.append(pool.apply_async(compute_two_sphere_two_plane, \
                                             (spheres, planes)))
              output.append(pool.apply_async(compute_one_sphere_three_plane, \
                                             (spheres, planes)))

              for opt in output:
                  # get 方法用于获取任务的返回值，它会阻塞这段代码
                  (m_c_a, m_c) = opt.get()
                  # 比较得到最大的球
                  if m_c.r > max_sphere.r:
                      max_sphere_area = m_c_a
                      max_sphere = m_c

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

   ​

   ​



## Experiment

执行 main.py，打开任务管理器，看到有四个工作进程在运行，一个主线程处于阻塞状态。

![process](http://oih52y89x.bkt.clouddn.com/p4_process.png)

结果输出：

![output](http://oih52y89x.bkt.clouddn.com/p4_output.png)

## Conclusion

在加入了多线程/多进程运算后，运算速度并没有显著提高，原因是多线程过程中的安全问题导致产生不断上锁开锁的开销，而多进程运算又存在进程间通信，传递参数的开销。

## Appendix

```shell
commit cc1cf1eb3880104a3a70c1235c3edea7b8b0abaf
Author: WqyJh <781345688@qq.com>
Date:   Tue Jun 20 16:47:36 2017 +0800

    Finished proj4

commit e1448406c90ce8a3584d373594d3074e0c2c1769
Author: WqyJh <781345688@qq.com>
Date:   Tue Jun 20 16:05:10 2017 +0800

    Combine user_interface with main

commit 18899a649d189c1ab271e017f5b38ad3e308bf2d
Author: WqyJh <781345688@qq.com>
Date:   Tue Jun 20 15:54:28 2017 +0800

    Add user_interface

commit 35b2c394bb63d26f3c7ddf7efb4c8398147c8efc
Author: WqyJh <781345688@qq.com>
Date:   Tue Jun 20 15:18:38 2017 +0800

    Replace multi-thread with multi-process

commit cd70f2af9d52370b8d6a27531147f2707d59c00e
Author: WqyJh <781345688@qq.com>
Date:   Tue Jun 20 15:05:58 2017 +0800

    Test process pool

commit 9db70ec791496eef2fd985f079f29b44b6b7e54c
Author: WqyJh <781345688@qq.com>
Date:   Tue Jun 20 14:30:48 2017 +0800

    Remove useless code in proj3

commit 71006bdad16ca6b80d5eff05c1c7d00d1f749416
Author: WqyJh <781345688@qq.com>
Date:   Tue Jun 20 12:55:43 2017 +0800

    Remove useless code in proj3
commit 9f1a26f7c4b45c08258c3e26bf600998edead49d
Author: WqyJh <781345688@qq.com>
Date:   Tue Jun 20 01:35:17 2017 +0800

    Add README.md for proj1

commit b767beddc4a8e855d618aa65e8f518a5ed650838
Author: WqyJh <781345688@qq.com>
Date:   Mon Jun 19 22:59:27 2017 +0800

    fix drawer.py in proj3

commit 8b231e2bb33a353b24944b986524b20d65842b80
Author: WqyJh <781345688@qq.com>
Date:   Mon Jun 19 22:27:31 2017 +0800

    Refactor: fix drawer.py in proj4

commit 9fa869424f1900650e3d17811788de77afeabb17
Author: WqyJh <781345688@qq.com>
Date:   Mon Jun 19 21:58:55 2017 +0800

    Refact proj3: divide compute and draw

commit 98bec605c50d187b41cbe6aacb89fc72c3351bc3
Author: WqyJh <781345688@qq.com>
Date:   Mon Jun 19 21:38:55 2017 +0800

    Rename Circle to Sphere

commit bce55cc93b19bfd53893745ff404397956b013cb
Author: WqyJh <781345688@qq.com>
Date:   Mon Jun 19 21:24:21 2017 +0800

    Rearrange code

commit 1617748d7b5dd582a4e7c819341da821c156a659
Author: WqyJh <781345688@qq.com>
Date:   Mon Jun 19 21:21:00 2017 +0800

    Fix scipy thread-safe problem
commit 44cf0d61be9e016716dbc936b231a1f9f5632726
Author: WqyJh <781345688@qq.com>
Date:   Mon Jun 19 12:18:49 2017 +0000

    Add multi thread

commit 40c7e6ac28412da55d7e767eb0c92aff440d3538
Author: WqyJh <781345688@qq.com>
Date:   Mon Jun 19 12:10:00 2017 +0000

    Migrate to python3

commit a71b34015656c82f13d048ee587ff88ee44d2814
Author: WqyJh <781345688@qq.com>
Date:   Sun Jun 18 15:24:17 2017 +0000

    Add proj4

```

