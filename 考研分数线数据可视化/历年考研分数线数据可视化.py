
# In[1]:
# ### 导入库

import json
import requests
import pandas as pd 
import pyecharts.options as opts
from pyecharts.charts import *
from pyecharts.globals import ThemeType#设定主题
from pyecharts.commons.utils import JsCode
import chardet 
import jieba
import numpy as np

# In[2]:
# ### 读取文件考研历年国家分数线

df1 = pd.read_csv(r'./考研历年国家分数线(1).csv')
df2 = pd.read_csv(r'./考研历年国家分数线(2).csv')
df3 = pd.read_csv(r'./考研历年国家分数线(3).csv')
df4 = pd.read_csv(r'./考研历年国家分数线(4).csv')
df5 = pd.read_csv(r'./考研历年国家分数线(5).csv')
df6 = pd.read_csv(r'./考研历年国家分数线(6).csv')
df_all= pd.concat([df1,df2,df3,df4,df5,df6])
df_all.info()

# In[3]:
# ### 打印 df_all 数据框的形状信息，查看数据的行数和列数

print(df_all.shape)

# In[4]:
# ### 检查并打印数据中的重复值和空值情况

print('重复值：' ,df_all.duplicated().sum())
print('空值: \n',df_all.isnull().sum())

# In[5]:
# ### 处理重复值和空值

df_all = df_all.drop_duplicates()
df_all = df_all.dropna(axis=0,how='any')

# In[6]:
# ### 查看并打印数据的基本信息，包括列名、数据类型

df_all.info()
print(df_all.shape)

# In[7]:
# ### 检查打印数据中的重复值和空值情况

print('重复值：' ,df_all.duplicated().sum())
print('空值: \n',df_all.isnull().sum())

# In[8]:
# ### 删除不需要的列并查看前两行的数据

df_all = df_all.drop(labels=['学校名称_链接','院系名称_链接','专业名称_链接'],axis=1)
df_all.head(2)

# In[9]:
# ### 替换特殊字符并查看前两行的数据

df_all['专业名称'] = df_all['专业名称'].str.replace('\(专业学位\)','')
df_all['专业名称'] = df_all['专业名称'].str.replace('★','')
df_all.head(2)

# In[10]:
# ### 单独筛选出2020年考研信息并查看数据详情

data_2020 = df_all[df_all['年份'] == 2020]
data_2020.info()

# In[11]:
# ### 统计专业

data_2020['专业名称'].value_counts()[:100]

# In[12]:
# ### 分组归纳学校对应的专业数（专业可能是重复值）

data_2020.groupby('学校名称')['专业名称'].count().sort_values(ascending = False)[:100]

# In[13]:
# ### 转化考研专业总分特殊值

def tranform_num(x):
    if '-' in x:
        return 0
    else:
        return x
    
data_2020['总分'] = data_2020['总分'].apply(lambda x:tranform_num(x) )
data_2020['总分'] = data_2020['总分'].astype('int')

# In[14]:
# ### 分组归纳各专业的最高分，最低分，平均分

data_1 = data_2020.groupby('专业名称')['总分'].agg([np.mean, np.max,np.min])
data_1['mean'] = data_1['mean'].astype('int')
data_1 = data_1.sort_values(by=['mean'],ascending=False)[:50]
data_1

# In[15]:
# ### 绘制各专业分数的柱状图

bar = Bar(init_opts=opts.InitOpts(theme='light',
                                    width='1000px',
                                    height='1200px')
                                    )

bar.add_xaxis(data_1.index.tolist())
bar.add_yaxis('最高分', 
               data_1['max'].tolist(),
               z_level=1,
               stack='1',
               category_gap='50%',
               tooltip_opts=opts.TooltipOpts(is_show=False),
               label_opts=opts.LabelOpts(position='insideRight', formatter='{c} 分'),
               itemstyle_opts={"normal": {
                        'shadowBlur': 10,
                        'shadowColor': 'rgba(0, 0, 0, 0.1)',
                        'shadowOffsetX': 10,
                        'shadowOffsetY': 10,
                        'color':'#ec9bad',
                        'borderColor': 'rgb(220,220,220)',
                        'borderWidth':2}
                },
               )
bar.add_yaxis('最低分', 
               data_1['min'].tolist(),
               z_level=1,
               stack='1',
               category_gap='50%',
               tooltip_opts=opts.TooltipOpts(is_show=False),
               label_opts=opts.LabelOpts(position='insideLeft', formatter='{c} 分'),
               itemstyle_opts={"normal": {
                        'shadowBlur': 10,
                        'shadowColor': 'rgba(0, 0, 0, 0.1)',
                        'shadowOffsetX': 10,
                        'shadowOffsetY': 10,
                        'color':'#87CEFA',
                        'borderColor': 'rgb(220,220,220)',
                        'borderWidth':2}
                },
               )


bar.set_global_opts(title_opts=opts.TitleOpts(title="各专业的最高分和最低分",
                                              pos_left="center",
                                              pos_top='0%',
                                              title_textstyle_opts=opts.TextStyleOpts(font_size=20,
                                                                                      color='#00BFFF')),
                        legend_opts=opts.LegendOpts(is_show=True, pos_top='3%'),
                        datazoom_opts=opts.DataZoomOpts(type_='inside',
                                                    range_start=50,   # 设置起止位置，50%-100%
                                                    range_end=100,
                                                    orient='vertical'),
                        xaxis_opts=opts.AxisOpts(is_show=False, max_=818),
                        yaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=False),
                                             axistick_opts=opts.AxisTickOpts(is_show=False),
                                             axislabel_opts=opts.LabelOpts(color='#528B8B', font_size=10, font_weight='bold')),
                    )
bar.reversal_axis()
bar.render_notebook()

# In[16]:
# ### 统计 2020 年数据中各专业名称的出现次数，并提取前 50 个出现次数最多的专业名称

data_2 = data_2020['专业名称'].value_counts()[:50]

# In[17]:
# ### 绘制2020年考研专业Top50

data_x =data_2.index.tolist()
data_y = data_2.values.tolist()

bar = Bar(init_opts=opts.InitOpts(theme='light',
                                  width='1000px',
                                  height='900px'))
bar.add_xaxis(data_x)
bar.add_yaxis('考研专业', [int(i) for i in data_y])
bar.set_series_opts(label_opts=opts.LabelOpts(position="insideLeft",
                                              font_size=12,
                                              font_weight='bold',
                                              formatter='{b}:{c} 个'))
bar.set_global_opts(title_opts=opts.TitleOpts(title="2020年考研专业Top50", pos_top='2%', pos_left='center', 
                                              title_textstyle_opts=opts.TextStyleOpts(font_size=20,
                                                                                      color='#00BFFF')),
                    legend_opts=opts.LegendOpts(is_show=False),
                    xaxis_opts=opts.AxisOpts(is_show=False, is_scale=True),
                    yaxis_opts=opts.AxisOpts(is_show=False),
                    datazoom_opts=opts.DataZoomOpts(type_='inside',
                                                    range_start=50,   # 设置起止位置，50%-100%
                                                    range_end=100,
                                                    orient='vertical'),
                    
                    visualmap_opts=opts.VisualMapOpts(is_show=False, 
                                          max_=1058,
                                          min_=1,
                                          is_piecewise=False,
                                          dimension=0,
                                          range_color=['rgba(236,155,173,1)', 'rgba(237,157,178,0.4)'])
                                      )
bar.reversal_axis()
bar.render_notebook()

# In[18]:
# ### 读取2021年考研调剂大学信息并查看前几行数据的信息

df_info = pd.read_excel(r'./大学信息2021new.xlsx')
df_info.head()

# In[19]:
# ### openpyxl库的安装

get_ipython().system('pip install openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple  --trusted-host pypi.tuna.tsinghua.edu.cn')


# In[20]:
# ### 查看数据的基本信息

df_info.info()

# In[21]:
# ### 转换学校属性类别

#转换学校属性
def transform_attr(x):
    if '211' in x and '985' not in x:
        return 211 
    elif '985' in x:
        return '985'
    else:
        return '双非'

#转换学校类型   
def transform_type(x):
    if '理工类' in x or '理工类院校' in x or '理工科' in x or '理工、教学研究型大学' in x or '理工类\n[4]' in x or '理工\n[6]' in x:
        return '理工'
    elif '综合类' in x or '综合性大学\n[3]' in x or '综合类（应用型大学）' in x or '综合、研究教学型大学' in x or '综合类大学' in x or '综合师范类' in x:
        return '综合'
    elif '师范类院校' in x or '师范类' in x or '师范类（综合类）' in x or '师范（综合）' in x or '地方师范院校' in x:
        return '师范'
    elif '农林类' in x or '农业类' in x: 
        return '农林'
    elif '医药类' in x:
        return '医药'
    elif '民族类' in x:
        return '民族'
    elif '未知' in x or '国有企业' in x or '科技型企业' in x or '公立大学' in x:
        return '其他'
    elif '重点' in x or '省' in x or '2' in x or '' in x:
        return '其他'
    else:
        return x 
    
# 转换数据
df_info['school_level'] = df_info.school_attr.astype(str).apply(lambda x:transform_attr(x))
df_info['school_types'] = df_info.school_type.astype(str).apply(lambda x: transform_type(x))

# 筛选字段
df_info= df_info[['school','province','school_level','school_types']]

# 处理省份数据
df_info.loc[(df_info.school=='北京工商大学')&(df_info.province=='未知'), 'province']= '北京' 
df_info.loc[(df_info.school=='哈尔滨工程大学')&(df_info.province=='未知'), 'province']= '哈尔滨' 
df_info.loc[(df_info.school=='江苏大学')&(df_info.province=='未知'), 'province']= '江苏' 
df_info.loc[(df_info.school=='青岛大学')&(df_info.province=='未知'), 'province']= '山东' 
df_info.loc[(df_info.school=='北京石油化工学院')&(df_info.province=='未知'), 'province']= '北京' 
df_info.loc[(df_info.school=='齐鲁工业大学')&(df_info.province=='未知'), 'province']= '山东'
df_info.loc[(df_info.school=='江苏科技大学')&(df_info.province=='未知'), 'province']= '江苏'
df_info.loc[(df_info.school=='浙江农林大学')&(df_info.province=='未知'), 'province']= '浙江'
df_info.loc[(df_info.school=='燕山大学')&(df_info.province=='未知'), 'province']= '河北'
df_info.loc[(df_info.school=='福州大学')&(df_info.province=='未知'), 'province']= '福建'
df_info.loc[(df_info.school=='内蒙古科技大学')&(df_info.province=='未知'), 'province']= '内蒙古'

# In[22]:
# ### 查看数据的前几条信息

df_info.head()

# In[23]:
# ### 删除重复值并查看数据的基本信息

df_info = df_info.drop_duplicates()
df_info.info()

# In[24]:
# ### 确认数据的行数和列数

df_info.shape

# In[25]:
# ### 读取考研调剂数据 Excel 文件并查看行数和列数

df = pd.read_excel(r'./考研调剂数据-3.08.xlsx')
df.shape

# In[26]:
# ### 筛选出 2021 年的调剂信息并查看行数和列数

df_2021 = df[df['time'].str.contains('2021')].copy()
df_2021.shape

# In[27]:
# ### 通过左连接将 df_2021 和 df_info 按照 'school' 列合并，以获取调剂信息和大学信息的结合数据

pd.merge(df_2021,df_info,how = 'left',on = 'school').shape

# In[28]:
# ### 通过左连接确保 df_2021 中的所有行都被保留，同时补充 df_info 中的相关信息，展示前五条信息

df_all = pd.merge(df_2021,df_info,how = 'left',on = 'school')
df_all.head(5)

# In[29]:
# ### 重新排列数据，保留包括学校名称、调剂信息名称、时间、省份、学校层次和学校类型

df_all = df_all[['school','name','time','province','school_level','school_types']]
df_all.head()

# In[30]:
# ### 查看缺失数据

df_all.isnull().sum()

# In[31]:
# ### 发布时间对应的发布频次

pub_time = df_all.time.value_counts().sort_index()
pub_time

# In[32]:
# ### 调剂信息发布时间走势图

line1 = Line(init_opts=opts.InitOpts(width='1000px',height='600px'))
line1.add_xaxis(pub_time.index.tolist())
line1.add_yaxis('发布热度',pub_time.values.tolist(),
               areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
               label_opts=opts.LabelOpts(is_show=True))
line1.set_global_opts(title_opts=opts.TitleOpts(title='调剂信息发布时间走势图'),
                     toolbox_opts=opts.ToolboxOpts(),
                      xaxis_opts=opts.AxisOpts(name='时间',
                                               type_='category',                                           
                                               axislabel_opts=opts.LabelOpts(rotate=45),
                                               ),
                     visualmap_opts=opts.VisualMapOpts())
line1.render_notebook()

# In[33]:
# ### 计算学校层次（school_level）的百分比分布

level_perc = df_all.school_level.value_counts() / df_all.school_level.value_counts().sum()
display(level_perc)
level_perc = np.round(level_perc * 100 ,2)
level_perc

# In[34]:
# ### 绘制学校类别饼图

pie1 = Pie(init_opts=opts.InitOpts(theme='light',width='800px',height='600px'))
pie1.add("", 
         [*zip(level_perc.index, level_perc.values)], 
         radius=["40%","75%"]) 
pie1.set_global_opts(title_opts=opts.TitleOpts(title='学校层次分布',pos_left='center', pos_top='center',title_textstyle_opts=opts.TextStyleOpts(
                                                   color='#00BFFF', font_size=30, font_weight='bold'),
                                               ), 
                     legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
#                      toolbox_opts=opts.ToolboxOpts()
                    )   
pie1.set_series_opts(label_opts=opts.LabelOpts(formatter="{c}%")) 
pie1.render_notebook()

# %%
