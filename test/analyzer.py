import json 
import MeCab
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
import numpy as np
import pandas
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits import mplot3d
from random import randint
import statistics
from collections import Counter


from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']


read = {}
	
prefs = {}
#with open ("prefecs.json", "r") as f:
#	prefs = json.load(f)

with open("data-mod.json", "r") as fread:
	read = json.load(fread)

def get_nouns (text):
	tagger = MeCab.Tagger()
	words = []
	
	for c in tagger.parse(text).splitlines()[:-1]:
		if len(c.split('\t')) < 2:
			continue
		surface, feature = c.split('\t')
		pos = feature.split(',')[0]
		if pos == '名詞':
			words.append(surface)
	return ' '.join(words)


def bio(dimensions, theme, party="all", regions="日本", howmany=5, save=False): 
	# mostly using 2d #howmnay >>> how many clusters 5 is the most stable 
	biolist =[]
	list_select = []
	plt.figure(figsize = (8, 4.8))
	########################################################################
	if party == "all":
		pass
	else:
		for giin in read:
			if giin["name"]  == "stats":
				continue
			
			if giin["party"] == party:
				list_select.append(giin)

	#############################################################################################
	if regions == "日本":
		pass
	else:
		for giin in read:
			if giin["name"]  == "stats":
				continue
			
			if giin["region"] == regions:
				list_select.append(giin)
	
	if regions == "日本" and party == "all":
		list_select = read
	############ dimensions ################# 2D + consequtive balanced ###############################
	
	if dimensions == 2: 
		X = []
		Y = []
		Z = []
		for giin in list_select:
			if len(giin[theme]) < 1:
				continue
			if giin["name"]  == "stats":
				continue
			biolist.append(get_nouns(" ".join(giin[theme])))
			Z.append(giin["consequtive_balanced"])

		if len(biolist) < 20:
			print ("---passing--- theme >>> ", theme, "   party >>> ", party, "   regions >>>", regions, "   n = ", len(biolist))
			ax = plt.axes(projection="3d")
			ax.set_xlabel('X: k means 2d')
			ax.set_ylabel('Y: k means 2d')
			ax.set_zlabel('Z: consequtive election adjusted by age  \n the higher the successful as a politician')
			ax.text2D(-0.14, 0.95+(1/25),"not enough sample size", color="red",transform=ax.transAxes, size=9)
			ax.text2D(0.5, -0.1, "bio-{}dimensions-{}-{}-{}.png".format(dimensions, theme, regions, party), 
			color="black",transform=ax.transAxes, size=9)	

			if save==True:
				plt.savefig('plot-images/bio/EMPTY-bio-{}dimensions-{}-{}-{}.png'.format(dimensions, theme, regions, party))
			else:
				plt.show()
			plt.close()
			return
		else:
			print ("theme >>> ", theme, "party >>> ", party, "   regions >>>", regions, "   n = ", len(biolist))

		nparray = np.array (biolist)
		cv = CountVectorizer()
		bags = cv.fit_transform(nparray)
		tfidf=TfidfTransformer(norm='l2', sublinear_tf=True).fit_transform(bags)
		km_model = KMeans(n_clusters=howmany, init='k-means++')
		km_model.fit_transform(tfidf)
		lsa = TruncatedSVD(2)
		compressed_text_list = lsa.fit_transform(tfidf)

		for x, y in compressed_text_list:
			X.append(x)
			Y.append(y)

		clus_list = {"avg":[]}
		for i in range (howmany):
			agecon_avg = []
			clus_list[i] = []
			for a in range(len(biolist)):
				if km_model.labels_[a] == i:
					clus_list[i].append(biolist[a])
					agecon_avg.append(Z[a])
			clus_list["avg"].append(statistics.mean(agecon_avg))	
	
		ax = plt.axes(projection="3d")
		sc = ax.scatter3D(X, Y, Z, c=km_model.labels_, cmap = "Accent")

		ax.set_xlabel('X: k means 2d')
		ax.set_ylabel('Y: k means 2d')
		ax.set_zlabel('Z: consequtive election adjusted by age  \n the higher the successful as a politician')

		for a in clus_list:
			if a == "avg":
				continue
			ctr = Counter(clus_list[a])
			#print (a)
			#print (clus_list[a])

			if len(clus_list[a]) < 3:
				label1 = clus_list[a][0]
				label2 = "null"
				label3 = "null"
			elif len (ctr.most_common(3)) < 3:
				label1 = clus_list[a][0] 
				label2 = clus_list[a][1] 
				label3 = "null"

			else:
				label1 = ctr.most_common(3)[0][0] 
				label2 = ctr.most_common(3)[1][0] 
				label3 = ctr.most_common(3)[2][0] 

			ax.text2D(-0.14, 0.95+(a/25),
			"group {},  n={}, avg(cons.) = {} | 1<{}>,  2<{}>, 3<{}> etc.".format(
			a, len(clus_list[a]), float(str(clus_list["avg"][a])[:6]), label1, label2, label3,), 
			color=sc.get_facecolors()[biolist.index(clus_list[a][0])].tolist(),
			transform=ax.transAxes, size=6)
			ax.text2D(0.5, -0.1, "bio-{}dimensions-{}-{}-{}.png".format(dimensions, theme, regions, party), 
			color="black",transform=ax.transAxes, size=9)	

		

#############################################################################################################

	elif dimensions == 3: #not using 
	
		for giin in read:
			if len(giin[theme]) < 1:
				continue
			if giin["name"]  == "stats":
				continue
			biolist.append(get_nouns(" ".join(giin[theme])))

		nparray = np.array (biolist)
		cv = CountVectorizer()
		bags = cv.fit_transform(nparray)
		tfidf=TfidfTransformer(norm='l2', sublinear_tf=True).fit_transform(bags)
		km_model = KMeans(n_clusters=howmany, init='k-means++')
		km_model.fit_transform(tfidf)
		lsa = TruncatedSVD(3)
		compressed_text_list = lsa.fit_transform(tfidf)		

		X = []
		Y = []
		Z = []
	
		for x, y, z in compressed_text_list:
			X.append(x)
			Y.append(y)
			Z.append(z)
		
		clus_list = {}

		for i in range (howmany):
			clus_list[i] = []
			for a in range(len(biolist)):
				if km_model.labels_[a] == i:
					clus_list[i].append(biolist[a])

		for a in clus_list:
			print (a)
			print (clus_list[a])
			
		ax = plt.axes(projection="3d")
		sc = ax.scatter3D(X, Y, Z, c=km_model.labels_, cmap = "Paired")
		
		for a in clus_list:
			ax.text2D(0.01, 0.95+(a/25),
			"group {},  n={}   1<{}>,  2<{}>, 3<{}>".format(a, len(clus_list[a]),  #n=
			clus_list[a][randint(0, len(clus_list[a])-1)],  #1
			clus_list[a][randint(0, len(clus_list[a])-1)],  #2
			clus_list[a][randint(0, len(clus_list[a])-1)]), #3
			color=sc.get_facecolors()[biolist.index(clus_list[a][0])].tolist(),
			transform=ax.transAxes, size=7)
		ax.text2D(0.5, -0.1, "bio-{}dimensions-{}-{}-{}.png".format(dimensions, theme, regions, party), 
			color="black",transform=ax.transAxes, size=9)
		#ax.scatter3D(X_cent, Y_cent, Z_cent, c="red", marker = "+")
		ax.text2D(0.5, -0.1, "bio-{}dimensions-{}-{}-{}.png".format(dimensions, theme, regions, party), 
			color="black",transform=ax.transAxes, size=9)	


	if save==True:
		plt.savefig('plot-images/bio/bio-{}dimensions-{}-{}-{}.png'.format(dimensions, theme, regions, party), dpi=200)
	else:
		plt.show()
	plt.close()

def bioconseq(): # not used
	biolist =[]
	howmany = 10
	for giin in read:
		if len(giin["previously"]) < 1:
			continue
		biolist.append(get_nouns(" ".join(giin["previously"])))
	######################################################
	nparray = np.array (biolist)
	cv = CountVectorizer()
	bags = cv.fit_transform(nparray)
	tfidf=TfidfTransformer(norm='l2', sublinear_tf=True).fit_transform(bags)
	km_model = KMeans(n_clusters=howmany, init='k-means++')
	km_model.fit_transform(tfidf)
	lsa2 = TruncatedSVD(1)
	compressed_text_list = lsa2.fit_transform(tfidf)
	
	X = []
	Y = []

	for x in range(len(compressed_text_list)):
		X.append(compressed_text_list[x])
		Y.append(read[x]["consequtive_balanced"])
	
	plt.scatter(X, Y)	
	plt.show()

def prefectures():
	for giin in read:
		if giin["name"]  == "stats":
			continue
		print (giin["district"])
		if "比" in giin["district"]: 
			giin["region"] = "比例" 
		else:
			for pref in prefs:
				if pref["pref"] in giin["district"]:
					giin["region"] = pref["region"]


def agecons():
	for giin in read:
		if giin["name"]  == "stats":
			continue
		if "参" in giin["consequtive"]:
			i = 0
			for cha in giin["consequtive"]:
				try:
					i = i + int(cha)
				except ValueError:
					print (cha, " is not integer")
			giin["consequtive"] = i

		print (giin["name"])
		if len (giin["age"]) < 1:	
			giin["consequtive_balanced"] = 0
			continue
		toshi = giin["age"][1].split("（")[1].replace("）", "").replace("歳", "")
		toshi = toshi.split(r"[")[0]
		giin["toshi"] = int(toshi)
		giin["consequtive_balanced"] = int(giin["consequtive"])/(giin["toshi"]-25) # have to be 25 to run for the seat 

	
def education():
	for giin in read:
		if giin["name"]  == "stats":
			continue
		giin["postgrad"] = False
		giin["poli_edu"] = False

		for edu in giin["education"]:
			if "大学院" in edu or "修士" in edu or "博士" in edu:
				giin["postgrad"] = True
			
			if "政治" in edu or "政策" in edu:
				giin["poli_edu"] = True
			
def family():
	for giin in read:
		if giin["name"]  == "stats":
			continue
		giin["family_politician"] = False
		giin["family_business"] = False
		for fam in giin["family"]:
			if "議員" in fam or "政治家" in fam or "大臣" in fam:
				giin["family_politician"] = True
			if "社長" in fam or "経営者" in fam:
				giin["family_business"] = True

def previous():
	for giin in read:
		if giin["name"]  == "stats":
			continue
		
		giin["secretary_experi"] = False
		giin["civil_servant"] = False
		giin["journalist"] = False

		for previously in giin["previously"]:
			if "秘書" in previously:
				giin["secretary_experi"] = True
			if "省" in previously or "庁" in previously or "公務員" in previously:
				giin["civil_servant"] = True
			if "記者" in previously or "新聞" in previously:
				giin["journalist"] = True

def simpleplot ():
	X = []
	Y = []
	for giin in read:
		if giin["name"]  == "stats":
			continue
		if giin["postgrad"]  == 0:
			continue
		
		#X.append(giin["poli_edu"])
		X.append(giin["civil_servant"])

		"""
		if giin["postgrad"] == True:
			X.append(1)
		else:
			X.append(0)
		"""
		Y.append(giin["consequtive_balanced"])
		
	res = np.corrcoef(X, Y)
	if res.tolist()[0][1] == res.tolist()[0][1]:
		print (res.tolist()[0][1])
	plt.scatter(X, Y)
	plt.show()
	
		
def multidiment():
	howmany = 4
	sets = []
	for giin in read:
		print (giin["name"])
		if giin["name"]  == "stats":
			continue
		sets.append([
		giin["postgrad"],
		giin["poli_edu"],
		giin["family_politician"],
		giin["family_business"],
		giin["secretary_experi"],
		giin["civil_servant"],
		#giin["journalist"], 
		giin["consequtive_balanced"]])
	
	km_model = KMeans(n_clusters=howmany)
	km_model.fit_transform(sets)
	lsa2 = TruncatedSVD(3)
	compressed_text_list = lsa2.fit_transform(sets)
	compressed_center_list = lsa2.fit_transform(km_model.cluster_centers_)
	
	X = []
	Y = []
	Z = []
	X_cent = []
	Y_cent = []
	Z_cent = []

	for x, y, z in compressed_text_list:
		X.append(x)
		Y.append(y)
		Z.append(z)
	for x, y, z in compressed_center_list:
		X_cent.append(x)
		Y_cent.append(y)
		Z_cent.append(z)

	ax = plt.axes(projection="3d")

	"""
	z_line = np.linspace(0, 15, 1000)
	x_line = np.cos(z_line)
	y_line = np.sin(z_line)
	ax.plot3D(x_line, y_line, z_line, 'gray')
	"""
	
	ax.scatter3D(X, Y, Z, c=km_model.labels_)
	ax.scatter3D(X_cent, Y_cent, Z_cent, c="r", marker = "+")

	plt.show()


def main ():
	"""agecons()
	education ()
	family ()
	previous ()
	with open ("data-mod.json", "w") as f:
		json.dump(read, f, indent=2, ensure_ascii=False)
	"""
	#simpleplot()

	#bio(2, theme="education", regions="中部", party="all", save=True)

	
	for region in ["関東", "近畿", "東北", "九州", "四国", "比例", "中部", "北海道"]:
		for theme in ["education", "previously", "family"]:
			bio(2, theme= theme, party="all", regions=region, save=True)
			

	for party in ['自民', '共産', '維新', '公明', '希望', '立国社', '無']:
		for theme in ["education", "previously", "family"]:
			bio(2, theme=theme, party=party, regions="日本", save=True)
			
	for theme in ["education", "previously", "family"]:
		bio(2, theme=theme, party="all", regions="日本", save=True)
	
	
	#### regions = "関東" or "近畿" or "東北" or "九州" or "四国" or "比例" or "中部" or "北海道" default is "日本" 
	#### party = '自民', '共産', '維新', '公明', '希望', '立国社', '無'
	#### theem = "education", "previously", "family"
	
	#bioconseq()
	#multidiment()
	#prefectures()


	#with open ("data-mod.json", "w") as fwrite:
	#json.dump(read, fwrite, indent=2, ensure_ascii=False)



if __name__ == "__main__":
	main()

