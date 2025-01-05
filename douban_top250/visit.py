import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def visualize_excel_data(file_path):
    # 设置 matplotlib 字体为支持中文的字体（如SimHei）并解决负号显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取Excel文件
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print("文件未找到")
        return

    # 尝试将评分列转换为数值类型，非数值值转换为NaN
    try:
        df['评分'] = pd.to_numeric(df['评分'], errors='coerce')
        # 删除包含NaN的行
        df = df.dropna(subset=['评分'])
    except KeyError:
        print("评分列不存在于数据中")
        return

    # 按照评分列绘制主星图（假设是绘制箱线图）
    plt.figure(figsize=(8, 6))
    plt.boxplot(df['评分'])
    plt.title('评分列的箱线图')
    plt.ylabel('评分')
    plt.show()

    # 按照国家列绘制饼图
    country_counts = df['国家'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(country_counts.values, labels=country_counts.index, autopct='%1.1f%%')
    plt.title('国家列的分布饼图')
    plt.show()

    # 按照类型列绘制饼图
    type_counts = df['类型'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%')
    plt.title('类型列的分布饼图')
    plt.show()

    # 以评分列和评分数的关系绘制散点图
    if '评价数' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.scatter(df['评分'], df['评价数'])
        plt.xlabel('评分')
        plt.ylabel('评价数')
        plt.title('评分与评价数的关系散点图')
        plt.show()
    else:
        print("评价数列不存在于数据中")


# 调用函数并传入Excel文件路径
file_path = './豆瓣电影Top250_修改后.xlsx'
visualize_excel_data(file_path)