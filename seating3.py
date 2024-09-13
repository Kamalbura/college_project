import streamlit as st
import pandas as pd
import logic
import itertools

st.set_page_config(layout="centered")


def ranges(i):
    i = sorted(set(i))
    for key, group in itertools.groupby(enumerate(i), lambda t: t[1] - t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]


with st.sidebar:
    st.title("VASAVI COLLEGE OF ENGINEERING")

    file = st.file_uploader("Upload a CSV/XLSX/XLS file", type=["csv", "xlsx", "xls"])
    exam_type = st.selectbox("Select Examination Type", ["Internal", "External"])

    description = st.text_input("Enter Description of Examination")
    sheet_names = None
    branch = None
    block_rooms = {
        "R": ["R-201", "R-202", "R-203", "R-301", "R-207", "R-208", "R-308", "R-309", "R-307", "R-302", "R-303"],
        "V": ["V-209", "V-109", "V-210", "V-312", "V-118", "V-212", "V-110", "V-211", "V-316", "V-117", "V-108", "V-313", "V-119"],
        "J": ["J-012", "J-112", "J-215", "J-208", "J-106", "J-419", "J-412", "J-007", "J-313", "J-306", "J-301"],
        "C": ["C-101", "C-107", "C-106", "C-305", "C-301", "C-304"],
        "VS": ["VS-001", "VS-002", "VS-101", "VS-102", "VS-201", "VS-301", "VS-302", "VS-303"]
    }
    block_halls = {"R": ["R-204", "R-205", "R-206", "R-304", "R-305", "R-306"]}
    branch_codes = {"733": "CSE", "737": "IT", "735": "ECE", "734": "EEE", "748": "AIML", "732": "CIVIL", "736": "MECH"}

    selected_rooms = []
    selected_halls = []
    selected_blocks = []
    capacities = []

    if file is not None:
        with pd.ExcelFile(file) as xls:
            sheet_names = xls.sheet_names

    if sheet_names is not None:
        branch = st.multiselect("Select Branch", sheet_names)

    selected_blocks = st.multiselect("Select Blocks", list(block_rooms.keys()))

    for block in selected_blocks:
        rooms = st.multiselect("Select Rooms in Block " + str(block), block_rooms[block])
        selected_rooms.extend(rooms)

    for block in selected_blocks:
        if block in block_halls.keys():
            halls = st.multiselect("Select Halls in Block " + str(block), block_halls[block])
            selected_halls.extend(halls)

    room_count = len(selected_rooms)
    hall_count = len(selected_halls)

    if exam_type == "Internal":
        capacities = st.selectbox("Select Capacity", [30, 45, 52, 60])
    else:
        capacities = st.selectbox("Select Capacity", [30, 45])


def generate_html_table(headers, data, isRoom, isExternal=False):
    html_table = '<div style="display: flex; justify-content: center; margin-top: 20px;">\n'
    cols = 1 if isExternal else (2 if isRoom else 1)

    html_table += '<table style="font-size:80%; width:auto; font-weight:400; text-align:center; border-collapse: collapse;">\n'
    html_table += "<tr>"
    for header in headers:
        html_table += f"<th colspan={cols} style='border: 1px solid black;'>{header}</th>"
    html_table += "</tr>\n"

    for row in data:
        html_table += "<tr>"
        for x in row:
            for value in x:
                html_table += f'<td style="font-size:120%; width:200px; height:40px; border: 1px solid black; white-space: nowrap;">{value if value != "-1" else " "}</td>'
        html_table += "</tr>\n"

    html_table += "</table>\n</div>"
    return html_table


def generate_branch_table(data, total):
    html_table = '<table style="min-width:70%; font-size:80%; font-weight:400; text-align:center; margin-left:auto; margin-right:auto;">\n'
    for row in data:
        html_table += "<tr>"
        for x in data[row]:
            html_table += f'<td>{x if x != "-1" else " "}</td>'
        html_table += "</tr>\n"

    html_table += f'<tr><td style="border:0px;"></td><td style="border:0px;"></td><td style="font-weight: 700;">{total}</td></tr>'
    html_table += "</table>"
    return html_table


if file and selected_blocks and (selected_halls or selected_rooms) and branch:
    res = logic.generate(file, selected_blocks, selected_halls, selected_rooms, branch, exam_type, capacities)
    tabs = st.tabs(list(res.keys()))

    for count, i in enumerate(res.keys()):
        with tabs[count]:
            st.markdown('<br><br><br><br><br><br><br><br><br>', unsafe_allow_html=True)
            st.markdown('<h1 style="text-align:center; font-size:200%; margin:0px;">VASAVI COLLEGE OF ENGINEERING, HYDERABAD-31</h1>', unsafe_allow_html=True)
            st.markdown('<h1 style="text-align:center; font-size:200%; margin:0px;">' + description + '</h1>', unsafe_allow_html=True)
            st.markdown('<h3 style="margin-left:auto; margin-right:53%; text-align:center;">ROOM NO : ' + str(i) + '</h3>', unsafe_allow_html=True)

            headers = ["DESK " + str(i + 1) for i in range(4)] if i in logic.vs_rooms else ["DESK " + str(i + 1) for i in range(5)]

            dist_branches = []
            count = 0
            for x in range(len(res[i])):
                for y in range(len(res[i][x])):
                    try:
                        if str(res[i][x][y][0]).split("-") not in dist_branches:
                            dist_branches.append(str(res[i][x][y][0]).split("-")[2])
                    except:
                        pass
                    try:
                        if str(res[i][x][y][1]).split("-") not in dist_branches:
                            dist_branches.append(str(res[i][x][y][1]).split("-")[2])
                    except:
                        pass

            dist_branches = [[0, dist_branches[k], [], []] for k in range(len(dist_branches))]

            for x in range(len(res[i])):
                for y in range(len(res[i][x])):
                    try:
                        if res[i][x][y][0] != -1:
                            count += 1
                    except:
                        pass
                    try:
                        if res[i][x][y][1] != -1:
                            count += 1
                    except:
                        pass

            for x in dist_branches:
                x[2] = list(ranges(x[2]))
                x[3] = list(ranges(x[3]))

            html_table = generate_html_table(headers, res[i], i in selected_rooms, exam_type == "External")
            branch_mem = {}
            total = 0
            for x in dist_branches:
                total += x[0]
                branch_mem[branch_codes[x[1]]] = [str(x[0]), str(x[2]), str(x[3])]

            st.markdown(html_table, unsafe_allow_html=True)
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            st.markdown(generate_branch_table(branch_mem, total), unsafe_allow_html=True)
