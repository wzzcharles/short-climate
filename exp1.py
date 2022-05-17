# 创建者：wzz
# 开发时间：2022/3/29 18:56

# 导入库
import numpy as np  # 数据处理用
import xarray as xr
import matplotlib.pyplot as plt  # 画图用
import cartopy.crs as ccrs  # 投影用
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
# from cartopy.io.shapereader import Reader
from matplotlib.ticker import MultipleLocator
from cartopy.util import add_cyclic_point


# 画布设置
def drawmap():
    canvas = ccrs.PlateCarree(central_longitude=180)  # 建了一个画布，中心纬度180
    fig = plt.figure(figsize=(9, 6))  # 设置画布大小
    pt = fig.subplots(1, 1, subplot_kw={'projection': canvas})  # 画图，画一张（必备步骤）
    pt.coastlines('110m')  # 海岸线
    pt.set_xticks(np.arange(-180, 181, 30), crs=ccrs.PlateCarree())  # 标注xy坐标轴
    pt.set_yticks(np.arange(-90, 91, 30), crs=ccrs.PlateCarree())

    # 设置坐标轴大小刻度,间隔内对基数的每个整数倍设置一个刻度
    majorticks = MultipleLocator(30)  # 主刻度30倍数
    minorticks = MultipleLocator(10)  # 副刻度10倍数
    # 设置主副刻度标签的位置,标签文本的格式
    pt.xaxis.set_major_locator(majorticks)  # x轴主刻度位置
    pt.xaxis.set_minor_locator(minorticks)  # x轴副刻度位置
    pt.yaxis.set_minor_locator(minorticks)
    lonformat = LongitudeFormatter(zero_direction_label=False)  # 坐标轴设置成经纬度格式，把0经度设置不加E和W
    latformat = LatitudeFormatter()
    pt.xaxis.set_major_formatter(lonformat)  # 经纬度格式确认
    pt.yaxis.set_major_formatter(latformat)
    return pt, fig


# 读取数据
origindata = xr.open_dataset(r'E:\Work\Python\short_climate\exp1\hgt.mon.mean.nc')['hgt']
# print(data)

# 找出经纬度
lat = origindata['lat']
lon = origindata['lon']
# lons, lats = np.meshgrid(lon, lat)  #从坐标向量返回坐标矩阵
# print(lons, lats)

# 使用数据提取，1980-2010,850hPa
userdata = origindata.loc[origindata.time.dt.month.isin([7])].loc["1980-01-01":'2010-12-01', 850, :, :]
# print(userdata)


# ----------------- 实习1-1 -------------------#
ave850 = userdata.mean(dim='time')  # 制作850hpa高度场平均值
# print(ave850)
# print(ave850.max(), ave850.min())  #找出最大和最小值

# 开始画图-图1
pt1, fig1 = drawmap()
useave850, uselon = add_cyclic_point(ave850, coord=lon)
contour = pt1.contour(uselon, lat, useave850, levels=np.arange(1000, 1620, 60),
                      colors='k', linewidths=1, transform=ccrs.PlateCarree())  # 画等值线
plt.clabel(contour, inline=True, fontsize=8, fmt='%.0f')  # 标注等值线图
pt1.set_title('Picture1:850 hPa avehgt', loc='center')  # 写个标题，居中
# plt.show()
plt.savefig(r'850hPa_1980-2010_avehgt.png')


# ----------------- 实习1-2 -------------------#
hgt_850_Jul_2010 = userdata.loc['2010-07-01']  # 读取数据：2010年7月,850hPa高度场原始数据
# print(hgt_Jul_850)

jp_hgt_850_JUl_2010 = hgt_850_Jul_2010 - ave850  # 计算距平
# print(jp_hgt_Jul_850)
# print(jp_hgt_Jul_850.max(), jp_hgt_Jul_850.min())   #找出最大最小值

# 开始画图
pt2, fig2 = drawmap()
use_jp, uselon = add_cyclic_point(jp_hgt_850_JUl_2010, coord=lon)
contour = pt2.contour(uselon, lat, use_jp, levels=np.arange(-140, 85, 20),
                      colors='k', linewidths=1, transform=ccrs.PlateCarree())  # 画等值线
plt.clabel(contour, inline=True, fontsize=8, fmt='%.0f')  # 标注等值线图
contour = pt2.contourf(uselon, lat, use_jp, cmap='coolwarm', levels=np.arange(-140, 85, 20),
                       transform=ccrs.PlateCarree())  # 画填色图
plt.colorbar(contour, shrink=0.5, orientation='horizontal')  # 设置色标，使色标横向
pt2.set_title('Picture2:850 hPa jp_hgt_2010_Jul_850', loc='center')  # 写个标题，居中
# plt.show()
plt.savefig(r'jp_hgt_2010_Jul_850.png')


# -----------------实习1-3-------------------#
ave_lat_hgt_850_Jul = hgt_850_Jul_2010.mean(dim='lat')  # 计算2010年7月850hPa高度场纬向平均
# print(ave_lat_hgt_850_Jul)

wp_hgt_850_Jul_2010 = hgt_850_Jul_2010 - ave_lat_hgt_850_Jul  # 计算距平值
# print(wp_hgt_850_Jul_2010)
# print(wp_hgt_850_Jul_2010.max(), wp_hgt_850_Jul_2010.min())     #找出最大最小值

# 开始画图
pt3, fig = drawmap()
use_wp, uselon = add_cyclic_point(wp_hgt_850_Jul_2010, coord=lon)
contour = pt3.contour(uselon, lat, use_wp, levels=np.arange(-500, 300, 50),
                      colors='k', linewidths=1, transform=ccrs.PlateCarree())  # h画等值线
plt.clabel(contour, inline=True, fontsize=8, fmt='%.0f')  # 标注等值线图
contour = pt3.contourf(uselon, lat, use_wp, cmap='coolwarm', levels=np.arange(-500, 300, 50),
                       transform=ccrs.PlateCarree())  # 画填色图
plt.colorbar(contour, shrink=0.5, orientation='horizontal')  # 设置色标，使色标横向
pt3.set_title('Picture3:850 hPa wp_hgt_2010_Jul_850', loc='center')  # 写个标题，居中
# plt.show()
plt.savefig(r'wp_hgt_2010_Jul_850.png')
