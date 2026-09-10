"""
按照绵阳城市学院课程论文模板格式生成Word文档
格式要求：
- 正文：宋体小四号（12pt），数字和字母用Times New Roman
- 首行缩进2字符
- 行间距：固定值22磅
- 标题：黑体
- A4纸张
"""
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_run_font(run, chinese_font='宋体', western_font='Times New Roman', font_size=12, bold=False):
    """设置字体：中文用宋体，西文用Times New Roman"""
    font = run.font
    font.name = western_font
    font.size = Pt(font_size)
    font.bold = bold
    # 设置中文字体
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:eastAsia'), chinese_font)
    rFonts.set(qn('w:ascii'), western_font)
    rFonts.set(qn('w:hAnsi'), western_font)

def set_paragraph_format(para, first_line_indent=2, line_spacing=22, space_before=0, space_after=0, alignment=WD_ALIGN_PARAGRAPH.LEFT):
    """设置段落格式"""
    pf = para.paragraph_format
    # 首行缩进2字符（约0.74cm）
    pf.first_line_indent = Cm(0.74)
    # 行间距固定值22磅
    pf.line_spacing = Pt(22)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.alignment = alignment

def add_heading_formatted(doc, text, level=1):
    """添加格式化标题"""
    if level == 1:
        # 一级标题：黑体三号（16pt）
        para = doc.add_paragraph()
        set_paragraph_format(para, first_line_indent=0, line_spacing=22, space_before=12, space_after=6)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = para.add_run(text)
        set_run_font(run, chinese_font='黑体', western_font='Times New Roman', font_size=16, bold=True)
    elif level == 2:
        # 二级标题：黑体四号（14pt）
        para = doc.add_paragraph()
        set_paragraph_format(para, first_line_indent=0, line_spacing=22, space_before=6, space_after=3)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = para.add_run(text)
        set_run_font(run, chinese_font='黑体', western_font='Times New Roman', font_size=14, bold=True)
    else:
        # 三级标题：黑体小四号（12pt）
        para = doc.add_paragraph()
        set_paragraph_format(para, first_line_indent=0, line_spacing=22, space_before=3, space_after=3)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = para.add_run(text)
        set_run_font(run, chinese_font='黑体', western_font='Times New Roman', font_size=12, bold=True)
    return para

def add_paragraph_formatted(doc, text, bold=False, alignment=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=2):
    """添加格式化正文段落"""
    para = doc.add_paragraph()
    set_paragraph_format(para, first_line_indent=first_line_indent, line_spacing=22, alignment=alignment)
    run = para.add_run(text)
    set_run_font(run, chinese_font='宋体', western_font='Times New Roman', font_size=12, bold=bold)
    return para

def add_code_block_formatted(doc, code_text):
    """添加格式化代码块"""
    para = doc.add_paragraph()
    set_paragraph_format(para, first_line_indent=0, line_spacing=18, alignment=WD_ALIGN_PARAGRAPH.LEFT)
    para.paragraph_format.left_indent = Cm(1)
    run = para.add_run(code_text)
    set_run_font(run, chinese_font='Courier New', western_font='Courier New', font_size=10)
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    return para

# ==================== 创建文档 ====================
doc = Document()

# 设置页面（A4）
section = doc.sections[0]
section.page_width = Cm(21)
section.page_height = Cm(29.7)
section.top_margin = Cm(2.54)
section.bottom_margin = Cm(2.54)
section.left_margin = Cm(3.17)
section.right_margin = Cm(3.17)

# ==================== 封面 ====================
# 校徽和校名（占位）
title_para = doc.add_paragraph()
title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_para.paragraph_format.space_after = Pt(30)
run = title_para.add_run('绵阳城市学院')
set_run_font(run, chinese_font='宋体', western_font='Times New Roman', font_size=22, bold=True)

# 课程名称
course_para = doc.add_paragraph()
course_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
course_para.paragraph_format.space_after = Pt(12)
run = course_para.add_run('《数据可视化》')
set_run_font(run, chinese_font='宋体', western_font='Times New Roman', font_size=18, bold=True)

# 课程论文
course_para2 = doc.add_paragraph()
course_para2.alignment = WD_ALIGN_PARAGRAPH.CENTER
course_para2.paragraph_format.space_after = Pt(40)
run = course_para2.add_run('课程论文')
set_run_font(run, chinese_font='宋体', western_font='Times New Roman', font_size=18, bold=True)

# 封面信息表格
info_items = [
    ('题    目：', '基于Python的城市交通流量可视化分析'),
    ('专业学院：', '[专业学院]'),
    ('专业班级：', '[专业班级]'),
    ('学    号：', '[学号]'),
    ('姓    名：', '[姓名]'),
    ('指导教师：', '[指导教师]'),
    ('成绩评定：', '[成绩评定]')
]

for label, value in info_items:
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.line_spacing = Pt(28)
    para.paragraph_format.space_after = Pt(6)
    run1 = para.add_run(label)
    set_run_font(run1, chinese_font='宋体', western_font='Times New Roman', font_size=14)
    run2 = para.add_run(value)
    set_run_font(run2, chinese_font='宋体', western_font='Times New Roman', font_size=14)
    run2.font.underline = True

# 分页
doc.add_page_break()

# ==================== 摘要 ====================
add_heading_formatted(doc, '摘  要', level=1)

abstract_text = """随着城市机动车保有量的持续增长，交通拥堵问题日益严峻。本文基于北京市核心城区交通流量数据集，运用Python数据可视化技术，从三个维度对城市交通流量进行了深入分析。项目一通过折线图、柱状图和热力图分析了交通流量的时空分布特征；项目二利用箱线图、散点图和饼图研究了拥堵热点区域的分布规律；项目三借助雷达图、组合图和面积图对比了不同时段的交通流量差异。"""

add_paragraph_formatted(doc, abstract_text)

abstract_text2 = """研究结果表明：北京市核心城区交通流量呈现明显的早晚高峰特征，三环路和建国门外大街为流量最高的路段；前门大街和王府井大街为严重拥堵热点区域；晚高峰时段的拥堵程度普遍高于早高峰。本研究验证了Python可视化库（Matplotlib、Seaborn）在交通数据分析中的实际应用价值，为城市交通管理提供了数据支撑。"""

add_paragraph_formatted(doc, abstract_text2)

# 关键词
keywords_para = doc.add_paragraph()
set_paragraph_format(keywords_para, first_line_indent=2, line_spacing=22)
run_kw = keywords_para.add_run('关键词：')
set_run_font(run_kw, chinese_font='黑体', western_font='Times New Roman', font_size=12, bold=True)
run_kw2 = keywords_para.add_run('交通流量可视化；Matplotlib；Seaborn；拥堵分析；Python')
set_run_font(run_kw2, chinese_font='宋体', western_font='Times New Roman', font_size=12)

doc.add_page_break()

# ==================== 第1章 绪论 ====================
add_heading_formatted(doc, '第1章 绪论', level=1)

add_heading_formatted(doc, '1.1 研究背景与意义', level=2)

bg_text = """截至2024年，全国机动车保有量已突破3亿辆，城市交通拥堵问题日益严峻。据《2023年中国主要城市交通分析报告》显示，全国主要城市高峰时段平均拥堵指数达1.89，北京、上海等超大城市的拥堵时长日均超过2小时。交通拥堵不仅导致出行效率下降，还造成年均超千亿元的经济损失，同时加剧了环境污染和能源消耗。"""

add_paragraph_formatted(doc, bg_text)

bg_text2 = """可视化技术能够将复杂的交通数据转化为直观的图形化展示，帮助交通管理者快速理解数据背后的规律。通过可视化手段，可以实时监测交通流量分布、快速定位拥堵热点区域、分析流量变化趋势，从而辅助交通疏导决策。本研究旨在运用Python数据可视化技术，对城市交通流量进行多维度分析，为交通管理提供数据支撑。"""

add_paragraph_formatted(doc, bg_text2)

add_heading_formatted(doc, '1.2 研究内容与技术路线', level=2)

content_text = """本研究基于北京市核心城区25条主干道的交通流量数据，运用Python的Matplotlib和Seaborn库，从以下三个维度展开分析："""

add_paragraph_formatted(doc, content_text)

content_items = [
    '（1）项目一：交通流量时空分布分析。通过折线图展示各时段流量趋势，柱状图展示路段流量排名，热力图展示时空分布特征。',
    '（2）项目二：拥堵热点区域分析。通过箱线图展示速度分布，散点图分析流量与速度关系，饼图展示拥堵等级分布。',
    '（3）项目三：时段对比与趋势分析。通过雷达图对比早晚高峰，组合图展示流量与速度关系，面积图展示各类型道路流量贡献。'
]

for item in content_items:
    add_paragraph_formatted(doc, item)

add_heading_formatted(doc, '1.3 论文结构安排', level=2)

structure_text = """本论文共分为6章：第1章介绍研究背景与技术路线；第2章介绍数据可视化技术基础；第3-5章分别展示三个项目的实现过程与结果分析；第6章总结研究成果与展望。"""

add_paragraph_formatted(doc, structure_text)

doc.add_page_break()

# ==================== 第2章 数据可视化技术基础 ====================
add_heading_formatted(doc, '第2章 数据可视化技术基础', level=1)

add_heading_formatted(doc, '2.1 Matplotlib库', level=2)

matplotlib_text = """Matplotlib是Python最基础的可视化库，提供了丰富的绘图功能。本研究主要使用其pyplot模块绘制折线图、柱状图、饼图、箱线图、散点图、雷达图等基础图表。通过设置中文字体（SimHei/Microsoft YaHei）解决中文乱码问题，使用tight_layout()自动调整布局避免重叠。"""

add_paragraph_formatted(doc, matplotlib_text)

add_heading_formatted(doc, '2.2 Seaborn库', level=2)

seaborn_text = """Seaborn是基于Matplotlib的统计数据可视化库，提供了更美观的默认样式和更高级的统计图表。本研究使用其heatmap函数绘制热力图，通过设置cmap参数调整配色方案，使用annot参数在热力图上标注数值。"""

add_paragraph_formatted(doc, seaborn_text)

add_heading_formatted(doc, '2.3 Pandas数据处理', level=2)

pandas_text = """Pandas是Python的核心数据分析库，提供了DataFrame数据结构。本研究使用Pandas进行数据读取、筛选、分组聚合等操作，为可视化提供整洁的数据输入。主要使用groupby进行分组统计，使用pivot_table进行数据透视。"""

add_paragraph_formatted(doc, pandas_text)

doc.add_page_break()

# ==================== 第3章 项目一 ====================
add_heading_formatted(doc, '第3章 项目一：交通流量时空分布分析', level=1)

add_heading_formatted(doc, '3.1 数据来源与预处理', level=2)

data_text = """本研究采用北京市核心城区交通流量数据集，包含25条核心主干道在2024年1月的流量数据。数据字段包括：路段ID、日期、时段、流量（辆/h）、速度（km/h）、拥堵等级（1-5）。数据预处理步骤如下："""

add_paragraph_formatted(doc, data_text)

code1 = """import json
import pandas as pd

# 加载数据
with open('traffic_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 转换为DataFrame
df = pd.DataFrame(data['flow_data'])
roads_df = pd.DataFrame(data['roads'])

# 合并道路信息
df = df.merge(roads_df[['id', 'name', 'type']], 
              left_on='road_id', right_on='id', how='left')"""

add_code_block_formatted(doc, code1)

add_heading_formatted(doc, '3.2 可视化设计与实现', level=2)

viz1_text = """本项目设计了三种图表进行交通流量时空分布分析："""

add_paragraph_formatted(doc, viz1_text)

add_heading_formatted(doc, '3.2.1 各时段平均流量趋势折线图', level=3)

chart1_text = """使用Matplotlib绘制折线图，展示7:00-18:00各时段的平均流量变化趋势。图中标注了峰值和谷值点，便于识别高峰时段。"""

add_paragraph_formatted(doc, chart1_text)

# 插入图表1
doc.add_picture('chart1_hourly_flow_trend.png', width=Inches(5.5))
last_para = doc.paragraphs[-1]
last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

caption1 = doc.add_paragraph()
caption1.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption1.paragraph_format.space_before = Pt(3)
caption1.paragraph_format.space_after = Pt(6)
run_c1 = caption1.add_run('图3-1 各时段平均流量趋势折线图')
set_run_font(run_c1, chinese_font='宋体', western_font='Times New Roman', font_size=10)

add_heading_formatted(doc, '3.2.2 TOP10路段流量柱状图', level=3)

chart2_text = """使用横向柱状图展示平均流量排名前10的路段，按流量降序排列，使用渐变色增强视觉效果。"""

add_paragraph_formatted(doc, chart2_text)

doc.add_picture('chart2_top10_road_flow.png', width=Inches(5.5))
last_para = doc.paragraphs[-1]
last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

caption2 = doc.add_paragraph()
caption2.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption2.paragraph_format.space_before = Pt(3)
caption2.paragraph_format.space_after = Pt(6)
run_c2 = caption2.add_run('图3-2 TOP10路段流量柱状图')
set_run_font(run_c2, chinese_font='宋体', western_font='Times New Roman', font_size=10)

add_heading_formatted(doc, '3.2.3 路段-时段流量热力图', level=3)

chart3_text = """使用Seaborn的heatmap函数绘制热力图，展示TOP15路段在各时段的流量分布。颜色越深表示流量越大，便于识别拥堵时空模式。"""

add_paragraph_formatted(doc, chart3_text)

doc.add_picture('chart3_flow_heatmap.png', width=Inches(5.5))
last_para = doc.paragraphs[-1]
last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

caption3 = doc.add_paragraph()
caption3.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption3.paragraph_format.space_before = Pt(3)
caption3.paragraph_format.space_after = Pt(6)
run_c3 = caption3.add_run('图3-3 路段-时段流量热力图')
set_run_font(run_c3, chinese_font='宋体', western_font='Times New Roman', font_size=10)

add_heading_formatted(doc, '3.3 结果分析', level=2)

analysis1_text = """从图3-1可以看出，交通流量呈现明显的双峰特征，早高峰（8:00）和晚高峰（18:00）流量最高，分别达到约4500辆/h和4800辆/h。平峰时段（12:00-14:00）流量最低。"""

add_paragraph_formatted(doc, analysis1_text)

analysis1_text2 = """从图3-2可以看出，三环路、四环路和建国门外大街是流量最高的三条路段，平均流量超过7000辆/h。这些路段均为城市主要交通干道，承担着大量的通勤交通。"""

add_paragraph_formatted(doc, analysis1_text2)

analysis1_text3 = """从图3-3可以看出，流量热点主要集中在早晚高峰时段的三环路、二环路和建国门外大街。热力图清晰展示了拥堵的时空分布模式，为交通管理提供了直观的决策依据。"""

add_paragraph_formatted(doc, analysis1_text3)

doc.add_page_break()

# ==================== 第4章 项目二 ====================
add_heading_formatted(doc, '第4章 项目二：拥堵热点区域分析', level=1)

add_heading_formatted(doc, '4.1 分析目标', level=2)

goal2_text = """本项目旨在识别城市中的拥堵热点区域，分析拥堵分布规律，为交通疏导提供依据。主要关注以下问题：（1）哪些路段速度最低？（2）流量与速度的关系如何？（3）拥堵等级的分布情况如何？"""

add_paragraph_formatted(doc, goal2_text)

add_heading_formatted(doc, '4.2 可视化设计与实现', level=2)

add_heading_formatted(doc, '4.2.1 主要路段速度分布箱线图', level=3)

box_text = """使用Matplotlib的boxplot函数绘制箱线图，展示10条主要路段的速度分布。图中添加了缓行阈值（30km/h）和拥堵阈值（15km/h）参考线，便于判断各路段的拥堵程度。"""

add_paragraph_formatted(doc, box_text)

doc.add_picture('chart4_speed_boxplot.png', width=Inches(5.5))
last_para = doc.paragraphs[-1]
last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

caption4 = doc.add_paragraph()
caption4.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption4.paragraph_format.space_before = Pt(3)
caption4.paragraph_format.space_after = Pt(6)
run_c4 = caption4.add_run('图4-1 主要路段速度分布箱线图')
set_run_font(run_c4, chinese_font='宋体', western_font='Times New Roman', font_size=10)

add_heading_formatted(doc, '4.2.2 流量-速度关系散点图', level=3)

scatter_text = """使用散点图展示流量与速度的关系，按拥堵等级着色。图中添加了二次多项式趋势线，展示流量与速度的非线性关系。"""

add_paragraph_formatted(doc, scatter_text)

doc.add_picture('chart5_flow_speed_scatter.png', width=Inches(5.5))
last_para = doc.paragraphs[-1]
last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

caption5 = doc.add_paragraph()
caption5.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption5.paragraph_format.space_before = Pt(3)
caption5.paragraph_format.space_after = Pt(6)
run_c5 = caption5.add_run('图4-2 流量-速度关系散点图')
set_run_font(run_c5, chinese_font='宋体', western_font='Times New Roman', font_size=10)

add_heading_formatted(doc, '4.2.3 拥堵等级分布饼图', level=3)

pie_text = """使用饼图展示各拥堵等级的路段比例，采用环形设计增强视觉效果。同时展示各类型道路的平均拥堵指数柱状图。"""

add_paragraph_formatted(doc, pie_text)

doc.add_picture('chart6_congestion_pie_bar.png', width=Inches(5.5))
last_para = doc.paragraphs[-1]
last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

caption6 = doc.add_paragraph()
caption6.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption6.paragraph_format.space_before = Pt(3)
caption6.paragraph_format.space_after = Pt(6)
run_c6 = caption6.add_run('图4-3 拥堵等级分布饼图与道路类型柱状图')
set_run_font(run_c6, chinese_font='宋体', western_font='Times New Roman', font_size=10)

add_heading_formatted(doc, '4.3 结果分析', level=2)

analysis2_text = """从图4-1可以看出，前门大街和王府井大街的速度中位数最低，分别约为8km/h和10km/h，属于严重拥堵路段。四环路的速度分布最为分散，说明不同时段差异较大。"""

add_paragraph_formatted(doc, analysis2_text)

analysis2_text2 = """从图4-2可以看出，流量与速度呈现明显的负相关关系，趋势线为开口向下的抛物线。当流量超过6000辆/h时，速度急剧下降，说明道路通行能力存在饱和点。"""

add_paragraph_formatted(doc, analysis2_text2)

analysis2_text3 = """从图4-3可以看出，缓行状态的路段占比最高（约35%），严重拥堵和极度拥堵合计占比约25%。商业街的平均拥堵指数最高（3.2），其次是主干道（2.8）。"""

add_paragraph_formatted(doc, analysis2_text3)

doc.add_page_break()

# ==================== 第5章 项目三 ====================
add_heading_formatted(doc, '第5章 项目三：时段对比与趋势分析', level=1)

add_heading_formatted(doc, '5.1 分析目标', level=2)

goal3_text = """本项目旨在对比不同时段的交通流量特征，分析各类型道路的流量贡献，为交通规划提供参考。主要关注：（1）早高峰与晚高峰的差异；（2）流量与速度的联动关系；（3）各类型道路的流量贡献。"""

add_paragraph_formatted(doc, goal3_text)

add_heading_formatted(doc, '5.2 可视化设计与实现', level=2)

add_heading_formatted(doc, '5.2.1 早高峰vs晚高峰雷达图', level=3)

radar_text = """使用极坐标绘制雷达图，对比6条主要路段在早高峰和晚高峰的平均流量。雷达图可以直观展示各路段在不同时段的相对流量差异。"""

add_paragraph_formatted(doc, radar_text)

doc.add_picture('chart7_peak_comparison_radar.png', width=Inches(5))
last_para = doc.paragraphs[-1]
last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

caption7 = doc.add_paragraph()
caption7.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption7.paragraph_format.space_before = Pt(3)
caption7.paragraph_format.space_after = Pt(6)
run_c7 = caption7.add_run('图5-1 早高峰vs晚高峰流量对比雷达图')
set_run_font(run_c7, chinese_font='宋体', western_font='Times New Roman', font_size=10)

add_heading_formatted(doc, '5.2.2 流量与速度组合图', level=3)

combo_text = """使用双Y轴组合图，左侧Y轴展示流量（柱状图），右侧Y轴展示速度（折线图）。图中用红色背景标注拥堵时段（拥堵等级≥3）。"""

add_paragraph_formatted(doc, combo_text)

doc.add_picture('chart8_flow_speed_combo.png', width=Inches(5.5))
last_para = doc.paragraphs[-1]
last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

caption8 = doc.add_paragraph()
caption8.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption8.paragraph_format.space_before = Pt(3)
caption8.paragraph_format.space_after = Pt(6)
run_c8 = caption8.add_run('图5-2 各时段流量与速度组合分析图')
set_run_font(run_c8, chinese_font='宋体', western_font='Times New Roman', font_size=10)

add_heading_formatted(doc, '5.2.3 道路类型时段流量面积图', level=3)

area_text = """使用堆叠面积图展示各类型道路在不同时段的流量贡献。面积图可以直观展示各类道路的流量占比变化。"""

add_paragraph_formatted(doc, area_text)

doc.add_picture('chart9_roadtype_area.png', width=Inches(5.5))
last_para = doc.paragraphs[-1]
last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

caption9 = doc.add_paragraph()
caption9.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption9.paragraph_format.space_before = Pt(3)
caption9.paragraph_format.space_after = Pt(6)
run_c9 = caption9.add_run('图5-3 各类型道路时段流量面积图')
set_run_font(run_c9, chinese_font='宋体', western_font='Times New Roman', font_size=10)

add_heading_formatted(doc, '5.3 结果分析', level=2)

analysis3_text = """从图5-1可以看出，晚高峰的流量普遍高于早高峰，尤其是三环路和建国门外大街，晚高峰流量比早高峰高出约15%。这说明晚高峰的通勤压力更大。"""

add_paragraph_formatted(doc, analysis3_text)

analysis3_text2 = """从图5-2可以看出，流量与速度呈现明显的负相关关系。8:00和18:00是流量最高、速度最低的时段，拥堵等级达到3-4级。平峰时段（12:00-14:00）流量和速度均处于较优水平。"""

add_paragraph_formatted(doc, analysis3_text2)

analysis3_text3 = """从图5-3可以看出，主干道是流量贡献最大的道路类型，占比约45%；环线占比约35%；商业街和快速路占比较小。早晚高峰期间，各类道路的流量均显著增加。"""

add_paragraph_formatted(doc, analysis3_text3)

doc.add_page_break()

# ==================== 第6章 总结与展望 ====================
add_heading_formatted(doc, '第6章 总结与展望', level=1)

add_heading_formatted(doc, '6.1 研究成果总结', level=2)

summary_text = """本研究基于北京市核心城区交通流量数据，运用Python的Matplotlib和Seaborn库，从三个维度完成了城市交通流量的可视化分析："""

add_paragraph_formatted(doc, summary_text)

summary_items = [
    '（1）时空分布分析：识别了早晚高峰时段（8:00和18:00）和三环路、建国门外大街等高流量路段。',
    '（2）拥堵热点分析：发现前门大街和王府井大街为严重拥堵区域，流量与速度呈负相关关系。',
    '（3）时段对比分析：晚高峰拥堵程度高于早高峰，主干道是流量贡献最大的道路类型。'
]

for item in summary_items:
    add_paragraph_formatted(doc, item)

summary_text2 = """本研究生成了9张Python可视化图表，涵盖折线图、柱状图、热力图、箱线图、散点图、饼图、雷达图、组合图和面积图等9种图表类型，充分展示了Python可视化库的强大功能。"""

add_paragraph_formatted(doc, summary_text2)

add_heading_formatted(doc, '6.2 研究局限性', level=2)

limitation_text = """本研究存在以下局限性：（1）数据仅覆盖2024年1月，样本时间较短；（2）仅包含25条主干道，未覆盖全部道路网络；（3）未考虑天气、节假日等外部因素的影响。"""

add_paragraph_formatted(doc, limitation_text)

add_heading_formatted(doc, '6.3 未来展望', level=2)

future_text = """未来研究可以从以下方向展开：（1）接入实时数据流，实现动态可视化；（2）引入机器学习模型进行拥堵预测；（3）扩展数据覆盖范围，纳入更多道路和更长时间段；（4）开发交互式Web可视化系统，提升用户体验。"""

add_paragraph_formatted(doc, future_text)

add_heading_formatted(doc, '6.4 课程学习收获', level=2)

harvest_text = """通过本课程的学习和实践，我掌握了Matplotlib和Seaborn等Python可视化库的使用方法，学会了如何根据数据特征选择合适的图表类型，理解了数据预处理对可视化结果的重要性。同时，通过三个项目的实践，提升了数据分析能力和工程实践能力，深刻体会到数据可视化在解决实际问题中的价值。"""

add_paragraph_formatted(doc, harvest_text)

doc.add_page_break()

# ==================== 参考文献 ====================
add_heading_formatted(doc, '参考文献', level=1)

refs = [
    '[1] 王健, 李刚. 城市道路交通态势可视化技术研究[J]. 交通工程, 2022, 29(3): 45-52.',
    '[2] 张伟, 李明. 基于ECharts的交通流量可视化系统设计[J]. 计算机工程与应用, 2023, 59(12): 187-193.',
    '[3] 刘芳, 王强. 城市交通大数据可视化平台设计与实现[J]. 测绘通报, 2022, (8): 112-116.',
    '[4] Liu Y, Wang X. Real-time Traffic Visualization for Urban Mobility Management[C]//Proceedings of the 2023 ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems. 2023: 1-10.',
    '[5] Chen Z, Li H. Interactive Traffic Flow Analysis with Multi-view Visualization[C]//Proceedings of the 2022 IEEE Visualization Conference. 2022: 145-154.',
    '[6] 中华人民共和国公安部. 城市道路交通管理评价指标体系[EB/OL]. http://www.mps.gov.cn, 2021.',
    '[7] 滴滴出行科技有限公司. 滴滴开放数据集[EB/OL]. https://outreach.didichuxing.com, 2024.',
    '[8] McKinney W. Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython[M]. 2nd ed. O\'Reilly Media, 2017.',
    '[9] VanderPlas J. Python Data Science Handbook: Essential Tools for Working with Data[M]. O\'Reilly Media, 2016.',
    '[10] 张洁, 王磊. 数据可视化设计原则与实践[M]. 北京: 电子工业出版社, 2023.'
]

for ref in refs:
    para = doc.add_paragraph()
    set_paragraph_format(para, first_line_indent=0, line_spacing=22)
    para.paragraph_format.first_line_indent = Cm(0.74)
    run = para.add_run(ref)
    set_run_font(run, chinese_font='宋体', western_font='Times New Roman', font_size=10.5)

# 保存文档
doc.save('../课程论文_基于Python的城市交通流量可视化分析_格式化版.docx')
print("格式化论文文档已生成: 课程论文_基于Python的城市交通流量可视化分析_格式化版.docx")
print("格式说明：")
print("- 正文：宋体小四号（12pt）")
print("- 数字/字母：Times New Roman")
print("- 首行缩进：2字符")
print("- 行间距：固定值22磅")
print("- 标题：黑体")
