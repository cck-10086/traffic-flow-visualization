# 城市交通流量可视化分析

对城市道路交通流量数据做统计分析与交互式可视化，包含 Python 分析脚本和基于 ECharts 的网页可视化两个部分。

## 功能

- 小时流量趋势与高峰时段识别
- 路段流量 Top10 排名
- 流量热力图、速度箱线图、流量-速度散点关系
- 拥堵等级分布与高峰/平峰对比
- 道路类型流量构成分析

## 技术栈

- Python：pandas、matplotlib、numpy
- 前端：原生 HTML/CSS/JavaScript、ECharts

## 目录结构

```
traffic-flow-visualization/
├── data/                       # 交通流量原始数据
├── python_visualization/       # 分析脚本与静态图表
│   ├── project1_traffic_flow.py        # 小时流量趋势分析
│   ├── project2_congestion_analysis.py # 拥堵分析
│   └── project3_time_comparison.py     # 高峰/平峰对比
└── visualization/              # ECharts 交互式可视化页面
    ├── index.html
    ├── style.css
    ├── app.js
    └── data/
```

## 运行

静态图表：

```bash
cd python_visualization
python project1_traffic_flow.py
```

交互式页面：直接用浏览器打开 `visualization/index.html`。
