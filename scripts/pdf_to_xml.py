import requests 

url = "http://pdfx.cs.man.ac.uk"

pdfs = ['/home/sajal/Wharton/resumes/American University', '/home/sajal/Wharton/resumes/Austin College 1',
'/home/sajal/Wharton/resumes/Austin College 2','/home/sajal/Wharton/resumes/Austin College 3','/home/sajal/Wharton/resumes/Bates College']

def pypdfx(filename):
  	fin = open(filename + '.pdf', 'rb')
	files = {'file': fin}
	try:
		print 'Sending', filename, 'to', url
		r = requests.post(url, files=files, headers={'Content-Type':'application/pdf'})
		print 'Got status code', r.status_code
	finally:
		fin.close()
	fout = open(filename + '.xml', 'w')
	fout.write(r.content)
	fout.close()
	print 'Written to', filename + '.xml'

if __name__ == '__main__':
  	for filename in pdfs:
		pypdfx(filename)