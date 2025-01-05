import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt


def get_font_size(num_directors):
    """
    根据导演数量动态获取合适的字体大小
    """
    if num_directors < 10:
        return 14
    elif num_directors < 20:
        return 10
    elif num_directors < 30:
        return 8
    else:
        return 6


def visualize_sheet_data(df, sheet_name):
    try:
        # 设置中文字体和解决负号显示问题
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 可视化年份分布（柱形图）
        year_distribution = df['年份'].value_counts().sort_index()
        plt.figure(figsize=(10, 6))
        plt.bar(year_distribution.index.astype(str), year_distribution.values)
        plt.title(f'{sheet_name} - 年份分布柱形图')
        plt.xlabel('年份')
        plt.ylabel('数量')
        plt.xticks(rotation=45)
        plt.show()

        # 可视化电影类型分布（饼图）
        movie_type_distribution = df['电影类型_细分'].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(movie_type_distribution.values, labels=movie_type_distribution.index, autopct='%1.1f%%')
        plt.title(f'{sheet_name} - 电影类型分布饼图')
        plt.show()

        # 可视化导演分布（纵向柱形图）
        director_distribution = df['导演'].value_counts()
        num_directors = len(director_distribution.index)
        font_size = get_font_size(num_directors)
        plt.figure(figsize=(10, 6))
        plt.bar(director_distribution.index, director_distribution.values, width = 0.4)  # 调整柱子宽度
        plt.title(f'{sheet_name} - 导演分布柱形图')
        plt.xlabel('导演')
        plt.ylabel('数量')
        plt.xticks(rotation=90, fontsize=font_size)  # 根据导演数量动态设置字体大小
        plt.show()

        # 可视化实时热度（折线图）
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['实时热度'])
        plt.title(f'{sheet_name} - 实时热度折线图')
        plt.xlabel('数据点')
        plt.ylabel('实时热度')
        plt.show()

    except KeyError as e:
        print(f"{sheet_name} 中缺少列: {e}")
    except Exception as e:
        print(f"{sheet_name} 发生错误: {e}")


def visualize_excel_data(file_path):
    try:
        # 读取 Excel 文件的所有表名
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names

        for sheet_name in sheet_names:
            # 读取每个工作表的数据
            df = excel_file.parse(sheet_name)
            visualize_sheet_data(df, sheet_name)

    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    file_path = './combined_processed_files.xlsx'
    visualize_excel_data(file_path)