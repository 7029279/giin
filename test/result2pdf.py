from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import os.path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('TakaoMincho','TakaoMincho.ttf'))

state = 0

def bioimage(c, theme, region, party):
	global state
	path = 'plot-images/bio/{}bio-2dimensions-{}-{}-{}.png'.format("", theme, region, party)
	
	if os.path.exists(path):
		pass
	else:
		if os.path.exists('plot-images/bio/{}-bio-2dimensions-{}-{}-{}.png'.format("EMPTY", theme, region, party)):
			path = 'plot-images/bio/{}-bio-2dimensions-{}-{}-{}.png'.format("EMPTY", theme, region, party)
		else:
			print (path, "does not exist")
			return
		
	image =Image.open(path)
	print (path, "   size   ", image.size)
	page_width, page_height = c._pagesize

	if theme == "education":
		c.setFont('TakaoMincho', size=20)
		c.setFillColorRGB(0,0,0) 
		if state == 0:
			c.drawString(x=10, y=800, text="↓↓↓↓↓↓↓↓  地域：{}｜政党：{}  ↓↓↓↓↓↓↓↓".format(region, party))
		elif state == 1:
			c.drawString(x=10, y=400, text="↓↓↓↓↓↓↓↓  地域：{}｜政党：{}  ↓↓↓↓↓↓↓↓".format(region, party))
			
	if state == 0:
		c.drawImage(path, x=0, y=-165, width=page_width, preserveAspectRatio=True, anchor="n")
		state = 1
	elif state == 1:
		c.drawImage(path, x=0, y=-580, width=page_width, preserveAspectRatio=True, anchor="n")
		state = 0
		c.showPage()


def simpleimage(c, theme):
	global state
	path = 'plot-images/simpleplot/{}.png'.format(theme)
	if os.path.exists(path):
		pass
	else:
		print (path, "does not exist")
		return
		
	image =Image.open(path)
	print (path, "   size   ", image.size)
	page_width, page_height = c._pagesize
			
	if state == 0:
		c.drawImage(path, x=0, y=-165, width=page_width, preserveAspectRatio=True, anchor="n")
		state = 1
	elif state == 1:
		c.drawImage(path, x=0, y=-580, width=page_width, preserveAspectRatio=True, anchor="n")
		state = 0
		c.showPage()

def main():
	"""
	global state
	c = canvas.Canvas("bio.pdf")
	for region in ["日本", "関東", "近畿", "東北", "九州", "四国", "比例", "中部", "北海道"]:
		for party in [ "all", '自民', '共産', '維新', '公明', '希望', '立国社', '無']:
			for theme in ["education", "previously", "family"]:
				bioimage (c, theme=theme, region=region, party=party)
				
	#def putimage(c, empty, theme, regions, party, state): state = 0 for top and 1 for bottom   
	c.showPage()
	c.save()
	"""
	global state
	c = canvas.Canvas("simpleplot.pdf")
	 
	for theme in ["postgrad", "poli_edu", 
	"family_politician", "family_business", 
	"secretary_experi", "civil_servant", "journalist", "lawyer"]:
		simpleimage(c, theme)
	if state == 1:
		c.showPage()
	c.save()


if __name__ == "__main__":
	main()
