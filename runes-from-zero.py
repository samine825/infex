.p from math import *
from PIL import Image, ImageDraw, ImageFont

d =100
L = 1000
polygons = [[0,0]]*20

# 1
polygons[0] = [0, 0]
polygons[3] = [L, 0]
polygons[16] = [0, L]
polygons[19] = [L, L]

# 2
gipotenuza = (L/2)*sqrt(2)
katet = d/2
ugol = pi/2-acos(katet/gipotenuza)+pi/4
iskomoe=L - (L/tan(ugol))

polygons[1] = [iskomoe, 0]
polygons[2] = [L - iskomoe, 0]
polygons[17] = [iskomoe, L]
polygons[18] = [L - iskomoe, L]

#3
hzkaknazvat = d/tan(ugol)

polygons[4] = [hzkaknazvat, d]
polygons[7] = [L - hzkaknazvat, d]
polygons[12] = [hzkaknazvat, L-d]
polygons[15] = [L - hzkaknazvat, L-d]

#4
polygons[5] = [hzkaknazvat + iskomoe, d]
polygons[6] = [L - hzkaknazvat - iskomoe, d]
polygons[13] = [hzkaknazvat + iskomoe, L-d]
polygons[14] = [L - hzkaknazvat - iskomoe, L-d]

#5
triangle2 = (L/2)/tan(ugol)
polygons[9] = [triangle2, L/2]
polygons[10] = [L - triangle2, L/2]

#6
triangle3 = (L/2)/tan(pi/2 - ugol)
polygons[8] = [L/2, L - triangle3]
polygons[11] = [L/2, triangle3]


print(polygons)

















map = {
0: [0,1,5,4],
1: [1,2,6,5],
2: [2,3,7,6],
3: [4,5,8,9],
4: [6,7,10,8],
5: [8,10,11,9],
6: [9,11,13,12],
7: [10,15,14,11], 
8: [12,13,17,16],
9: [13,14,18,17],
10: [14,15,19,18]
}
elements4num = {
0:[0,1,2],
1:[5,3,0],
2:[2,4,5],
3:[8,6,5],
4:[5,7,10],
5:[10,9,8]
}
maplines = {}
# уникальные линии
def unique(line: list):
    vstrechaitsa = 0
    for i in maplines.values():
        if line in i or list(reversed(line)) in i:
            #print(line, " ", list(reversed(line)), " ", i)
            if vstrechaitsa > 0:
                return False
            else: vstrechaitsa+=1
    return True
# находится ли точка в активном элементе
def point_in_active(point):
    for idx, points in map.items():
        if active_elements[idx] and point in points:
            return True
    return False
# магнитная цепочка
def findidx(point):
    resultus.remove([point])
    for num, i in enumerate(resultus):
        for j in i:
            if j == point:
                return num
    return -1

def paravozik(idx, start):
    if not resultus:
        return []
    #print(resultus)
    resultus[idx].remove(start)
    remainder = resultus[idx][0]
    finded_idx = findidx(remainder)
    if finded_idx == -1:
        return [start]
    return [start] + paravozik(finded_idx, remainder)
for i in range(64):
	number = f"{bin(23)[2:]:0>6}"
	numlist = [int(i) for i in list(number)]
	# линии
	for i, k in map.items():
	    maplines[i] = []
	    for linenum in range(len(k)):
	        maplines[i].append([k[linenum], k[(linenum+1)%4]])
	# линии с определением, уникально чи н
	maplinescategorized = {}
	for i, k in map.items():
	    maplinescategorized[i] = {}
	    maplinescategorized[i]["u"] = []
	    maplinescategorized[i]["n"] = []
	    for linenum in range(len(k)):
	        maplinescategorized[i]["u" if unique([k[linenum], k[(linenum+1)%4]]) else "n"].append([k[linenum], k[(linenum+1)%4]])
	

	active_elements = {i:False for i in range(0, 11)}
	
	#находем активные элементы (6 -> 11)
	for idx, val in enumerate(numlist):
	    elements = elements4num[idx]
	    if val:
	        for i in elements:
	            active_elements[i] = True
	
	# список активных линий
	resultus = []
	for idx, active in active_elements.items():
	    #print(maplinescategorized[idx])
	    if active:
	        resultus += maplinescategorized[idx]["u"]
	    else:
	        for i in maplinescategorized[idx]["n"]:
	            for j in i:
	                if point_in_active(j):
	                    if i not in resultus:
	                        resultus.append(i)
	
	#print(resultus)
	
		
	resulted_paravozik = []
	while resultus:
	    subparavoz = paravozik(0, resultus[0][0])
	    if len(subparavoz) == 3:
	        subparavoz.reverse()
	    resulted_paravozik.append(subparavoz)
	
	
	svg_start = f'<svg width="{1000}" height="{1000}" viewBox="0 0 {1000} {1000}" xmlns="http://www.w3.org/2000/svg">\n  <path d="'
	#M 0,0 L 200,0 L 200,200 L 0,200 Z M 50,50 L 50,150 L 150,150 L 150,50 Z
	svg_end = '" />\n</svg>'
	
	
	svg = ""
	for i in resulted_paravozik:
	    for num, j in enumerate(i):
	        if num == 0:
	            svg += "M "
	        else:
	            svg += "L "
	        svg += f"{polygons[j][0]},{polygons[j][1]} "
	    svg += "Z "
	svg = svg_start + svg + svg_end
	print(svg)
	with open(f"/storage/emulated/0/{number}.svg", "w", encoding="utf-8") as file:
	    file.write(svg)
	
	
	# рендер
	margin = 80
	img_size = L + margin * 2
	img = Image.new('RGB', (img_size, img_size), 'white')
	draw = ImageDraw.Draw(img)
	for i, (x, y) in enumerate(polygons):
	    px = x + margin
	    py = y + margin
	    radius = 6
	    draw.ellipse(
	        (px - radius, py - radius, px + radius, py + radius),
	        fill='red', outline='black', width=1
	    )   
	    draw.text((px + 8, py - 10), str(i), fill='black')
	    coord_text = f'({int(x)},{int(y)})'
	    draw.text((px + 8, py + 8), coord_text, fill='blue')
	
	for i in resultus:
	    a = polygons[i[0]]
	    b = polygons[i[1]]
	    a = [iii + margin for iii in a]
	    b = [iii + margin for iii in b]
	    draw.line([tuple(a), tuple(b)], fill ="red", width = 10)
	
	print_photo(img)