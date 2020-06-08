import requests as req
import csv, json

export_url = 'https://udb.moe.edu.tw/DetailReportList/%E5%AD%B8%E7%94%9F%E9%A1%9E/StatDepartmentRegistrationRate/Export'

payload = {
    'FileType': "csv",
    'Parameter': '''{
        "Year":["108"],
        "BuildType":["PUBLIC","PRIVATE"],
        "UniversityType":["Tech"],
        "UniversityList":[],
        "DepartmentName":"資訊管理系",
        "EduSystem":["4R"],
        "PageSize":"10",
        "PageNumber":1
    }'''
}

session = req.Session()

print('post..')
res = session.post(export_url, data = payload)

data = json.loads(res.text)
download_url = f'https://udb.moe.edu.tw/DetailReportList/%E5%AD%B8%E7%94%9F%E9%A1%9E/StatDepartmentRegistrationRate/Download/?fileGuid={data["handle"]}&filename={data["fileName"]}'

print('get csv file.')
csv_file = session.get(download_url)
decoded_content = csv_file.content.decode('utf-8')
reader = csv.reader(decoded_content.splitlines(), delimiter = ',')
rows = list(reader)

d_rows = []
new_rows = []

for i in range(1, len(rows)):
    if (rows[i][3]) == (rows[i - 1][3]):
        d_rows.append(i)

for i in range(1, len(rows)):
    if i not in d_rows:
        new_rows.append(rows[i])

new_rows.sort(reverse = True, key = lambda s: float(s[12]))

'''
with open('n_output.csv', 'w', newline = '', encoding = 'utf-8') as file:
    writer = csv.writer(file, delimiter = ',')

    for row in new_rows:
        writer.writerow(row)

print('done.')
'''

j_name = []
j_a = []
j_b = []
j_ab = []
j_c = []
j_d = []

for i in range(len(new_rows)):
    j_name.append(new_rows[i][4])
    j_a.append(int(new_rows[i][9]))
    j_b.append(int(new_rows[i][10]))
    j_c.append(new_rows[i][11])
    j_d.append(new_rows[i][12])

for i in range(len(j_a)):
    j_ab.append(j_a[i] - j_b[i])

'''
new_name = ""

for i in range(len(j_name)):
    if "國立" in j_name[i]:
        j_name[i] = j_name[i].strip("國立")
    elif "財團法人" in j_name[i]:
        for j in range(len(j_name[i])):
            if j > (j_name[i].find("財團法人") + 3):
                new_name += j_name[i][j]
        j_name[i] = new_name
        new_name = ""
'''

nrows = []

with open('schoolname.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        nrows.append(row)

for i in range(len(j_name)):
    for j in range(len(nrows)):
        if j_name[i] == nrows[j][0]:
            j_name[i] = nrows[j][1]

print('writing chart file.')
file = open('index.html', 'w')
file.write("<!DOCTYPE html>\n")
file.write("<script src='https://code.jquery.com/jquery-3.5.1.min.js'></script>\n")
file.write("<script src='https://code.highcharts.com/highcharts.js'></script>\n")
file.write("<html>\n")
file.write("<head>\n")
file.write("<title>Test</title>\n")
file.write("</head>\n")
file.write("<body>\n")
file.write("<div id='container' style='width:100%; height:500px;'>\n")
file.write("<script>\n")
file.write("var data = {\n")
file.write("chart: {zoomType: 'xy'},\n")
file.write("title: {text: '108年新生註冊率'},\n")
file.write("subtitle: {text: 'Source: 教育部大專校院校務資訊公開平臺'},\n")
file.write("xAxis: [{categories: [")
for i in range(len(j_name) - 1):
    file.write("'" + j_name[i] + "', ")
file.write("'" + j_name[len(j_name) - 1] + "'")
file.write("], crosshair: true}],\n")
file.write("yAxis: [{\n")
file.write("labels: {format: '{value}%', style: {color: Highcharts.getOptions().colors[1]}}, title: {text: '註冊率', style: {color: Highcharts.getOptions().colors[1]}}\n")
file.write("}, {\n")
file.write("title: {text: '人數', style: {color: Highcharts.getOptions().colors[0]}}, labels: {format: '{value}人', style: {color: Highcharts.getOptions().colors[0]}}, opposite: true\n")
file.write("}],\n")
file.write("tooltip: {shared: true},\n")
file.write("legend: {layout: 'vertical', align: 'left', x: 120, verticalAlign: 'top', y: 100, floating: true, backgroundColor: Highcharts.defaultOptions.legend.backgroundColor || 'rgba(255,255,255,0.25)'},\n")
file.write("series: [{\n")
file.write("name: '招生名額', type: 'column', yAxis: 1, data: [")
for i in range(len(j_ab) - 1):
    file.write(str(j_ab[i]) + ", ")
file.write(str(j_ab[len(j_ab) - 1]))
file.write("], tooltip: {valueSuffix: '人'}\n")
file.write("}, {\n")
file.write("name: '註冊人數', type: 'column', yAxis: 1, data: [")
for i in range(len(j_c) - 1):
    file.write(j_c[i] + ", ")
file.write(j_c[len(j_c) - 1])
file.write("], tooltip: {valueSuffix: '人'}\n")
file.write("}, {\n")
file.write("name: '註冊率', type: 'spline', data: [")
for i in range(len(j_d) - 1):
    file.write(j_d[i] + ", ")
file.write(j_d[len(j_d) - 1])
file.write("], tooltip: {valueSuffix: '%'}\n")
file.write("}]\n")
file.write("}\n")
file.write("$('#container').highcharts(data);\n")
file.write("</script>\n")
file.write("</div>\n")
file.write("</body>\n")
file.write("</html>\n")
file.close

print('done.')