import xlwt


class ExcelPipeline:
    def __init__(self):
        self.book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook设置编码格式
        self.sheet = self.book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建sheet表
        self.col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
        for i in range(len(self.col)):
            self.sheet.write(0, i, self.col[i])  # 写入excel,参数对应：行、列、值
        self.row = 1

    def process_item(self, item, spider):
        for i, value in enumerate(item.values()):
            self.sheet.write(self.row, i, value)
        self.row += 1
        return item

    def close_spider(self, spider):
        self.book.save('豆瓣电影Top250.xlsx')

'''
import csv


class CsvPipeline:
    def __init__(self):
        self.file = open('豆瓣电影Top250.csv', 'w', encoding='utf-8', newline='')  # 打开文件，指定编码和去除多余空行
        self.writer = csv.writer(self.file)
        self.col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
        self.writer.writerow(self.col)  # 写入表头

    def process_item(self, item, spider):
        data = [item.get(field, '') for field in ["link", "imgSrc", "ctitle", "otitle", "rating", "judgeNum", "inq", "bd"]]
        self.writer.writerow(data)  # 写入一行数据，从item中提取对应字段的值
        return item

    def close_spider(self, spider):
        self.file.close()  # 关闭文件
'''