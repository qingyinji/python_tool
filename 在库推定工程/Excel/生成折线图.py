from openpyxl.chart import LineChart, Reference


def chart(ws):
    data = Reference(ws, min_col=2, max_col=11, min_row=1, max_row=22)  # 引用数据系列，用作折线图表的数据值。
    c = LineChart()
    c.add_data(data, titles_from_data=True)
    dates = Reference(ws, min_col=1, min_row=2, max_row=22)
    c.set_categories(dates)
    ws.add_chart(c, 'A24')