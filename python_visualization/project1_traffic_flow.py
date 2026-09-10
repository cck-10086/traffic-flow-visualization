"""
项目一：交通流量时空分布分析
使用 Matplotlib + Seaborn 绘制折线图、柱状图、热力图
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

# 转换为DataFrame
df = pd.DataFrame(data['flow_data'])
roads_df = pd.DataFrame(data['roads'])

# 数据预处理：合并道路信息
df = df.merge(roads_df[['id', 'name', 'type']], left_on='road_id', right_on='id', how='left')

# ========== 图表1：各时段平均流量趋势折线图 ==========
fig, ax = plt.subplots(figsize=(10, 6))

hourly_flow = df.groupby('hour')['flow'].mean().reset_index()
ax.plot(hourly_flow['hour'], hourly_flow['flow'], marker='o', linewidth=2.5, 
        markersize=8, color='#667eea', label='平均流量')

# 标注峰值和谷值
max_idx = hourly_flow['flow'].idxmax()
min_idx = hourly_flow['flow'].idxmin()
ax.annotate(f'峰值: {hourly_flow.loc[max_idx, "flow"]:.0f}辆/h', 
            xy=(hourly_flow.loc[max_idx, 'hour'], hourly_flow.loc[max_idx, 'flow']),
            xytext=(10, 20), textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', fc='#ff4d4f', alpha=0.8),
            arrowprops=dict(arrowstyle='->', color='#ff4d4f'),
            fontsize=11, color='white', fontweight='bold')

ax.annotate(f'谷值: {hourly_flow.loc[min_idx, "flow"]:.0f}辆/h', 
            xy=(hourly_flow.loc[min_idx, 'hour'], hourly_flow.loc[min_idx, 'flow']),
            xytext=(10, -30), textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', fc='#52C41A', alpha=0.8),
            arrowprops=dict(arrowstyle='->', color='#52C41A'),
            fontsize=11, color='white', fontweight='bold')

ax.set_xlabel('时段', fontsize=12)
ax.set_ylabel('平均流量 (辆/h)', fontsize=12)
ax.set_title('北京市核心城区各时段平均交通流量趋势', fontsize=14, fontweight='bold', pad=15)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xticks(range(7, 19))
ax.legend(loc='upper left', fontsize=11)

plt.tight_layout()
plt.savefig('chart1_hourly_flow_trend.png', dpi=150, bbox_inches='tight')
plt.show()
print("图表1已保存: chart1_hourly_flow_trend.png")

# ========== 图表2：TOP10路段流量柱状图 ==========
fig, ax = plt.subplots(figsize=(10, 7))

road_flow = df.groupby('name')['flow'].mean().sort_values(ascending=True).tail(10)
colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(road_flow)))

bars = ax.barh(road_flow.index, road_flow.values, color=colors, edgecolor='white', height=0.7)

# 添加数值标签
for bar, val in zip(bars, road_flow.values):
    ax.text(val + 100, bar.get_y() + bar.get_height()/2, f'{val:.0f}', 
            va='center', fontsize=10, fontweight='bold')

ax.set_xlabel('平均流量 (辆/h)', fontsize=12)
ax.set_title('TOP10 路段平均流量排名', fontsize=14, fontweight='bold', pad=15)
ax.set_xlim(0, max(road_flow.values) * 1.15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('chart2_top10_road_flow.png', dpi=150, bbox_inches='tight')
plt.show()
print("图表2已保存: chart2_top10_road_flow.png")

# ========== 图表3：路段-时段流量热力图 ==========
fig, ax = plt.subplots(figsize=(12, 8))

# 选取流量前15的路段
top_roads = df.groupby('name')['flow'].mean().nlargest(15).index
heatmap_data = df[df['name'].isin(top_roads)].pivot_table(
    values='flow', index='name', columns='hour', aggfunc='mean'
)

sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', 
            linewidths=0.5, ax=ax, cbar_kws={'label': '流量 (辆/h)'})

ax.set_xlabel('时段', fontsize=12)
ax.set_ylabel('路段名称', fontsize=12)
ax.set_title('TOP15路段各时段流量热力图', fontsize=14, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig('chart3_flow_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
print("图表3已保存: chart3_flow_heatmap.png")

print("\n项目一完成！生成3张图表：")
print("1. 时段流量趋势折线图")
print("2. TOP10路段流量柱状图") 
print("3. 路段-时段流量热力图")
