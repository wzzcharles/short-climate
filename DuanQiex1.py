#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# # 数据来源：NCEP/NCAR 月平均的位势高度场
# # 实习要求
# (1)计算1980-2010年（30年）7月850 hPa 的平均高度场，绘制环流平均图；
# (2)计算2010年7月850 hPa 的高度距平，绘制高度距平场图（相对于1980-2010年共30年的平均)；
# (3)计算2010年7月850 hPa 的高度场纬偏值，绘制环流纬偏图。

# 

# In[1]:


# 导入需要用到的库
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.ticker import MultipleLocator


# In[2]:


# 创建地图函数
def createmap():
    proj = ccrs.PlateCarree(central_longitude=180)
    fig = plt.figure(figsize=(9, 6))
    ax = fig.subplots(1, 1, subplot_kw={'projection': proj})
    # 海岸线
    ax.coastlines('110m')
    # 标注坐标轴
    ax.set_xticks(np.arange(-180, 181, 30), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(-90, 91, 30), crs=ccrs.PlateCarree())
    # 设置大小刻度
    minorticks = MultipleLocator(10)
    majorticks = MultipleLocator(30)
    ax.xaxis.set_major_locator(majorticks)
    ax.xaxis.set_minor_locator(minorticks)
    ax.yaxis.set_minor_locator(minorticks)
    # 经纬度格式，把0经度设置不加E和W
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    return ax, fig


# In[3]:


ds = xr.open_dataset('D:\WORKcode\DuanQiQiHou\data\hgt.mon.mean.nc')['hgt']
ds


# In[4]:


lat = ds['lat']
lon = ds['lon']
lons, lats = np.meshgrid(lon, lat)


# In[5]:


ds1 = ds.loc[ds.time.dt.month.isin([7])].loc["1980-01-01":'2010-12-01', 850, :, :]


# In[6]:


ds1


# In[7]:


avehgt850 = ds1.mean(dim='time')
avehgt850


# 

# In[8]:


print(avehgt850.max(),avehgt850.min())


# In[9]:


ax,fig = createmap()
denglines = ax.contour(lons, lats, avehgt850, levels=np.arange(1000, 1620, 60), colors='blue',linewidths=1)
plt.clabel(denglines, inline=True, fontsize=8, fmt='%.0f')
ax.set_title('QU1:850hPaavehgt',loc='left')
plt.savefig('D:\\WORKcode\\DuanQiQiHou\\data\\1.png')


# In[10]:


hgt850_7=ds1.loc['2010-07-01']
hgt850_7


# In[11]:


juping_hgt850_7=hgt850_7-avehgt850
juping_hgt850_7


# In[12]:


print(juping_hgt850_7.max(),juping_hgt850_7.min())


# In[13]:


ax,fig = createmap()
denglines = ax.contour(lons, lats, juping_hgt850_7, levels=np.arange(-140, 82, 20), colors='blue',linewidths=1)
plt.clabel(denglines, inline=True, fontsize=8, fmt='%.0f')
ax.set_title('QU2:850hPahgtjuping-2010',loc='left')
plt.savefig('D:\\WORKcode\\DuanQiQiHou\\data\\2.png')


# In[14]:


avehgt850_lat=hgt850_7.mean(dim='lat')
avehgt850_lat


# In[15]:


weipianzhi=hgt850_7-avehgt850_lat
weipianzhi


# In[16]:


print(weipianzhi.max(),weipianzhi.min())


# In[17]:


ax,fig = createmap()
denglines = ax.contour(lons, lats, weipianzhi, levels=np.arange(-500, 230, 50), colors='blue',linewidths=1)
plt.clabel(denglines, inline=True, fontsize=8, fmt='%.0f')
ax.set_title('QU3:850hPahgtweipian-2010',loc='left')
plt.savefig('D:\\WORKcode\\DuanQiQiHou\\data\\3.png')

