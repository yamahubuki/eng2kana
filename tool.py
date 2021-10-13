



class UnregisteredException(Exception):
	def __init__(self,first,second,englishWord):
		self.first = first
		self.second = second
		self.englishWord = englishWord

	def __str__(self):
		return "Unknown pattern Error  "+self.first+"+"+self.second+" in "+self.englishWord


def parseFile(input,output):
	ok=0
	ng=0
	errorDic = {}
	for line in input:
		try:
			english,kana = parseLine(line.split(" "))
			output.write(english+"\t"+kana+"\n")
			ok+=1
		except UnregisteredException as e:
			ng+=1
			key = e.first+" "+e.second
			if key in errorDic:
				errorDic[key].append(e.englishWord)
			else:
				errorDic[key]=[e.englishWord,]
		if ok+ng >= 500000:
			break
	errorDic2 = sorted(errorDic.items(), key=lambda x:len(x[1]))
	if errorDic2:
		print(errorDic2[len(errorDic2)-1])

	print("OK:"+str(ok)+" "+str((ok/(ok+ng))*100)+"%")
	print("NG:"+str(ng))

def parseLine(data):
	#print()
	#print(data)
	englishWord = data[0]
	# [2]は必ず空文字なので無視
	first = data[2]
	if len(data) > 3:
		second = data[3]
	else:
		second = None
	next = 3
	if len(data) > (next+1):
		third = data[next+1]
	else:
		third = None

	kana = ""
	while(next <= len(data)):
		ret,usedCount = getNextKana(first,second,third)
		kana += ret
		if usedCount == -1:
			if second:
				raise UnregisteredException(first,second,englishWord)
			else:
				raise UnregisteredException(first,"",englishWord)
		elif usedCount == 0:
			break
		else:
			next += (usedCount - 1)
			if len(data) > next:
				first = data[next]
			else:
				break
			next += 1
			if len(data) > next:
				second = data[next]
			else:
				second = None
			if len(data) > (next+1):
				third = data[next+1]
			else:
				third = None

	if kana.startswith("ッ"):
		kana = kana[1:]

	#print(englishWord+" "+kana)
	return englishWord,kana


def getNextKana(first,second,third):
		#アクセントとワードを分離
		accent = [-1, -1, -1]
		if first[-1] == "\n":
			first = first[0:-1]
		if first[-1] in ("0", "1", "2"):
			accent[0] = first[-1]
			first = first[0:-1]
		if second is not None:
			if second[-1] == "\n":
				second = second[0:-1]
			if second[-1] in ("0","1","2"):
				accent[1] = second[-1]
				second = second[0:-1]
		if third is not None:
			if third[-1] == "\n":
				third = third[0:-1]
			if third[-1] in ("0","1","2"):
				accent[2] = third[-1]
				third = third[0:-1]

		dic = {
			"AA":{
					"L": ("ア", 1),
					("K", "P"): ("オ", 1),
				},
			"AE":{
					"K": ("ア", 1),
				},
			"AO":{
					"R":("オー", 2),
				},
			"AH":{
					("L"): ("オ", 1),
					("JH", "N"): ("ア", 1),
				},
			"B":{
					(None, "R"): ("ブ", 1),
					"AH": ("バ", 2),
					"AE": ("バ", 2),
					"AO": {
							"R": ("ボー", 3),
						},
					"AY": {
							"AA":("バヤ", 3),	#HIRABAYASHI
							"*":("バイ", 2),	#bicycle keyboard
						},
					"IH": ("ビ", 2),
					("IY"): ("ビー", 2),	#zombie
				},
			"CH":{
					"AH": ("チャ", 2),
					"AY": ("チャイ", 2),
					"ER": ("チャー", 2),

				},
			"D":{
					(None, "G", "R"): ("ド", 1),
					("AH", "AO"): ("ド", 2),	#london
					"EH": ("デ", 2),
					"ER": ("ダー", 2),
					"IH": ("デ", 2),	#destroy
					"IY": ("ディー", 2),
					"UW": ("デュー", 2),
				},
			"DH":{
				"ER": ("ザー", 2),
				},
			"EY":{
					"N": ("エン", 2),
					"T": ("エイ", 1),
				},
			"ER":{
					"TH": ("アー", 1),	#EARTH
				},
			"F":{
					(None,"L", "R"): ("フ", 1),
					"AA": ("フォ", 2),
					"AO": ("フォ", 2),
					"AH": ("ファ", 2),
					"AY": ("ファイ", 2),
					"EY": ("フェイ", 2),
				},
			"G":{
					(None,"L", "R"): ("グ", 1),
					"AH": ("ゴ", 2),	#dragon
					"ER": ("ガー", 2),
					"EY": ("ゲー", 2),
					"IH": ("ギ", 2),
				},
			"HH":{
					"AA": ("ハ", 2),	#TAKAHASHI
					"AH": ("ハ", 2),	#UNDRED
					"ER": ("ハ", 2),	#HURRICANE
					"IH": ("ヒ", 2),
				},
			"IH":{
					(None,  "NG"): ("イ", 1),
					("K", "L"): ("エ", 1),	#electronic, economy
					"N": ("エン", 2),	#ENGAGEMENTS
				},
			"JH":{
					None: ("ッジ",1),
					"AA": ("ジョ", 2),
					"AH": ("ジャ", 2),
					"EH": ("ジェ", 2),
					"ER": ("ジャー", 2),
					"M": ("ジ", 1),		#ENGAGEMENTS
					"UW": ("ジュー", 2), 	#juice
				},
			"K":{
					(None, "D", "F", "W"): ("ック", 1),	#clock, breakfast
					"R": ("ク", 1),	#crystal
					"AA": ("カ", 2),
					"AO": ("コー", 2),
					"AH": ("カ", 2),
					("EH", "AE"): ("キャ", 2),	#character, scanner
					"IY": ("キー", 2),
					"OW": {
							"AA": ("コ", 2),
							"D": ("コー", 2),
							},
					("S", "SH", "T","L"): ("ク", 1),
					"UW": ("クー", 2),
					"Y":{
							"UW": ("キュー", 3),
						},
				},
			"L":{
					(None, "D", "F", "JH", "T"): ("ル", 1),
					"AA": ("ロ", 2),
					"AE": ("ラ", 2),	#laboratory
					"AH": ("レ", 2),	#knowledge
					"AW":{
							"ER": ("ラワー", 3),
							"*": ("ラウ", 2),
						},
					"EH": ("レ", 2),
					"ER": ("ラー", 2),
					"EY":("レー", 2),
					"IH": ("リ", 2),
					"IY": ("リー", 2),
					"Y": ("リ", 2),
				},
			"M":{
					(None, "Z"): ("ム", 1),
					"AA": ("モ", 2),	#TOMORROW
					("B", "P"): ("ン", 1),
					"AE": ("マ", 2),		#demand
					"AH": ("マ", 2),
					"IH": ("ミ", 2),
					"IY": ("ミー", 2),
				},
			"N":{
					(None, "D", "G", "S", "T", "TH"): ("ン", 1),
					"AA": ("ナ", 2),
					"AH": ("ナ", 2),
					"AY": ("ナイ", 2),
					"ER": {
							"AH": ("ナ", 3),
							"*": ("ナー", 2),	#未利用
						},
					"IH": ("ニ", 2),
					"IY": ("ニー", 2),
				},
			"NG":{
					None: ("ング", 1),
					"G": ("ング", 2),
				},
			"P":{
					(None, "T", "R"): ("プ", 1),
					"AA": ("ポ", 2),
					"AH": ("ピ", 2),
					"AY": ("パイ", 2),
					"R":{
						"AA": ("ロ", 3),
						},
					"UH": ("パ", 2),
					"Y": {
						"AH": ("ピュ", 3),
						"UW": ("ピュー", 3),
					}
				},
			"R":{
					None: ("ア", 1),	#underscore
					("AA"): ("ロ", 2),	#electronic
					("AE", "AH"): ("ラ", 2),
					"AY": ("ライ", 2),
					"EH": ("レ", 2),
					"EY": ("レー", 2),	#DEMONSTRATE
					"IH": ("リ", 2),	#character,crystal
					"IY": {
							None: ("リー", 2),
							"*": ("リ", 2),
						},
					"N": ("ー", 1),
					"OW":{
						None: ("ロー", 2),
						"*": ("ロ", 2),
						},
					"OY": ("ロイ", 2),

				},
			"S":{
					(None, "K", "T", "P"): ("ス", 1),
					"AH": ("サ", 2),
					"AY": ("サイ", 2),
					"EH": ("セ", 2),
					"IH": ("シ", 2),
					"IY": ("シー", 2),
				},
			"SH":{
					None: ("ッシュ", 1),
					"AH":{
							"N": ("ション", 3),
						},
					"IY": ("シ", 2),
				},
			"T":{
					(None, "R"): ("ト", 1),
					("AA", "AE", "AH"):{
							"R": ("ター", 3),
							"*": ("タ", 2),
						},
					"AH":{
							"D": ("テッド", 3),
							"*": ("ト", 2),
						},
					("AO"): ("トー", 2),
					"AY": ("タイ", 2),
					"EH": ("テ", 2),
					"ER":{
							("AY", "IH"): ("タライ", 3),
							"IY":("トリー", 3),
							"*": ("ター", 2),
						},
					("EY"): ("テイ", 2),
						"IY": ("ティー", 2),
					"IH": ("ティ", 2),
					"OW": ("トー", 2),
					"UW": ("ツー", 2),
					"S": ("ツ", 2),
				},
			"TH":{
					(None, "K"): ("ス", 1),
					"AA": ("ソ", 2),
					"AH": ("サ", 2),	#synthesizer
					"R": ("ス", 1),
				},
			"V":{
					None: ("ブ", 1),
					"AH": {
							"L":("バー", 3),
							"*":("ブ", 2),	#SEVEN
						},
					"AY": ("バイ", 2),
					"ER": ("バー", 2),	#未利用
					"IH": ("ビ", 2),
					"IY": ("ビー", 2),	#未利用
				},
			"W":{
					"AH": ("ワ", 2),
					"AO": ("ウォー", 2),
					"EH": ("ウェ", 2),
					"EY": ("エイ", 2),
					"ER": ("ワー", 2),
					"IY": ("ウィー", 2),	#we
				},
			"Y":{
				"UW": ("ユー", 2),
				},
			"Z":{
					(None, "D"): ("ズ", 1),
					"AA": ("ゾ", 2),
					"AH": ("ズ", 2),
					"ER": ("ザー", 2),
					"EY": ("ゼイ", 2),
					"IH": ("ジ", 2),
					"UW": ("ズー",2),
				},
			}
		for i in dic.keys():
			if i == first:
				#print("found:"+i)
				for j in dic[i].keys():
					if second == j or (type(j)==tuple and second in j):
						if type(dic[i][j]) == dict:
							#print("search3 from "+str(j))
							#print(third)
							for k in dic[i][j].keys():
								#print(k)
								if third == k or k == "*" or (type(k)==tuple and (third in k or "*" in k)):
									#print("found3:"+str(k))
									#print(dic[i][j])
									#print(dic[i][j][k])
									return dic[i][j][k]
						else:
							#print("found2:"+str(j))
							#print(dic[i][j])
							return dic[i][j]
		return("",-1)

if __name__ == "__main__":
	with open("cmudict-0.7b.txt", "r") as input:
#	with open("test.txt", "r") as input:
		with open("out.txt", "w") as output:
			parseFile(input, output)
