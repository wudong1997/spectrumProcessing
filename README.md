# 水色遥感--水下profile测量

在测量Water-leaving reflectance的各类方法中，水下profile测量可以避免水面反射光的影响，测得较为稳定的数值  
在近一段时间的研究中，我对水下profile的测量结果数据进行了处理，并通过python进行快速计算  
本文主要对水下profile的测量方法进行简要叙述，同时记录水下profile的数据处理过程及结果分析  

## 水下profile测量
水下profile测量所使用的仪器为RAMSES-ARC （德国TriOS GmbH）  
在测量过程中，将TriOS逐渐向下沉入至湖底  
在此过程中
#### 注意：  
1. 深度分辨率（Depth resolution）：仪器采样度应为每米至少测量两个值，最好测量六到八个值。（NASA）
2. 避免船只阴影影响与水文扰动影响：建议从船尾进行测量（NASA）  
    NASA所给的数据中显示，需要将仪器置于距离船体1.5K~3K的位置
4. ？通过对![1](https://latex.codecogs.com/svg.image?E_{d}\left&spacej;(&space;0^{&plus;}&space;\right&space;))的测量计算![2](https://latex.codecogs.com/svg.image?E_{d}\left&space;(&space;0^{-}&space;\right&space;))对水下测量进行校正（NASA)
5. 仪器的姿态数据（实际无记录）

#### 记录数据：
1. 时间日期
2. 地理位置（经纬度）
3. 传感器与船舶之间的距离，以及相对于船舶航向的方向
4. Secchi Disk Depth；
5. 云量和天空情况
6. 风速和风向（可以通过后期官方观测记录获取）
7. 大气压力
8. 水样信息

#### 测量结果：
<div align=center><img src="https://github.com/wudong1997/myresearch/blob/main/underwaterprofile.png"></div>
<div align=center>霞ヶ浦某点水下0~3m不同深度的光谱</div>

## K-Analysis
根据NASA水下测量方法，深度z与![2](https://latex.codecogs.com/svg.image?lnE_{d}\left&space;(&space;z&space;\right&space;))存在一次线性关系  
其斜率K即为水下散射衰减系数（Diffuse Attenuation Coefficient）
即  
<div align=center><img src="https://latex.codecogs.com/svg.image?K\left&space;(&space;z&space;\right&space;)=-\frac{dlnE_{d}\left&space;(&space;z&space;\right&space;)}{dz}" title="K\left ( z \right )=-\frac{dlnE_{d}\left ( z \right )}{dz}" /></div>

利用该公式在Python中进行实现  
```
    model = linear_model.LinearRegression()
    model.fit(self.x.reshape(-1, 1), self.y.reshape(-1, 1))
    b = model.intercept_[0]
    k = model.coef_[0]
```
<div align=center><img src="https://github.com/wudong1997/myresearch/blob/pic/%E5%9B%9E%E5%BD%92.png"></div>
<div align=center>560nm波段处深度z与<img src="https://latex.codecogs.com/svg.image?dlnE_{d}\left&space;(&space;z&space;\right&space;)" title="dlnE_{d}\left ( z \right )" />的线性关系</div>
<div>通过最小二乘法可以求的一次函数的斜率<img src="https://latex.codecogs.com/svg.image?K_{d}" title="K_{d}" />、截距b以及相关系数</div>
  
<div>将该方法应用于所有波段可以得到连续的<img src="https://latex.codecogs.com/svg.image?K_{d}" title="K_{d}" /></div>
<div align=center><img src="https://github.com/wudong1997/myresearch/blob/pic/diffuse atten co.png"></div>

## ![2](https://latex.codecogs.com/svg.image?E_{d}\left&space;(&space;0^{-}&space;\right&space;))与![3](https://latex.codecogs.com/svg.image?L_{u}\left&space;(&space;0^{-}&space;\right&space;))计算
根据数学公式，可以推出![2](https://latex.codecogs.com/svg.image?E_{d}\left&space;(&space;0^{-}&space;\right&space;))的值与上述方程的截距b存在以下关系：
<div align=center><img src="https://latex.codecogs.com/svg.image?E_{d}\left&space;(&space;0^{-}&space;\right&space;)=e^{b}" title="E_{d}\left ( 0^{-} \right )=e^{b}" /></div>
<div align=center><img src="https://github.com/wudong1997/myresearch/blob/pic/ed0.png"></div>
同理：
<div align=center><img src="https://latex.codecogs.com/svg.image?L_{u}\left&space;(&space;0^{-}&space;\right&space;)=e^{b}" title="L_{u}\left ( 0^{-} \right )=e^{b}" /></div>
<div align=center><img src="https://github.com/wudong1997/myresearch/blob/pic/lu0.png"></div>

## ![4](https://latex.codecogs.com/svg.image?R_{rs}\left&space;(&space;0^{&plus;}&space;\right&space;))计算
