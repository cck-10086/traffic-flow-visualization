"""
项目二：拥堵热点区域分析
使用 Matplotlib + Seaborn 绘制箱线图、散点图、饼图
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False

# 加载数据
with open('../data/traffic_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data['flow_data'])
roads_df = pd.DataFrame(data['roads'])
df = df.merge(roads_df[['id', 'name', 'type']], left_on='road_id', right_on='id', how='left')

# 添加拥堵等级标签
def get_congestion_label(level):
    if level == 1: return '畅通'
    elif level == 2: return '缓行'
    elif level == 3: return '拥堵'
    elif level == 4: return '严重拥堵'
    else: return '极度拥堵'

df['congestion_label'] = df['congestion'].apply(get_congestion_label)

# ========== 图表4：各路段速度分布箱线图 ==========
fig, ax = plt.subplots(figsize=(12, 7))

# 选取部分主要路段
main_roads = ['长安街', '二环路', '三环路', '四环路', '建国门外大街', 
              '中关村大街', '王府井大街', '前门大街', '金融街', '平安大街']
box_data = [df[df['name'] == road]['speed'].values for road in main_roads if road in df['name'].values]
box_labels = [road for road in main_roads if road in df['name'].values]

bp = ax.boxplot(box_data, labels=box_labels, patch_artist=True, 
                notch=True, showmeans=True, meanline=True)

colors = plt.cm.Set3(np.linspace(0, 1, len(bp['boxes'])))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_ylabel('速度 (km/h)', fontsize=12)
ax.set_title('主要路段速度分布箱线图', fontsize=14, fontweight='bold', pad=15)
ax.axhline(y=30, color='#FAAD14', linestyle='--', alpha=0.7, label='缓行阈值 (30km/h)')
ax.axhline(y=15, color='#FF4D4F', linestyle='--', alpha=0.7, label='拥堵阈值 (15km/h)')
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3, axis='y')
plt.xticks(rotation=30, ha='right')

plt.tight_layout()
plt.savefig('chart4_speed_boxplot.png', dpi=150, bbox_inches='tight')
plt.show()
print("图表4已保存: chart4_speed_boxplot.png")

# ========== 图表5：流量-速度关系散点图 ==========
fig, ax = plt.subplots(figsize=(10, 7))

# 按拥堵等级着色
congestion_colors = {1: '#52C41A', 2: '#FAAD14', 3: '#FF4D4F', 4: '#CF1322', 5: '#871618'}
congestion_labels = {1: '畅通', 2: '缓行', 3: '拥堵', 4: '严重拥堵', 5: '极度拥堵'}

for level in sorted(df['congestion'].unique()):
    subset = df[df['congestion'] == level]
    ax.scatter(subset['flow'], subset['speed'], 
               c=congestion_colors[level], label=congestion_labels[level],
               alpha=0.6, s=60, edgecolors='white', linewidth=0.5)

# 添加趋势线
z = np.polyfit(df['flow'], df['speed'], 2)
p = np.poly1d(z)
x_trend = np.linspace(df['flow'].min(), df['flow'].max(), 100)
ax.plot(x_trend, p(x_trend), "k--", alpha=0.5, linewidth=2, label='趋势线')

ax.set_xlabel('流量 (辆/h)', fontsize=12)
ax.set_ylabel('速度 (km/h)', fontsize=12)
ax.set_title('流量与速度关系散点图', fontsize=14, fontweight='bold', pad=15)
ax.legend(loc='upper right', fontsize=10, title='拥堵等级')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('chart5_flow_speed_scatter.png', dpi=150, bbox_inches='tight')
plt.show()
print("图表5已保存: chart5_flow_speed_scatter.png")

# ========== 图表6：拥堵等级分布饼图 ==========
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 饼图
congestion_dist = df['congestion_label'].value_counts()
colors_pie = ['#52C41A', '#FAAD14', '#FF4D4F', '#CF1322', '#871618']
labels_pie = [f'{k}\n{v}条' for k, v in congestion_dist.items()]

wedges, texts, autotexts = ax1.pie(congestion_dist.values, labels=congestion_dist.index, 
                                     autopct='%1.1f%%', colors=colors_pie[:len(congestion_dist)],
                                     startangle=90, explode=[0.02]*len(congestion_dist),
                                     textprops={'fontsize': 11})
for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_color('white')

ax1.set_title('拥堵等级分布', fontsize=14, fontweight='bold', pad=15)

# 环形图
center_circle = plt.Circle((0, 0), 0.5, color='white', linewidth=2)
ax1.add_patch(center_circle)
ax1.text(0, 0, f'总计\n{len(df)}条', ha='center', va='center', fontsize=12, fontweight='bold')

# 各类型道路平均拥堵指数柱状图
road_type_congestion = df.groupby('type').agg({
    'congestion': 'mean',
    'speed': 'mean'
}).reset_index().sort_values('congestion', ascending=True)

bars = ax2.barh(road_type_congestion['type'], road_type_congestion['congestion'], 
                color=['#667eea', '#a78bfa', '#ff7eb3'], edgecolor='white', height=0.6)

for bar, val in zip(bars, road_type_congestion['congestion']):
    ax2.text(val + 0.05, bar.get_y() + bar.get_height()/2, f'{val:.2f}', 
             va='center', fontsize=11, fontweight='bold')

ax2.set_xlabel('平均拥堵等级', fontsize=12)
ax2.set_title('各类型道路平均拥堵指数', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlim(0, max(road_type_congestion['congestion']) * 1.2)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('chart6_congestion_pie_bar.png', dpi=150, bbox_inches='tight')
plt.show()
print("图表6已保存: chart6_congestion_pie_bar.png")

print("\n项目二完成！生成3张图表：")
print("4. 路段速度分布箱线图")
print("5. 流量-速度关系散点图")
print("6. 拥堵等级分布饼图+道路类型柱状图")
