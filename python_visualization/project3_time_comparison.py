"""
项目三：时段对比与趋势预测分析
使用 Matplotlib + pyecharts 绘制雷达图、面积图、组合图
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

# 添加时段分类
def get_period(hour):
    if 7 <= hour <= 9: return '早高峰'
    elif 17 <= hour <= 18: return '晚高峰'
    else: return '平峰'

df['period'] = df['hour'].apply(get_period)

# ========== 图表7：早高峰vs晚高峰雷达图 ==========
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

# 选取主要路段
main_roads = ['长安街', '二环路', '三环路', '四环路', '建国门外大街', '中关村大街']
periods = ['早高峰', '晚高峰']

# 计算各时段各路段平均流量
angles = np.linspace(0, 2 * np.pi, len(main_roads), endpoint=False).tolist()
angles += angles[:1]  # 闭合

colors = ['#667eea', '#ff4d4f']
for i, period in enumerate(periods):
    values = []
    for road in main_roads:
        avg_flow = df[(df['name'] == road) & (df['period'] == period)]['flow'].mean()
        values.append(avg_flow if not np.isnan(avg_flow) else 0)
    values += values[:1]  # 闭合
    
    ax.plot(angles, values, 'o-', linewidth=2.5, label=period, color=colors[i], markersize=8)
    ax.fill(angles, values, alpha=0.15, color=colors[i])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(main_roads, fontsize=11)
ax.set_ylim(0, max([df[(df['name'] == road) & (df['period'] == '晚高峰')]['flow'].mean() 
                     for road in main_roads]) * 1.2)
ax.set_title('早高峰 vs 晚高峰流量对比雷达图', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('chart7_peak_comparison_radar.png', dpi=150, bbox_inches='tight')
plt.show()
print("图表7已保存: chart7_peak_comparison_radar.png")

# ========== 图表8：各时段流量与速度组合图 ==========
fig, ax1 = plt.subplots(figsize=(12, 6))

hourly_stats = df.groupby('hour').agg({
    'flow': 'mean',
    'speed': 'mean',
    'congestion': 'mean'
}).reset_index()

# 柱状图 - 流量
bars = ax1.bar(hourly_stats['hour'], hourly_stats['flow'], 
               color='#667eea', alpha=0.7, width=0.6, label='平均流量')
ax1.set_xlabel('时段', fontsize=12)
ax1.set_ylabel('平均流量 (辆/h)', fontsize=12, color='#667eea')
ax1.tick_params(axis='y', labelcolor='#667eea')

# 折线图 - 速度
ax2 = ax1.twinx()
line = ax2.plot(hourly_stats['hour'], hourly_stats['speed'], 
                color='#ff4d4f', marker='o', linewidth=2.5, markersize=8, label='平均速度')
ax2.set_ylabel('平均速度 (km/h)', fontsize=12, color='#ff4d4f')
ax2.tick_params(axis='y', labelcolor='#ff4d4f')

# 添加拥堵等级背景色
for idx, row in hourly_stats.iterrows():
    if row['congestion'] >= 3:
        ax1.axvspan(row['hour']-0.4, row['hour']+0.4, alpha=0.1, color='red')

# 合并图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)

ax1.set_title('各时段流量与速度组合分析图', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(range(7, 19))
ax1.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('chart8_flow_speed_combo.png', dpi=150, bbox_inches='tight')
plt.show()
print("图表8已保存: chart8_flow_speed_combo.png")

# ========== 图表9：道路类型时段流量面积图 ==========
fig, ax = plt.subplots(figsize=(12, 6))

# 按道路类型和时段聚合
type_hour_flow = df.groupby(['type', 'hour'])['flow'].mean().unstack(level=0)

ax.stackplot(type_hour_flow.index, 
             type_hour_flow['主干道'].values,
             type_hour_flow['环线'].values,
             type_hour_flow['商业街'].values,
             type_hour_flow['快速路'].values,
             labels=['主干道', '环线', '商业街', '快速路'],
             colors=['#667eea', '#a78bfa', '#ff7eb3', '#52C41A'],
             alpha=0.8)

ax.set_xlabel('时段', fontsize=12)
ax.set_ylabel('平均流量 (辆/h)', fontsize=12)
ax.set_title('各类型道路时段流量面积图', fontsize=14, fontweight='bold', pad=15)
ax.legend(loc='upper left', fontsize=11)
ax.set_xticks(range(7, 19))
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('chart9_roadtype_area.png', dpi=150, bbox_inches='tight')
plt.show()
print("图表9已保存: chart9_roadtype_area.png")

print("\n项目三完成！生成3张图表：")
print("7. 早高峰vs晚高峰雷达图")
print("8. 流量与速度组合分析图")
print("9. 道路类型时段流量面积图")
