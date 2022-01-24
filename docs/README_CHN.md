![astro_scheduller](./astro_scheduller.jpg)

# AstroSchedullerGo 0.9.3

[![](https://img.shields.io/badge/许可-MIT-green)](https://github.com/xiawenke/AstroSchedullerGo/blob/Dev/LICENSE)
[![](https://img.shields.io/badge/当前版本-v0.9.3-informational)](https://github.com/xiawenke/AstroSchedullerGo/releases)
[![](https://img.shields.io/badge/switch language into-English-orange)](https://github.com/xiawenke/AstroSchedullerGo#readme)

AstroScheduller项目尝试设计一种用于生成天文观测纲要的算法，此项目主要用GoLang代码设计。AstroSchedullerGo前身为[AstroScheduller.py](https://github.com/xiawenke/AstroSchedulle)。

## 快速开始

#### 观测参数

AstroScheduller程序的输入是以XML方式编写的观察参数，以下是一个带有注释的例子。

```xml
<scheduller>
    <observation>
        <duration>
            <begin>1627113420</begin> <!-- 观察开始时的时间戳 -->
            <end>1628113420</end> <!-- 观察结束时的时间戳 -->
        </duration>

        <telescope>
            <latitude>32.701500</latitude> <!-- 望远镜在地球上的纬度 -->
            <longitude>-109.891284</longitude> <!-- 望远镜在地球上的经度 -->
            <altitude>3185</altitude> <!-- 望远镜在地球上的海拔 -->
            <velocity>
                <ra>0.5</ra> <!-- 望远镜在R.A.方向的旋转速度 -->
                <dec>0.6</dec> <!-- 望远镜在Dec.方向的旋转速度 -->
            </velocity>
        </telescope>

        <elevation>
            <minimal>30</minimal> <!-- 望远镜能够运行的最低角度 -->
            <maximal>80</maximal> <!-- 望远镜能够运行的最高角度 -->
        </elevation>

        <escape>
            <sun>20</sun> <!-- 望远镜能够运行的与太阳的最小夹角 -->
        </escape>
    </observation>

    <sources>
        <object> <!-- 第一个观测源 -->
            <identifier>PSR J1012+5307</identifier> <!-- 观测源的源名 -->
            <ra>153.13930897</ra> <!-- 观测源的R.A.坐标（单位为角度） -->
            <dec>53.11737904</dec> <!-- 观测源的Dec.坐标（单位为角度） -->
            <duration>800</duration> <!-- 观测时长（单位：秒） -->
        </object>

        <object> <!-- 第二个观测源 -->
            <identifier>PSR B0320+39</identifier> <!-- 观测源的源名 -->
            <ra>50.86090833</ra> <!-- 观测源的R.A.坐标（单位为角度） -->
            <dec>39.74802778</dec> <!-- 观测源的Dec.坐标（单位为角度） -->
            <duration>2400</duration> <!-- 观测时长（单位：秒） -->
            <weight>0.1</weight> <!-- 观测源的权重。为0到1之间的浮点数，更大意味着权重更高。 -->
			<important>1</important> <!-- 标记为“重要”。观测源将会有极高的权重，若important标签被标记为“1”。 -->
        </object>
      
      	... <!-- 在此之后可以添加更的观测源 -->
      
    </sources>
</scheduller>
```

如果你已经有了项目[AstroScheduller.py](https://github.com/xiawenke/AstroScheduller)的 "源表"，该列表可以通过[PyInterface.py](https://github.com/xiawenke/AstroSchedullerGo/blob/Dev/PyInterface.py)转换为XML格式的观测参数。

### 生成观测纲要

1. 在准备好观测参数后，从[Releases](https://github.com/xiawenke/AstroSchedullerGo/releases)下载最新预编译的AstroSchedullerGo程序（或从源代码编译）。

2. 打开一个新的命令行工具并切换到当前目录。

   ```bash
   cd /path/to/AstroSchedullerGo_v0_9_3_dev
   ```

3. 通过`./AstroScheduller_vx_x_dev [PATH TO OBSERVATION PARAMETER.xml] [PATH TO EXPORT.xml]`指令运行程序。

   ```bash
   ./AstroSchedullerGo_v0_9_3_dev psr_list_debug.xml psr_list_debug_export.xml
   ```

4. 计划表成功生成后，程序将提示 `The schedule has been successfully generated`。

### PyInterface.py 脚本

[PyInterface.py](https://github.com/xiawenke/AstroSchedullerGo/blob/Dev/PyInterface.py)是一个带有 "scheduller() "类的Python脚本，可以用来更高效和方便地运行程序。要使用这个脚本，请从[release](https://github.com/xiawenke/AstroSchedullerGo/releases)获得一个最新的预编译的AstroSchedullerGo程序，并将其保存在与脚本相同的目录中。

在许多类被声明后，脚本的末尾，可以使用以下命令：

1. 新启一个新的scheduller类的Handle：

   ```
   schedullerHandle = scheduller()
   ```

2. 从XML格式的观测参数中导入数据：

   ```python
   schedullerHandle.load_from_xml("./tests/psr_list_debug.xml")
   ```

   或者 [AstroScheduller.py](https://github.com/xiawenke/AstroScheduller) 项目中的“源表”可以被转换为新的格式并导入：

   ```python
   schedullerHandle.load_from_json("./tests/psr_list_debug.json")
   ```

3. 生成观测纲要：

   ```
   schedullerHandle.schedule()
   ```

   如果同一目录下多个Core（也就是编译后的AstroSchedullerGo程序），脚本将会询问使用哪一个Core。

4. 将生成的观测纲要绘制为图片预览：

   ```python
   schedullerHandle.plot()
   ```

5. 保存观测纲要：

   ```python
   schedullerHandle.save("./tests/psr_list_debug_schedule.xml")
   ```

   

在[PyInterface.py](https://github.com/xiawenke/AstroSchedullerGo/blob/Dev/PyInterface.py)的末尾有一个实例供参考。

## 许可

AstroSchedullerGo是在MIT许可下作为一个开放源码项目发布的。更多信息见[LICENSE](https://github.com/xiawenke/AstroSchedullerGo/blob/Dev/LICENSE)。

## 鸣谢

我们由衷地感谢中国科学院上海天文台的研究人员和学生，感谢他们的想法以及意味深远的讨论；感谢他们帮助进行算法可靠性的测试。

