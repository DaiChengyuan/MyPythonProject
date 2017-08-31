# -- coding: utf-8 --

'''
[description]
	比对工号
[in]
	文件1：全量工号，约6w工号
	文件2：文件1的子集，约3w工号
	文件3：文件1的另一子集，约2w工号（文件2/3的工号有交集）
[out]
	文件4：文件1中包含的、文件2+文件3中均不包含的工号
'''

file = open("ids1", "r")
ids1 = file.readline().split(',')
file.close()

file = open("ids2", "r")
ids2 = file.readline().split(',')
file.close()

file = open("ids3", "r")
ids3 = file.readline().split(',')
file.close()

new_ids = []
for id in ids2:
	new_ids.append(id)
for id in ids3:
	new_ids.append(id)

file = open("ids4", "w")
for id in ids1:
	if id not in new_ids:
		file.write(id + ',')
file.close()

print "Hello World!"