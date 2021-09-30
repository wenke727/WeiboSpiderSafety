import geopandas as gpd
import matplotlib.pyplot as plt

# 设置matplotlib绘图模式为嵌入式
plt.rcParams["font.family"] = "SimHei" # 设置全局中文字体为黑体

# 读入中国领土面数据
china = gpd.read_file('zip://../data/china-shapefiles.zip!china-shapefiles/china.shp',
                     encoding='utf-8')
# 由于每行数据是单独的面，因此按照其省份列OWNER融合
china = china.dissolve(by='OWNER').reset_index(drop=False)

# 读入南海九段线线数据
nine_lines = gpd.read_file('zip://../data/china-shapefiles.zip!china-shapefiles/china_nine_dotted_line.shp',
                          encoding='utf-8')

china = china.merge(df_num, left_on="OWNER", right_index=True, how='left')

# china.loc[4, 'num'] = 0
# %%
#! 绘图

# 初始化图床
fig, ax = plt.subplots(figsize=(12, 8))
ax = china.geometry.plot(ax=ax)
ax = nine_lines.geometry.plot(ax=ax)
fig.savefig('图1.png', dpi=300)


# %%
# 定义CRS
albers_proj = '+proj=aea +lat_1=25 +lat_2=47 +lon_0=105'

fig, ax = plt.subplots(figsize=(12, 8))
ax = china.geometry.to_crs(albers_proj).plot(ax=ax)
ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax)
fig.savefig('图3.png', dpi=300)

# %%
fig, ax = plt.subplots(figsize=(12, 8))
ax = china.geometry.to_crs(albers_proj).plot(ax=ax,
                                             facecolor='grey',
                                             edgecolor='white',
                                             alpha=0.8)
ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  alpha=0.4)
ax.axis('off') # 移除坐标轴
fig.savefig('图4.png', dpi=300)

# %%
fig, ax = plt.subplots(figsize=(12, 8))
ax = china.geometry.to_crs(albers_proj).plot(ax=ax,
                                             facecolor='grey',
                                             edgecolor='white',
                                             linestyle='--',
                                             alpha=0.8)
ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4)
ax.axis('off') # 移除坐标轴
fig.savefig('图6.png', dpi=300)
# %%
fig, ax = plt.subplots(figsize=(12, 8))
ax = china.geometry.to_crs(albers_proj).plot(ax=ax,
                                             facecolor='grey',
                                             edgecolor='white',
                                             linestyle='--',
                                             hatch='x**',
                                             alpha=0.8)
ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4)
ax.axis('off') # 移除坐标轴
fig.savefig('图10.png', dpi=300)

# %%
fig, ax = plt.subplots(figsize=(12, 8))
ax = china.geometry.to_crs(albers_proj).plot(ax=ax,
                                             facecolor='grey',
                                             edgecolor='white',
                                             linestyle='--',
                                             hatch='xxxx',
                                             alpha=0.8)
ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4)
ax = china.geometry.centroid.to_crs(albers_proj).plot(ax=ax,
                                                      facecolor='black')
ax.axis('off') # 移除坐标轴
fig.savefig('图11.png', dpi=300)

# %%
fig, ax = plt.subplots(figsize=(12, 8))
ax = china.geometry.to_crs(albers_proj).plot(ax=ax,
                                             facecolor='grey',
                                             edgecolor='white',
                                             linestyle='--',
                                             hatch='xxxx',
                                             alpha=0.8)
ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4)
ax = china.geometry.representative_point() \
                   .to_crs(albers_proj) \
                   .plot(ax=ax, 
                         facecolor='black')
ax.axis('off') # 移除坐标轴
fig.savefig('图12.png', dpi=300)

# %%
fig, ax = plt.subplots(figsize=(12, 8))
ax = china.geometry.to_crs(albers_proj).plot(ax=ax,
                                             facecolor='grey',
                                             edgecolor='white',
                                             linestyle='--',
                                             hatch='xxxx',
                                             alpha=0.8)
ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4)
ax = china.geometry.representative_point() \
                   .to_crs(albers_proj) \
                   .plot(ax=ax, 
                         facecolor='white',
                         edgecolor='black',
                         marker='*',
                         markersize=200,
                         linewidth=0.5)
ax.axis('off') # 移除坐标轴
fig.savefig('图14.png', dpi=300)

# %%

fig, ax = plt.subplots(figsize=(12, 8))
ax = china.geometry.to_crs(albers_proj).plot(ax=ax,
                                             facecolor='grey',
                                             edgecolor='white',
                                             linestyle='--',
                                             alpha=0.8)
ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4,
                                                  label='南海九段线')
ax = china.geometry.representative_point() \
                   .to_crs(albers_proj) \
                   .plot(ax=ax, 
                         facecolor='white',
                         edgecolor='black',
                         marker='*',
                         markersize=100,
                         linewidth=0.5,
                         label='省级单位')
# 单独提前设置图例标题大小
plt.rcParams['legend.title_fontsize'] = 14

# 设置图例标题，位置，排列方式，是否带有阴影
ax.legend(title="图例", loc='lower left', ncol=1, shadow=True)

ax.axis('off') # 移除坐标轴
fig.savefig('图15.png', dpi=300)


# %%
fig, ax = plt.subplots(figsize=(12, 8))
ax = china.geometry.to_crs(albers_proj).plot(ax=ax,
                                             facecolor='grey',
                                             edgecolor='white',
                                             linestyle='--',
                                             alpha=0.8)
ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4,
                                                  label='南海九段线')

# 根据转换过投影的代表点，循环添加文字至地图上对应位置
for idx, _ in enumerate(china.geometry.representative_point().to_crs(albers_proj)):
    # 提取省级单位简称
    if ('自' in china.loc[idx, 'OWNER'] or '特' in china.loc[idx, 'OWNER']) \
    and china.loc[idx, 'OWNER'] != '内蒙古自治区':
        region = china.loc[idx, 'OWNER'][:2]
    else:
        region = china.loc[idx, 'OWNER'].replace('省', '') \
                                        .replace('市', '') \
                                        .replace('自治区', '')

    ax.text(_.x, _.y, region, ha="center", va="center", size=6)

# 单独提前设置图例标题大小
plt.rcParams['legend.title_fontsize'] = 14

# 设置图例标题，位置，排列方式，是否带有阴影
ax.legend(title="图例", loc='lower left', ncol=1, shadow=True)

ax.axis('off') # 移除坐标轴
fig.savefig('图16.png', dpi=300)

# %%
from shapely.geometry import Point

bound = gpd.GeoDataFrame({
    'x': [80, 150, 106.5, 123],
    'y': [15, 50, 2.8, 24.5]
})
# 添加矢量列
bound.geometry = bound.apply(lambda row: Point([row['x'], row['y']]), axis=1)
# 初始化CRS
bound.crs = 'EPSG:4326'
# 再投影
bound.to_crs(albers_proj, inplace=True)
bound
# %%
fig = plt.figure(figsize=(8, 8))

# 创建覆盖整个画布的子图1
ax = fig.add_axes((0, 0, 1, 1))
ax = china.geometry.to_crs(albers_proj).plot(ax=ax,
                                             facecolor='grey',
                                             edgecolor='white',
                                             linestyle='--',
                                             alpha=0.8)
ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4,
                                                  label='南海九段线')

# 单独提前设置图例标题大小
plt.rcParams['legend.title_fontsize'] = 14

# 设置图例标题，位置，排列方式，是否带有阴影
ax.legend(title="图例", loc='lower left', ncol=1, shadow=True)

ax.axis('off') # 移除坐标轴
ax.set_xlim(bound.geometry[0].x, bound.geometry[1].x)
ax.set_ylim(bound.geometry[0].y, bound.geometry[1].y)

# 创建南海插图对应的子图，这里的位置和大小信息是我调好的，你可以试着调节看看有什么不同
ax_child = fig.add_axes([0.75, 0.15, 0.2, 0.2])
ax_child = china.geometry.to_crs(albers_proj).plot(ax=ax_child,
                                                   facecolor='grey',
                                                   edgecolor='white',
                                                   linestyle='--',
                                                   alpha=0.8)
ax_child = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax_child,
                                                        edgecolor='grey',
                                                        linewidth=3,
                                                        alpha=0.4,
                                                        label='南海九段线')

ax_child.set_xlim(bound.geometry[2].x, bound.geometry[3].x)
ax_child.set_ylim(bound.geometry[2].y, bound.geometry[3].y)

# 移除子图坐标轴刻度，因为这里的子图需要有边框，所以只移除坐标轴刻度
ax_child.set_xticks([])
ax_child.set_yticks([])

fig.savefig('图20.png', dpi=300)

# %%

data_with_geometry = china

# %%

fig, ax = plt.subplots(figsize=(12, 12))

# 新增缺失值处理参数
ax = data_with_geometry.to_crs(albers_proj).plot(ax=ax,
                                                 column='num',
                                                 cmap='Reds',
                                                 missing_kwds={
                                                     "color": "lightgrey",
                                                     "edgecolor": "black",
                                                     "hatch": "////"
                                                 })

ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4)

ax.axis('off')

fig.savefig('图24.png', dpi=300)
# %%
fig, ax = plt.subplots(figsize=(12, 12))

ax = data_with_geometry.to_crs(albers_proj).plot(ax=ax,
                                                 column='num',
                                                 cmap='Reds',
                                                 missing_kwds={
                                                     "color": "lightgrey",
                                                     "edgecolor": "black",
                                                     "hatch": "////"
                                                 },
                                                 legend=True)

ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4)

ax.axis('off')

fig.savefig('图25.png', dpi=300)
# %%
fig, ax = plt.subplots(figsize=(12, 12))

ax = data_with_geometry.to_crs(albers_proj).plot(ax=ax,
                                                 column='num',
                                                 cmap='Reds',
                                                 missing_kwds={
                                                     "color": "lightgrey",
                                                     "edgecolor": "black",
                                                     "hatch": "////"
                                                 },
                                                 legend=True,
                                                 scheme='NaturalBreaks',
                                                 k=5)

ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4)

ax.axis('off')

fig.savefig('图26.png', dpi=300)
# %%
china.loc[4, 'num_x'] = 0
fig, ax = plt.subplots(figsize=(12, 12))

ax = data_with_geometry.to_crs(albers_proj).plot(ax=ax,
                                                 column='num_x',
                                                 cmap='Reds',
                                                #  missing_kwds={
                                                #     #  "color": "lightgrey",
                                                #      "edgecolor": "black",
                                                #      "hatch": "////",
                                                #      "label": ""
                                                #  },
                                                 legend=True,
                                                 scheme='NaturalBreaks',
                                                 k=6,
                                                 legend_kwds={
                                                     'loc': 'lower left',
                                                     'title': '确诊数量分级',
                                                     'shadow': True
                                                 })

ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                  edgecolor='grey',
                                                  linewidth=3,
                                                  alpha=0.4)

ax.axis('off')

fig.savefig('provicne_distribution.pdf')

pd.DataFrame( china[ [x for x in china.columns if x != 'geometry'] ] ).to_csv('provicne_distribution.csv')