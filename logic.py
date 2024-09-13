import pandas as pds
import itertools

branch_codes = {"733":"CSE", "737":"IT", "735":"ECE", "734":"EEE", "748":"AIML", "732":"CIVIL", "736":"MECH"}
room_capacity = {"normal":30 , "hall": 66} #5x6, 11x6
vs_rooms = ["VS-101","VS-102","VS-201","VS-301","VS-302","VS-303"]

def ranges(i):
    i = sorted(set(i))
    for key, group in itertools.groupby(enumerate(i), lambda t: t[1]-t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]

def transpose(l1, l2):
 
    for i in range(len(l1[0])):
        row =[]
        for item in l1:
            row.append(item[i])
        l2.append(row)
    return l2




def generate(file, selected_blocks, selected_halls, selected_rooms, branch, exam_type, capacities):
    xl = pds.ExcelFile(file)
    res = len(xl.sheet_names)
    sheets = []
    counters = []
    for i in range(res):
        sheet = pds.read_excel(file, sheet_name = i)
        rolls = [sheet._get_value(i, "Roll") for i in range(len(sheet.index))]
        sheets.append(rolls)
        counters.append([0, len(rolls)])
    

    rooms = []

    cur_left  = -1
    cur_right = -1

    sheets = []
    counters = []
    
    for i in branch:
        sheet = pds.read_excel(file, sheet_name = i)
        rolls = [sheet._get_value(i, "Roll") for i in range(len(sheet.index))]
        sheets.append(rolls)
        counters.append([0, len(rolls)])

    if(len(sheets) == 1):
        cur_left = 0
    else:
        cur_left = 0
        cur_right = 1

    if(exam_type == "External"):

        if(capacities == 30):
            cur = 0
            while((cur == cur_left or cur == cur_right or (cur < len(counters) and counters[cur][0] >= counters[cur][1]))):
                cur += 1
            
            print("Current:", cur)

            count = 0
            flag = 0


            for i in range(len(selected_rooms)):
                if(selected_rooms[i] in vs_rooms):
                    m, n = 4, 8
                else:
                    m, n = 5, 6
                benches = [[["-1"] for x in range(n)] for y in range(m)]
                if(len(sheets) == 1):
                    for x in range(m):
                        for y in range(n):
                            if(counters[cur_left][0] >= counters[cur_left][1]):
                                break
                            benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                            counters[cur_left][0] += 1
                else:
                    cur_left, cur_right, cur = 0, 1, 2
                    while((cur_left == cur or cur_left == cur_right or (cur_left < len(counters) and counters[cur_left][0] >= counters[cur_left][1]))):
                        cur_left += 1
                    while((cur_right == cur or cur_right == cur_left or (cur_right < len(counters) and counters[cur_right][0] >= counters[cur_right][1]))):
                        cur_right += 1
                    while((cur == cur_left or cur == cur_right or (cur < len(counters) and counters[cur][0] >= counters[cur][1]))):
                        cur += 1
                    for x in range(m):
                        for y in range(n):
                            if(cur_left<len(counters)):
                                if(counters[cur_left][0] >= counters[cur_left][1]):
                                    if(cur_left>cur_right and cur_left>cur):
                                        cur_left += 1
                                    else:
                                        cur_left += 1
                                        while(cur_left == cur_right or cur_left == cur or (cur_left<len(counters) and counters[cur_left][0] >= counters[cur_left][1])):
                                            cur_left += 1
                                        
                            if(cur_right<len(counters)):
                                if(counters[cur_right][0] >= counters[cur_right][1] or (cur_right<len(counters) and counters[cur_right][0] >= counters[cur_right][1])):
                                    if(cur_right>cur_left and cur_right>cur):
                                        cur_right += 1
                                    else:
                                        cur_right += 1
                                        while(cur_right == cur_left or cur_right == cur):
                                            cur_right += 1
                                        
                            if(cur<len(counters)):
                                if(counters[cur][0] >= counters[cur][1] or (cur<len(counters) and counters[cur][0] >= counters[cur][1])):
                                    if(cur>cur_left and cur>cur_right):
                                        cur += 1
                                    else:
                                        cur += 1
                                        while(cur == cur_left or cur == cur_right):
                                            cur += 1
                            if(cur < len(counters)):
                                if(cur_left < len(counters) and cur_right < len(counters)):
                                    if(count%3 == 0): 
                                        if(cur_left<len(counters)):
                                            if(counters[cur_left][0] < counters[cur_left][1]):
                                                benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                                                counters[cur_left][0] += 1
                                                count += 1
                                    elif(count%3 == 1):
                                        if(cur_right<len(counters)):
                                            if(counters[cur_right][0] < counters[cur_right][1]):
                                                benches[x][y][0] = sheets[cur_right][counters[cur_right][0]]
                                                counters[cur_right][0] += 1
                                                count += 1
                                    elif(count%3 == 2):
                                        if(cur<len(counters)):
                                            if(counters[cur][0] < counters[cur][1]):
                                                benches[x][y][0] = sheets[cur][counters[cur][0]]
                                                counters[cur][0] += 1
                                                count += 1
                                else:
                                    if(cur_left >= len(counters) and cur_right >= len(counters)):
                                        if(cur<len(counters)):
                                            if(counters[cur][0] < counters[cur][1]):
                                                benches[x][y][0] = sheets[cur][counters[cur][0]]
                                                
                                                counters[cur][0] += 1
                                                count += 1
                                    else:
                                        if(count%2 == 0):
                                            if(cur_left<len(counters)):
                                                if(counters[cur_left][0] < counters[cur_left][1]):
                                                    benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                                                    
                                                    counters[cur_left][0] += 1
                                                    count += 1
                                            if(cur_right<len(counters)):
                                                if(counters[cur_right][0] < counters[cur_right][1]):
                                                    benches[x][y][0] = sheets[cur_right][counters[cur_right][0]]
                                                    
                                                    counters[cur_right][0] += 1
                                                    count += 1
                                        elif(count%2 == 1):
                                            if(cur<len(counters)):
                                                if(counters[cur][0] < counters[cur][1]):
                                                    benches[x][y][0] = sheets[cur][counters[cur][0]]
                                                    
                                                    counters[cur][0] += 1
                                                    count += 1
                            else:
                                if(flag == 0):
                                    count = 0
                                    flag = 1

                                if(cur_left >= len(counters) or cur_right >= len(counters)):
                                    if(cur_left<len(counters)):
                                            if(counters[cur_left][0] < counters[cur_left][1]):
                                                benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                                                
                                                counters[cur_left][0] += 1
                                    if(cur_right<len(counters)):
                                            if(counters[cur_right][0] < counters[cur_right][1]):
                                                benches[x][y][0] = sheets[cur_right][counters[cur_right][0]]
                                                
                                                counters[cur_right][0] += 1
                                else:
                                    if(count%2 == 0): 
                                        if(cur_left<len(counters)):
                                            if(counters[cur_left][0] < counters[cur_left][1]):
                                                benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                                                
                                                counters[cur_left][0] += 1
                                                count += 1
                                    elif(count%2 == 1):
                                        if(cur_right<len(counters)):
                                            if(counters[cur_right][0] < counters[cur_right][1]):
                                                benches[x][y][0] = sheets[cur_right][counters[cur_right][0]]
                                                counters[cur_right][0] += 1
                                                count += 1      
                rooms.append(benches)

        elif(capacities == 45):
            cur = 0
            while((cur == cur_left or cur == cur_right or (cur < len(counters) and counters[cur][0] >= counters[cur][1]))):
                cur += 1
            
            print("Current:", cur)

            count = 0
            flag = 0


            for i in range(len(selected_rooms)):
                if(selected_rooms[i] in vs_rooms):
                    m, n = 4, 8
                else:
                    m, n = 5, 6
                benches = [[["-1", "-1"] for x in range(n)] for y in range(m)]
                if(len(sheets) == 1):
                    for x in range(m):
                        for y in range(n):
                            if(counters[cur_left][0] >= counters[cur_left][1]):
                                break
                            benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                            counters[cur_left][0] += 1
                else:
                    cur_left, cur_right, cur = 0, 1, 2
                    while((cur_left == cur or cur_left == cur_right or (cur_left < len(counters) and counters[cur_left][0] >= counters[cur_left][1]))):
                        cur_left += 1
                    while((cur_right == cur or cur_right == cur_left or (cur_right < len(counters) and counters[cur_right][0] >= counters[cur_right][1]))):
                        cur_right += 1
                    while((cur == cur_left or cur == cur_right or (cur < len(counters) and counters[cur][0] >= counters[cur][1]))):
                        cur += 1
                    for x in range(m):
                        for y in range(n):
                            if(cur_left<len(counters)):
                                if(counters[cur_left][0] >= counters[cur_left][1]):
                                    if(cur_left>cur_right and cur_left>cur):
                                        cur_left += 1
                                    else:
                                        cur_left += 1
                                        while(cur_left == cur_right or cur_left == cur or (cur_left<len(counters) and counters[cur_left][0] >= counters[cur_left][1])):
                                            cur_left += 1
                                        
                            if(cur_right<len(counters)):
                                if(counters[cur_right][0] >= counters[cur_right][1] or (cur_right<len(counters) and counters[cur_right][0] >= counters[cur_right][1])):
                                    if(cur_right>cur_left and cur_right>cur):
                                        cur_right += 1
                                    else:
                                        cur_right += 1
                                        while(cur_right == cur_left or cur_right == cur):
                                            cur_right += 1
                                        
                            if(cur<len(counters)):
                                if(counters[cur][0] >= counters[cur][1] or (cur<len(counters) and counters[cur][0] >= counters[cur][1])):
                                    if(cur>cur_left and cur>cur_right):
                                        cur += 1
                                    else:
                                        cur += 1
                                        while(cur == cur_left or cur == cur_right):
                                            cur += 1

                            if(y%2 == 0):
                                if(cur_right<len(counters)):
                                    if(counters[cur_right][0] < counters[cur_right][1]):
                                        benches[x][y][1] = sheets[cur_right][counters[cur_right][0]]
                                        counters[cur_right][0] += 1
                                        
                            if(cur_left<len(counters) and count%2 == 0):
                                if(counters[cur_left][0] < counters[cur_left][1]):
                                    benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                                    counters[cur_left][0] += 1
                                    
                            elif(cur<len(counters) and count%2 == 1):
                                if(counters[cur][0] < counters[cur][1]):
                                    benches[x][y][0] = sheets[cur][counters[cur][0]]
                                    counters[cur][0] += 1
                                    
                            count += 1
                            

                    rooms.append(benches)

    elif(capacities == 45):
        for i in range(len(selected_rooms)):
            if(selected_rooms[i] in vs_rooms):
                m, n = 4, 8
            else:
                m, n = 5, 6
            benches = [[["-1", "-1"] for x in range(n)] for y in range(m)]
            if(len(sheets) == 1):
                for x in range(m):
                    for y in range(n):
                        if(counters[cur_left][0] >= counters[cur_left][1]):
                            break
                        benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                        counters[cur_left][0] += 1
            else:
                cur_left, cur_right = 0, 1
                while(cur_left < len(counters) and counters[cur_left][0] >= counters[cur_left][1]):
                    cur_left += 1
                while(cur_right == cur_left or (cur_right < len(counters) and counters[cur_right][0] >= counters[cur_right][1])):
                    cur_right += 1
                
                for x in range(m):
                    for y in range(n):
                        if(cur_left<len(counters)):
                            if(counters[cur_left][0] >= counters[cur_left][1]):
                                if(cur_left>cur_right):
                                    cur_left += 1
                                else:
                                    cur_left += 1
                                    if(cur_left == cur_right):
                                        cur_left += 1
                                    
                        if(cur_right<len(counters)):
                            if(counters[cur_right][0] >= counters[cur_right][1]):
                                if(cur_right>cur_left):
                                    cur_right += 1
                                else:
                                    cur_right += 1
                                    if(cur_right == cur_left):
                                        cur_right += 1
                            
                                    
                        if(cur_left<len(counters)):
                            if(counters[cur_left][0] < counters[cur_left][1]):
                                benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                                counters[cur_left][0] += 1
                        if(y%2 == 0):
                            if(cur_right<len(counters)):
                                if(counters[cur_right][0] < counters[cur_right][1]):
                                    benches[x][y][1] = sheets[cur_right][counters[cur_right][0]]
                                    counters[cur_right][0] += 1
                            
            rooms.append(benches)
    elif(capacities == 60):
        for i in range(len(selected_rooms)):
            if(selected_rooms[i] in vs_rooms):
                m, n = 4, 8
            else:
                m, n = 5, 6
            benches = [[["-1", "-1"] for x in range(n)] for y in range(m)]
            if(len(sheets) == 1):
                for x in range(m):
                    for y in range(n):
                        if(counters[cur_left][0] >= counters[cur_left][1]):
                            break
                        benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                        counters[cur_left][0] += 1
            else:
                cur_left, cur_right = 0, 1
                while(cur_left < len(counters) and counters[cur_left][0] >= counters[cur_left][1]):
                    cur_left += 1
                while(cur_right == cur_left or (cur_right < len(counters) and counters[cur_right][0] >= counters[cur_right][1])):
                    cur_right += 1

                for x in range(m):
                    for y in range(n):
                        if(cur_left<len(counters)):
                            if(counters[cur_left][0] >= counters[cur_left][1]):
                                if(cur_left>cur_right):
                                    cur_left += 1
                                else:
                                    cur_left += 1
                                    if(cur_left == cur_right):
                                        cur_left += 1
                                    
                        if(cur_right<len(counters)):
                            if(counters[cur_right][0] >= counters[cur_right][1]):
                                if(cur_right>cur_left):
                                    cur_right += 1
                                else:
                                    cur_right += 1
                                    if(cur_right == cur_left):
                                        cur_right += 1
                            
                                    
                        if(cur_left<len(counters)):
                            if(counters[cur_left][0] < counters[cur_left][1]):
                                benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                                counters[cur_left][0] += 1
                        if(cur_right<len(counters)):
                            if(counters[cur_right][0] < counters[cur_right][1]):
                                benches[x][y][1] = sheets[cur_right][counters[cur_right][0]]
                                counters[cur_right][0] += 1
            rooms.append(benches)
    elif(capacities == 52):
        for i in range(len(selected_rooms)):
            count = 0
            if(selected_rooms[i] in vs_rooms):
                m, n = 4, 8
            else:
                m, n = 5, 6
            benches = [[["-1", "-1"] for x in range(n)] for y in range(m)]
            if(len(sheets) == 1):
                for x in range(m):
                    for y in range(n):
                        if(counters[cur_left][0] >= counters[cur_left][1]):
                            break
                        benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                        counters[cur_left][0] += 1
            else:
                cur_left, cur_right = 0, 1
                while(cur_left < len(counters) and counters[cur_left][0] >= counters[cur_left][1]):
                    cur_left += 1
                while(cur_right == cur_left or (cur_right < len(counters) and counters[cur_right][0] >= counters[cur_right][1])):
                    cur_right += 1

                for x in range(m):
                    for y in range(n):
                        
                        if(cur_left<len(counters)):
                            if(counters[cur_left][0] >= counters[cur_left][1]):
                                if(cur_left>cur_right):
                                    cur_left += 1
                                else:
                                    cur_left += 1
                                    if(cur_left == cur_right):
                                        cur_left += 1
                                    
                        if(cur_right<len(counters)):
                            if(counters[cur_right][0] >= counters[cur_right][1]):
                                if(cur_right>cur_left):
                                    cur_right += 1
                                else:
                                    cur_right += 1
                                    if(cur_right == cur_left):
                                        cur_right += 1
                            
                                    
                        if(cur_left<len(counters)):
                            if(counters[cur_left][0] < counters[cur_left][1]):
                                benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                                counters[cur_left][0] += 1
                        if(cur_right<len(counters)):
                            if(counters[cur_right][0] < counters[cur_right][1]):
                                if(count == 22):
                                    continue
                                benches[x][y][1] = sheets[cur_right][counters[cur_right][0]]
                                counters[cur_right][0] += 1
                                count += 1
            rooms.append(benches)
    elif(capacities == 30):

        count = 0

        for i in range(len(selected_rooms)):
            if(selected_rooms[i] in vs_rooms):
                m, n = 4, 8
            else:
                m, n = 5, 6
            benches = [[["-1", "-1"] for x in range(n)] for y in range(m)]
            if(len(sheets) == 1):
                for x in range(m):
                    for y in range(n):
                        if(counters[cur_left][0] >= counters[cur_left][1]):
                            break
                        benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                        counters[cur_left][0] += 1
            else:
                cur_left, cur_right = 0, 1
                while(cur_left < len(counters) and counters[cur_left][0] >= counters[cur_left][1]):
                    cur_left += 1
                while(cur_right == cur_left or (cur_right < len(counters) and counters[cur_right][0] >= counters[cur_right][1])):
                    cur_right += 1

                for x in range(m):
                    for y in range(n):
                        if(cur_left<len(counters)):
                            if(counters[cur_left][0] >= counters[cur_left][1]):
                                if(cur_left>cur_right):
                                    cur_left += 1
                                else:
                                    cur_left += 1
                                    if(cur_left == cur_right):
                                        cur_left += 1
                                    
                        if(cur_right<len(counters)):
                            if(counters[cur_right][0] >= counters[cur_right][1]):
                                if(cur_right>cur_left):
                                    cur_right += 1
                                else:
                                    cur_right += 1
                                    if(cur_right == cur_left):
                                        cur_right += 1
                            
                        if(count%2 == 0):   
                            if(cur_left<len(counters)):
                                if(counters[cur_left][0] < counters[cur_left][1]):
                                    benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                                    counters[cur_left][0] += 1
                                    count += 1
                            else:
                                count += 1
                        elif(count%2 == 1):
                            if(cur_right<len(counters)):
                                if(counters[cur_right][0] < counters[cur_right][1]):
                                    benches[x][y][0] = sheets[cur_right][counters[cur_right][0]]
                                    counters[cur_right][0] += 1
                                    count += 1
                            else:
                                count += 1
            rooms.append(benches)

    count = 0
    flag = 0

    for i in range(len(selected_halls)):
        m = 6
        n = 11
        benches = [[["-1"] for x in range(n)] for y in range(m)]
        if(len(sheets) == 1):
            for x in range(m):
                for y in range(n):
                    if(counters[cur_left][0] >= counters[cur_left][1]):
                        break
                    benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                    counters[cur_left][0] += 1
        else:
            cur_left, cur_right = 0, 1
            while(cur_left < len(counters) and counters[cur_left][0] >= counters[cur_left][1]):
                cur_left += 1
            while(cur_right == cur_left or (cur_right < len(counters) and counters[cur_right][0] >= counters[cur_right][1])):
                cur_right += 1
            for x in range(m):
                for y in range(n):
                    if(cur_left<len(counters)):
                        if(counters[cur_left][0] >= counters[cur_left][1]):
                            if(cur_left>cur_right):
                                cur_left += 1
                            else:
                                cur_left += 1
                                while(cur_left == cur_right or (cur_left<len(counters) and counters[cur_left][0] >= counters[cur_left][1])):
                                    cur_left += 1
                                
                    if(cur_right<len(counters)):
                        if(counters[cur_right][0] >= counters[cur_right][1] or (cur_right<len(counters) and counters[cur_right][0] >= counters[cur_right][1])):
                            if(cur_right>cur_left):
                                cur_right += 1
                            else:
                                cur_right += 1
                                while(cur_right == cur_left):
                                    cur_right += 1
                    if(count%2 == 0):   
                        if(cur_left<len(counters)):
                            if(counters[cur_left][0] < counters[cur_left][1]):
                                benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                                counters[cur_left][0] += 1
                                
                        elif(cur_right<len(counters)):
                            if(counters[cur_right][0] < counters[cur_right][1]):
                                benches[x][y][0] = sheets[cur_right][counters[cur_right][0]]
                                counters[cur_right][0] += 1

                        count += 1
                    elif(count%2 == 1):
                        if(cur_right<len(counters)):
                            if(counters[cur_right][0] < counters[cur_right][1]):
                                benches[x][y][0] = sheets[cur_right][counters[cur_right][0]]
                                counters[cur_right][0] += 1

                        elif(cur_left<len(counters)):
                            if(counters[cur_left][0] < counters[cur_left][1]):
                                benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                                counters[cur_left][0] += 1        
                        
                        count += 1                     
        rooms.append(benches)
    

    for i in range(len(rooms)):
        for j in range(len(rooms[i])):
            if(j%2==1): 
                rooms[i][j].reverse() 
    for i in range(len(rooms)):
        room = transpose(rooms[i], [])
        rooms[i] = room
    
    result = {}
    i = 0
    while(i < len(selected_rooms)):
        result[selected_rooms[i]] = rooms[i]
        i += 1
    i = 0
    while(i < len(selected_halls)):
        result[selected_halls[i]] = rooms[i+len(selected_rooms)]
        i += 1


    
    return result


