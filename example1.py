import numpy as np                 #用于计算
import matplotlib.pyplot as plt    #数据可视化
import xarray as xr                #数据读取
import cartopy.crs as ccrs         #地图投影
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.util import add_cyclic_point




def GetVar(file_name,DatasetName):
    rVar=[]                                   #创建列表
    with open(file_name) as file:             #打开文件
        file = xr.open_dataset(file_name)     #获取文件中的变量
        for x in DatasetName:           
            a = file[x]
            rVar.append(a)                   #单个变量加入列表
    rVar=np.array(rVar)                      #把列表转化为数组
    return rVar

def Plot_Shaded(r,lat,lon,title):
    fig  = plt.figure()
    ax1  = fig.add_subplot(111)
    cmap = plt.get_cmap('bwr')  #选择coloarmap

    # #画第一个子图
    # Label axes of a Plate Carree projection with a central longitude of 180:
    ax1 = plt.subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
    ax1.set_global() #使得轴域（Axes即两条坐标轴围城的区域）适应地图的大小
    ax1.coastlines() #画出海岸线
    
    #填充白条
    #hgt_an,lon= add_cyclic_point(hgt_an, coord=lon)
    #lon, lat = np.meshgrid(lon, lat) #生成网格点

    ax1.set_xticks([0, 60, 120, 180, 240, 300, 360], crs=ccrs.PlateCarree())
    ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
    #zero_direction_label用来设置经度的0度加不加E和W
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax1.xaxis.set_major_formatter(lon_formatter)
    ax1.yaxis.set_major_formatter(lat_formatter)
    plt.contourf(lon,lat,r,cmap=cmap,levels=np.arange(4950,6000,100),transform=ccrs.PlateCarree())
    plt.colorbar(shrink=1,orientation = 'horizontal')#(使色条横向)
    ax1.set_title(title,fontsize = 16)


if __name__ == '__main__':
    
     file = '/Users/huangni/Documents/TeachingAssistant/hgt.mon.mean.nc'  #读取数据
     DataSet=['hgt','lat','lon','level']    
     hgt,lat,lon,level = GetVar((file),DataSet)
     
     Jan_500_mean = np.mean(hgt[(32*12):(62*12)+1:12,5,:,:],axis=0)      #1980年1月500hPa平均
     hgt_an= hgt[62*12,5,:,:]-Jan_500_mean                             #1980年1月500hPa距平
    
     #Plot_Shaded(Jan_500_mean,lat,lon,'500hPa hgt Jan Mean')           #绘制等值线图
     #Plot_Shaded(hgt_an,lat,lon,'500hPa hgt Jan Anomaly')              #绘制填色图
     # (DataSet,Plot_Shaded为写好的函数，以后根据情况调用即可)
     
     
     title_mean = '500hPa hgt Jan Mean'
     title_an   = '500hPa hgt Jan Anomaly'

    # #画第一个子图
    # Label axes of a Plate Carree projection with a central longitude of 180:
     ax1 = plt.subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
     ax1.set_global() #使得轴域（Axes即两条坐标轴围城的区域）适应地图的大小
     ax1.coastlines() #画出海岸线
     cmap   = plt.get_cmap('bwr')  #选择色标
    #填充白条
    #hgt_an,lon= add_cyclic_point(hgt_an, coord=lon)
    #lon, lat = np.meshgrid(lon, lat) #生成网格点

     ax1.set_xticks([0, 60, 120, 180, 240, 300, 360], crs=ccrs.PlateCarree())#设置x轴坐标
     ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())  #设置y轴坐标
     #zero_direction_label用来设置经度的0度加不加E和W
     lon_formatter = LongitudeFormatter(zero_direction_label=False) #x轴设为经度格式
     lat_formatter = LatitudeFormatter()                            #y轴设为纬度格式
     ax1.xaxis.set_major_formatter(lon_formatter)
     ax1.yaxis.set_major_formatter(lat_formatter)
     
     ''
     ax1.set_title(title_mean,fontsize = 16) #设置标题
     cs = plt.contour(lon,lat,Jan_500_mean,colors='k',transform=ccrs.PlateCarree()) #绘制填色图。颜色设置为黑色
     plt.clabel(cs,fmt = '%1.0f')  #添加等值线标签，不保留小数
     #plt.colorbar(shrink=1,orientation = 'horizontal')#设置色标，使色标横向
     #plt.show() #展示图片
     plt.savefig('/Users/huangni/Documents/TeachingAssistant/Jan_500_mean.png') #保存图片
     '''
     plt.contourf(lon,lat,hgt_an,cmap=cmap,levels=np.arange(-150,200,50),transform=ccrs.PlateCarree()) #绘制填色图
     plt.colorbar(shrink=1,orientation = 'horizontal')#设置色标，使色标横向
     ax1.set_title(title_an,fontsize = 16) #设置标题
     plt.savefig('/Users/huangni/Documents/TeachingAssistant/Jan_500_an.png') #保存图片
     '''
     