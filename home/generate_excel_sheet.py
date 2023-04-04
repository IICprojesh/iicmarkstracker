import openpyxl
from bs4 import BeautifulSoup
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill, NamedStyle

workbook = openpyxl.Workbook()
sheet = workbook.active

my_style = NamedStyle(name="highlight")
my_style.font = Font(bold=True)
my_style.alignment = Alignment(vertical="center")

my_style1 = NamedStyle(name="border")
my_style1.border = Border(left=Side(border_style="thin", color="000000"), right=Side(border_style="thin", color="000000"), top=Side(
    border_style="thin", color="000000"), bottom=Side(border_style="thin", color="000000"))
my_style1.alignment = Alignment(vertical="center", horizontal="center")


def write_to_sheet(cell, value, style=None):
    if cell == "A4":
        sheet.column_dimensions["A"].width = len(value)
    elif cell == "B4":
        sheet.column_dimensions["B"].width = len(value)
    # code to set the width of other cell
    # elif re.match(r"^[^]")
    sheet[cell] = value
    if style:
        sheet[cell].style = style


def general_info(soup):
    _general_info = []
    ids = ["title", "name", "lid", "yearsem"]
    for idx, id in enumerate(ids):
        texts = soup.find(id=id).text.split(":")
        for cell_id, text in enumerate(texts):
            if cell_id == 0:
                _general_info.append((f"A{idx+1}", text))
            else:
                _general_info.append((f"B{idx+1}", text))
    return _general_info


def extract_marks_info(soup):
    # get all the marks of students to print in excel
    print(f"table: {soup.find('table')}")
    start_row = 6
    table_head = soup.find("thead")
    marks_infos = []
    cell_idx_vals = {}
    for idx, th in enumerate(table_head.find_all("th")):
        print("info", th.text)
        marks_infos.append((f"{chr(idx+65)}{start_row}", th.text))
        cell_idx_vals[idx] = chr(idx+65)

    # get all the table data in order
    table_body = soup.find("tbody")
    print(f"table_body: {table_body}")
    for id, row in enumerate(table_body.find_all("tr")):
        # added one because A1 has already been taken and shoould start from A2
        initiate_id = id+start_row
        marks_infos.append((f"A{initiate_id+1}", row.find("th").text))
        for idx, data in enumerate(row.find_all("td")):
            marks_infos.append(
                (f"{cell_idx_vals[idx+1]}{initiate_id+1}", data.text))
    print(f"marks_infos: {marks_infos}")
    return marks_infos


def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    basic_info = general_info(soup)
    print(f"basic_info: {basic_info}")
    for cell, value in basic_info:
        write_to_sheet(cell, value, my_style)

    marks_info = extract_marks_info(soup)
    for cell, value in marks_info:
        write_to_sheet(cell, value, my_style1)

    return workbook, basic_info[2][1]
