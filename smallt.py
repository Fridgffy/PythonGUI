from requests.packages.urllib3.exceptions import InsecureRequestWarning
import tkinter as tk
from tkinter import ttk
import subprocess
import pyperclip
import requests
import time
import sys
import paramiko
import csv
import re
import os
import base64
import html
import urllib


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Root():
	def __init__(self,window):
		self.window = window
		self.set_window()
		# Create notebook container
		self.notebook = ttk.Notebook(self.window)

		# Create tabscp
		self.tab_scp = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_scp,text="    SCP    ")
		self.create_scp()

		# Create tab memo
		self.tab_memo = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_memo,text="    Memo    ")
		self.create_memo()

		# Create tab Code
		self.tab_code = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_code,text="    Code    ")
		self.create_code()

		# Create tab subfile
		self.tab_subfile = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_subfile,text="    Subfile    ")
		self.create_subfile()

		# Create tab Extarct
		self.tab_extract = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_extract,text="    Extract    ")
		self.create_extract()


		# Create tab Websites: batch access to url
		self.tab_websites = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_websites,text="    Websites    ")
		self.create_websites()

		# create tab diff-finder
		self.tab_diff_finder = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_diff_finder,text="    Diff-Finder    ")
		self.create_diff_finder()

		self.notebook.pack()
	
	# 主面板大小设置
	def set_window(self):
		self.window.title('SmallTools')
		width = 930
		height = 700
		screenwidth = self.window.winfo_screenwidth()
		screenheight = self.window.winfo_screenheight()
		size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)

		self.window.geometry(size_geo)


	# 生成函数
	def create_button(self,tab,function,display,w=10):
		b = tk.Button(tab,text=display,command=function,font=('Consolas','12'),width=w)
		return b

	def create_text(self,tab,w,h):
		t = tk.Text(tab,width=w,height=h,font=('Consolas','12'))
		return t

	def create_label(self,tab,display,w=10,h=1):
		l = tk.Label(tab,text=display,width=w,height=h,font=('Consolas','12'))
		return l
	
	def create_entry(self,tab,w=15):
		e = tk.Entry(tab,show=None,width=w,font=('Consolas','12'))
		return e

	# result display
	def display_results(self,tab,result):
		l_result = tk.Label(tab, text=result,font=('Consolas','12'),width=100,height=5)
		l_result.grid(row=30,column=0,columnspan=10)

##### Create tab Websites
	def create_websites(self):
		def freplace():
			try:
				pattern = e_pattern.get()
				target = e_target.get()
				content = t_urls.get(0.0, tk.END)
				new_content = re.sub(pattern, target, content)
				t_urls.delete(0.0, tk.END)
				t_urls.insert('1.0', new_content)
				self.display_results(self.tab_websites, 'Replace completed')
			except Exception as e:
				self.display_results(self.tab_websites, str(e))
		
		def fclean():
			t_urls.delete(0.0,tk.END)
			self.display_results(self.tab_websites, '')

		def judgement():
			try:
				p1 = e_1.get()
				p2 = e_2.get()
				p3 = e_3.get()
				if p1 or p2 or p3:
					return True
				else:
					return False
			except Exception as e:
				self.display_results(self.tab_websites, str(e))

		def faccess():
			try:
				p1 = e_1.get()
				p2 = e_2.get()
				p3 = e_3.get()
				if judgement():
					urls = t_urls.get(0.0,tk.END)
					for url in urls.strip().split('\n'):
						try:
							if url:
								com = f'@start chrome {url.strip()}'
								if p1:
									com = com.replace('$1',p1)
								if p2:
									com = com.replace('$2',p2)
								if p3:
									com = com.replace('$3',p3)
								p = subprocess.Popen(com,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

								if p.stderr.read():
									self.display_results(self.tab_websites, p.stderr.read())
						except Exception as e:
							self.display_results(self.tab_websites, str(e))
				else:
					urls = t_urls.get(0.0,tk.END)
					for url in urls.strip().split('\n'):
						try:
							if url:
								com = f'@start chrome {url.strip()}'
								p = subprocess.Popen(com,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
						except Exception as e:
							self.display_results(self.tab_websites, str(e))
					if p.stderr.read():
						self.display_results(self.tab_websites, p.stderr.read())
					else:
						self.display_results(self.tab_websites, 'All URLs accessed')
			except Exception as e:
				self.display_results(self.tab_websites, str(e))

		def fentry_clean():
			try:
				e_1.delete(0, tk.END)
				e_2.delete(0, tk.END)
				e_3.delete(0, tk.END)
			except Exception as e:
				self.display_results(self.tab_websites, str(e))

		l_description = self.create_label(self.tab_websites,'Access to websites',w=65,h=1)
		l_description.grid(row=0,column=0,columnspan=7)

		# Entry1
		l_1 = self.create_label(self.tab_websites,'P1:',w=5,h=1)
		l_1.grid(row=1,column=0)
		e_1 = self.create_entry(self.tab_websites,w=20)
		e_1.grid(row=1,column=1)

		# Entry2
		l_2 = self.create_label(self.tab_websites,'P2:',w=5,h=1)
		l_2.grid(row=1,column=2)
		e_2 = self.create_entry(self.tab_websites,w=20)
		e_2.grid(row=1,column=3)

		# Entry3
		l_3 = self.create_label(self.tab_websites,'P3:',w=5,h=1)
		l_3.grid(row=1,column=4)
		e_3 = self.create_entry(self.tab_websites,w=20)
		e_3.grid(row=1,column=5)

		b_entry_clean = self.create_button(self.tab_websites, fentry_clean,' Clear ')
		b_entry_clean.grid(row=1,column=6)

		l_pattern = self.create_label(self.tab_websites,'Pattern:',w=10,h=1)
		l_pattern.grid(row=2,column=0,sticky=tk.E)
		e_pattern = self.create_entry(self.tab_websites,w=20)
		e_pattern.grid(row=2,column=1,sticky=tk.W)

		l_target = self.create_label(self.tab_websites,'Target:',w=10,h=1)
		l_target.grid(row=2,column=2,sticky=tk.E)
		e_target = self.create_entry(self.tab_websites,w=20)
		e_target.grid(row=2,column=3,sticky=tk.W)
		
		b_replace = self.create_button(self.tab_websites, freplace,' Replace ')
		b_replace.grid(row=2,column=6)
		

		t_urls = self.create_text(self.tab_websites,w=85,h=25)
		t_urls.grid(row=3, column=0,columnspan=6)
		t_urls.insert(0.0,'https://api.github.com/repos/$1/$2/releases/latest')

		b_access = self.create_button(self.tab_websites, faccess,' Access ')
		b_access.grid(row=3,column=6)

		b_clean = self.create_button(self.tab_websites,fclean,' Clean ')
		b_clean.grid(row=5,column=0,columnspan=7)

##### create tab memo
	def create_memo(self):
		try:
			file_path = './Memo'
			tmp_file = './tmp'
			if not os.path.exists(file_path):
				self.display_results(self.tab_memo, f'{file_path} not exists')

			with open(file_path, 'r', encoding='utf-8') as f:
				content = f.read()
			self.display_results(self.tab_memo, 'Read completed')
		except Exception as e:
			self.display_results(self.tab_memo, str(e))

		def freload():
			try:
				t_memo.delete("1.0", 'end')
				with open(file_path, 'r+', encoding='utf-8') as f2:
					content = f2.read()
					t_memo.insert("1.0", content.strip())
				self.display_results(self.tab_memo, 'Reload Successfully')
			except Exception as e:
				self.display_results(self.tab_memo, str(e))
		
		def fsave():
			try:
				text_content = t_memo.get(0.0, tk.END)
				with open(file_path, 'w', encoding='utf-8') as f:
					f.write(text_content)

				freload()
				self.display_results(self.tab_memo, 'Save Successfully')
			except Exception as e:
				self.display_results(self.tab_memo, str(e))

	
		def finsert():
			try:
				content = e_insert.get().strip().replace('\n','')
				if content:
					with open(file_path, 'a', encoding='utf-8') as f:
						f.write('\n')
						f.write(re.sub(r'^\s*$','', content.strip().replace('\n',''), flags=re.MULTILINE))
					e_insert.delete(0, tk.END)
					freload()
					self.display_results(self.tab_memo, 'Insert Successfully')
				else:
					pass
			except Exception as e:
				self.display_results(self.tab_memo, str(e))

		def fdelete():
			try:
				delete_content = e_delete.get()

				with open(file_path, 'r', encoding='utf-8') as f:
					with open(tmp_file, 'w', encoding='utf-8') as f_write:
						for line in f:
							if not re.search(r'^\s*$', line.strip()):
								if not line.strip() == delete_content.strip():
									f_write.write(line.strip())
									f_write.write('\n')
				os.replace(tmp_file, file_path)
				e_delete.delete(0, tk.END)
				freload()
				self.display_results(self.tab_memo, 'Delete Successfully')
			except Exception as e:
				self.display_results(self.tab_memo, str(e))

		

		l_description = self.create_label(self.tab_memo,'Read the contents of the file Memo',w=100,h=1)
		l_description.grid(row=0,column=0, columnspan=3)

		e_insert = self.create_entry(self.tab_memo,w=90)
		e_insert.grid(row=1, column=0)
		b_insert = self.create_button(self.tab_memo, finsert, ' Insert ')
		b_insert.grid(row=1, column=1)

		e_delete = self.create_entry(self.tab_memo,w=90)
		e_delete.grid(row=2, column=0)
		b_delete = self.create_button(self.tab_memo, fdelete, ' Delete ')
		b_delete.grid(row=2, column=1)

		t_memo = self.create_text(self.tab_memo,w=100,h=25)
		t_memo.grid(row=3, column=0, columnspan=3)
		t_memo.insert("1.0", content.strip())

		b_update = self.create_button(self.tab_memo, fsave, ' Save ')
		b_update.grid(row=4, column=0, sticky=tk.W)

		b_reload = self.create_button(self.tab_memo, freload, ' Reload ')
		b_reload.grid(row=4, column=1)

##### create tab Subfile
	def create_subfile(self):
		def f_httpx_csv():
			try:
				httpx_output = e_httpx_output.get()
				httpx_csv = e_httpx_csv.get()

				with open(httpx_output,'r', encoding='utf-8-sig') as output:
					with open(httpx_csv,'w+', newline='', encoding='utf-8-sig') as csv_file:
						write_obj = csv.writer(csv_file)

						for rows in output:
							if 'FAILED' not in rows and 'Current httpx version' not in rows and 'nohup:' not in rows and 'UI Dashboard is disabled' not in rows and 'projectdiscovery.io' not in rows:
								row_list = re.sub(r'\x1b\[\d{1,2}m','',rows).replace('\x1b[m]','').strip().split('[SUCCESS]')
								write_obj.writerow(row_list)


				self.display_results(self.tab_subfile, 'Filter completed')
			except Exception as e:
				self.display_results(self.tab_subfile, str(e))

		def falive_httpx():
			try:
				alive_file = e_read.get()
				alive_httpx = e_write.get()

				with open(alive_file, 'r', encoding='utf-8') as f_read:
					with open(alive_httpx, 'w+', encoding='utf-8') as f_write:
						for domain in f_read:
							http_ports = [80,81,3128,8000,8001,8080,8081,8088,8880,8888,8090,3128,9898,9900,9998,9999,18080,18081] # 18
							https_ports = [443,453,1443,4243,4443,8834,8443,9443,12443] # 9

							for port in http_ports:
								url = 'http://' + domain.strip() + ':' + str(port)
								f_write.write(url)
								f_write.write('\n')

							for port in https_ports:
								url = 'https://' + domain.strip() + ':' + str(port)
								f_write.write(url)
								f_write.write('\n')
						self.display_results(self.tab_subfile, 'Success, write in file alive_httpx')
			except Exception as e:
				self.display_results(self.tab_subfile, str(e))
		def fsecond():
			pass
		# process file data
		l_description = self.create_label(self.tab_subfile, 'Process dnsx output file <alive>: -> <alive_httpx>, add protocal and port',w=100,h=1)
		l_description.grid(row=0, column=0, columnspan=5)

		l_read = self.create_label(self.tab_subfile,'File_read:',w=15,h=1)
		l_read.grid(row=1,column=0)
		e_read = self.create_entry(self.tab_subfile, w=55)
		e_read.grid(row=1, column=1)
		e_read.insert(0,'C:\\Users\\DC\\Desktop\\alive')

		l_write = self.create_label(self.tab_subfile,'File_write:',w=15,h=1)
		l_write.grid(row=2,column=0)
		e_write = self.create_entry(self.tab_subfile, w=55)
		e_write.grid(row=2, column=1)
		e_write.insert(0, 'C:\\Users\\DC\\Desktop\\alive_httpx')

		b_alive_httpx = self.create_button(self.tab_subfile, falive_httpx, ' Process ')
		b_alive_httpx.grid(row=3, column=0, columnspan=2)
		# separator
		l_separator_label = tk.Label(self.tab_subfile,text='',font=('Consolas','12'),width=15,height=1)
		l_separator_label.grid(row=4,column=0, columnspan=10)	
		# rewrite httpx.csv
		l_description_rewrite = self.create_label(self.tab_subfile, 'Filter the successfully accessed domain from http_output: -> < httpx.csv >',w=100,h=1)
		l_description_rewrite.grid(row=5,column=0,columnspan=5)

		l_httpx_output = self.create_label(self.tab_subfile,'httpx_output:',w=15,h=1)
		l_httpx_output.grid(row=6,column=0)
		e_httpx_output = self.create_entry(self.tab_subfile, w=55)
		e_httpx_output.grid(row=6, column=1)
		e_httpx_output.insert(0,'C:\\Users\\DC\\Desktop\\httpx_output')

		l_httpx_csv = self.create_label(self.tab_subfile,'httpx_csv:',w=15,h=1)
		l_httpx_csv.grid(row=7,column=0)
		e_httpx_csv = self.create_entry(self.tab_subfile, w=55)
		e_httpx_csv.grid(row=7, column=1)
		e_httpx_csv.insert(0,'C:\\Users\\DC\\Desktop\\httpx.csv')

		b_httpx_csv = self.create_button(self.tab_subfile, f_httpx_csv, ' Filter ')
		b_httpx_csv.grid(row=8,column=0,columnspan=2)

##### create tab Extract
	def create_extract(self):
		def fclear():
			t_result.delete('1.0','end')
			self.display_results(self.tab_extract, '')
		def fextract_csv(file):
			try:
				result_list = []
				t_result.delete('1.0','end')
				pattern = e_getrows.get().strip()
				with open(file, 'r', encoding='utf-8') as f:
					reader_obj = csv.reader(f)
					for rows in reader_obj:
						row = '\t'.join(rows)
						if str(pattern) in row:
							result_list.append(row)
				t_result.insert('1.0', '\n'.join(result_list))
				self.display_results(self.tab_extract, 'Extracting completed')
			except Exception as e:
				self.display_results(self.tab_extract, str(e))
		def fdeduplication():
			try:
				old_content = t_result.get(0.0, tk.END)
				old_list = old_content.strip().split('\n')
				new_list = set(old_list)
				new_content = '\n'.join(new_list)

				t_result.delete(0.0, tk.END)
				t_result.insert(0.0, new_content)
				self.display_results(self.tab_extract, 'Deduplication completed')
			except Exception as e:
				self.display_results(self.tab_extract, str(e))
		def fextract_else(file):
			try:
				t_result.delete('1.0','end')
				pattern = e_pattern.get()
				reo = re.compile(pattern, re.I)
				with open(file, 'r', encoding='utf-8') as f:
					content = f.read()
					all_content = reo.findall(content)
					t_result.insert('1.0', '\n'.join(all_content))

				self.display_results(self.tab_extract, 'Extracting completed')
			except Exception as e:
				self.display_results(self.tab_extract, str(e))

		def fdeduplication_csv(file):
			try:
				result_list = []
				t_result.delete('1.0','end')
				pattern = e_getrows.get().strip()
				with open(file, 'r', encoding='utf-8') as f:
					reader_obj = csv.reader(f)
					for rows in reader_obj:
						row = '\t'.join(rows)
						if str(pattern) in row:
							result_list.append(row)
				t_result.insert('1.0', '\n'.join(set(result_list)))
				self.display_results(self.tab_extract, 'Extracting completed')
			except Exception as e:
				self.display_results(self.tab_extract, str(e))

		def fdeduplication_else(file):
			try:
				t_result.delete('1.0','end')
				pattern = e_pattern.get()
				file = e_file.get().replace('"','')
				reo = re.compile(pattern, re.I)
				with open(file, 'r', encoding='utf-8') as f:
					content = f.read()
					all_content = reo.findall(content)
					t_result.insert('1.0', '\n'.join(set(all_content)))
				self.display_results(self.tab_extract, 'Extracting completed')
			except Exception as e:
				self.display_results(self.tab_extract, str(e))
		
		def fdupli_extract():
			try:
				# determine if csv file
				file = e_file.get().replace('"','')
				name,ext = os.path.splitext(file)
				if str(ext) == '.csv':
					fdeduplication_csv(file)
				else:
					fdeduplication_else(file)
			except Exception as e:
				self.display_results(self.tab_extract, str(e))

		def fextract():
			try:
				# determine if csv file
				file = e_file.get().replace('"','')
				filename = os.path.split(file)[1]
				ext = os.path.splitext(filename)[1]
				if str(ext) == '.csv':
					fextract_csv(file)
				else:
					fextract_else(file)
			except Exception as e:
				self.display_results(self.tab_extract, str(e))
		def fsave():
			try:
				with open(r'./tmp', 'w', encoding='utf-8') as f:
					content = t_result.get(0.0, tk.END)
					f.write(content)
				self.display_results(self.tab_extract, r'Save to file ./tmp')
			except Exception as e:
				self.display_results(self.tab_extract, str(e))

		def fclear_getrows():
			e_getrows.delete(0, tk.END)
			self.display_results(self.tab_extract, '')
		def fclear_pattern():
			e_pattern.delete(0, tk.END)
			self.display_results(self.tab_extract, '')
		def fdefault_file():
			e_file.delete(0,tk.END)
			e_file.insert(0, r'./tmp')
		
		l_description = self.create_label(self.tab_extract, 'Extracting data from the file or csv using regular expressions', w=100, h=1)
		l_description.grid(row=0, column=0, columnspan=4)

		l_getrows = self.create_label(self.tab_extract, 'csv_Getrows:',w=15,h=1)
		l_getrows.grid(row=1,column=0)
		e_getrows = self.create_entry(self.tab_extract, w=65)
		e_getrows.grid(row=1, column=1)
		b_getrows = self.create_button(self.tab_extract, fclear_getrows, ' Clear ')
		b_getrows.grid(row=1, column=2)

		l_pattern = self.create_label(self.tab_extract, 'text_Pattern:',w=15,h=1)
		l_pattern.grid(row=2, column=0)
		e_pattern = self.create_entry(self.tab_extract, w=65)
		e_pattern.grid(row=2, column=1)
		b_pattern = self.create_button(self.tab_extract, fclear_pattern, ' Clear ')
		b_pattern.grid(row=2, column=2)

		l_file = self.create_label(self.tab_extract,'File:',w=15,h=1)
		l_file.grid(row=3, column=0)
		e_file = self.create_entry(self.tab_extract, w=65)
		e_file.grid(row=3, column=1)
		e_file.insert(0, r'./tmp')
		b_file = self.create_button(self.tab_extract, fdefault_file, ' Default ')
		b_file.grid(row=3, column=2)

		b_extract = self.create_button(self.tab_extract, fextract, ' Extract ')
		b_extract.grid(row=4, column=1, sticky=tk.E)

		# custom button 
		b_dedupli_extract = tk.Button(self.tab_extract, text='Dedupli-extract',command=fdupli_extract,font=('Consolas','12'),width=15)
		b_dedupli_extract.grid(row=4,column=1,sticky=tk.W)

		t_result = self.create_text(self.tab_extract,w=80,h=20)
		t_result.grid(row=5, column=0, columnspan=4)

		b_clear = self.create_button(self.tab_extract, fclear, ' Clear ')
		b_clear.grid(row=6, column=0, sticky=tk.W)

		b_deduplication = tk.Button(self.tab_extract, text='Deduplication',command=fdeduplication,font=('Consolas','12'),width=15)
		b_deduplication.grid(row=6,column=1)

		b_save = tk.Button(self.tab_extract,text=' Save->./tmp ',command=fsave,font=('Consolas','12'),width=15)
		b_save.grid(row=6, column=2)
		
##### create tab Diff-finder
	def create_diff_finder(self):
		def fa_clear():
			t_a.delete(0.0, tk.END)
			self.display_results(self.tab_diff_finder, '')
		def fb_clear():
			t_b.delete(0.0, tk.END)
			self.display_results(self.tab_diff_finder, '')
		def fsame_clear():
			t_same.delete(0.0, tk.END)
			self.display_results(self.tab_diff_finder, '')
		# delete same item from t_a
		def fa_delete():
			a_content = t_a.get(0.0,tk.END)
			same_content = t_same.get(0.0, tk.END)
			a_list = a_content.strip().split('\n')
			same_list = same_content.strip().split('\n')
			new_list = [item for item in a_list if item not in same_list]
			new_content = '\n'.join(new_list)
			t_a.delete(0.0, tk.END)
			t_a.insert(0.0, new_content)

		# delete same item from t_b
		def fb_delete():
			b_content = t_b.get(0.0,tk.END)
			same_content = t_same.get(0.0, tk.END)
			b_list = b_content.strip().split('\n')
			same_list = same_content.strip().split('\n')
			new_list = [item for item in b_list if item not in same_list]
			new_content = '\n'.join(new_list)
			t_b.delete(0.0, tk.END)
			t_b.insert(0.0, new_content)


		def ffind():
			a_content = t_a.get(0.0,tk.END)
			b_content = t_b.get(0.0, tk.END)
			a_list = a_content.strip().split('\n')
			b_list = b_content.strip().split('\n')
			same_list = set(a_list).intersection(b_list)
			t_same.delete(0.0, tk.END)
			t_same.insert(0.0, '\n'.join(same_list))

		def fa_read():
			afile = e_a_read.get().strip().replace('"', '')
			with open(afile, 'r', encoding='utf-8') as f:
				content = f.read()
				t_a.delete(0.0, tk.END)
				t_a.insert(0.0, content)

		def fb_read():
			bfile = e_b_read.get().strip().replace('"', '')
			with open(bfile, 'r', encoding='utf-8') as f:
				content = f.read()
				t_b.delete(0.0, tk.END)
				t_b.insert(0.0, content)
		l_description = self.create_label(self.tab_diff_finder, 'Find the differences between A and B, and delete them', w=100, h=1)
		l_description.grid(row=0, column=0, columnspan=3)
		l_a = self.create_label(self.tab_diff_finder, 'A',w=5,h=1)
		l_a.grid(row=1, column=0)
		l_same = self.create_label(self.tab_diff_finder, 'Same',w=5,h=1)
		l_same.grid(row=1, column=1)
		l_b = self.create_label(self.tab_diff_finder, 'B',w=5,h=1)
		l_b.grid(row=1, column=2)

		t_a = self.create_text(self.tab_diff_finder,w=30,h=23)
		t_a.grid(row=2, column=0)
		t_same = self.create_text(self.tab_diff_finder,w=30,h=23)
		t_same.grid(row=2, column=1)
		t_b = self.create_text(self.tab_diff_finder,w=30,h=23)
		t_b.grid(row=2, column=2)

		e_a_read = self.create_entry(self.tab_diff_finder, w=28)
		e_a_read.grid(row=3, column=0)
		b_a_read = tk.Button(self.tab_diff_finder, text='Read',command=fa_read,font=('Consolas','12'),width=5)
		b_a_read.grid(row=3, column=0, sticky=tk.E)

		e_b_read = self.create_entry(self.tab_diff_finder, w=28)
		e_b_read.grid(row=3, column=2)
		b_b_read = tk.Button(self.tab_diff_finder, text='Read',command=fb_read,font=('Consolas','12'),width=5)
		b_b_read.grid(row=3, column=2, sticky=tk.W)

		b_same_clear = self.create_button(self.tab_diff_finder, fsame_clear, ' Clear ')
		b_same_clear.grid(row=3, column=1)
		b_a_clear = self.create_button(self.tab_diff_finder, fa_clear, ' Clear ')
		b_a_clear.grid(row=4, column=0,sticky=tk.W)

		b_a_delete = self.create_button(self.tab_diff_finder, fa_delete, ' Del-same ')
		b_a_delete.grid(row=4, column=0, sticky=tk.E)

		b_find = self.create_button(self.tab_diff_finder, ffind, ' Find ')
		b_find.grid(row=4, column=1)

		b_b_clear = self.create_button(self.tab_diff_finder, fb_clear, ' Clear ')
		b_b_clear.grid(row=4, column=2, sticky=tk.E)

		b_b_delete = self.create_button(self.tab_diff_finder, fb_delete, ' Del-same ')
		b_b_delete.grid(row=4, column=2, sticky=tk.W)

##### Create tab Code
	def create_code(self):
		def finput_clean():
			t_input.delete('1.0','end')
			self.display_results(self.tab_code, '')
		def foutput_clean():
			t_output.delete(0.0, tk.END)
			self.display_results(self.tab_code, '')
		def fbase64en():
			try:
				in_content = t_input.get(0.0, tk.END)
				result = base64.b64encode(in_content.strip().encode('utf-8'))
				t_output.delete(0.0, tk.END)
				t_output.insert(0.0, result)
				self.display_results(self.tab_code, 'base64 encode completed')
			except Exception as e:
				self.display_results(self.tab_code, str(e))
		def fbase64de():
			try:
				in_content = t_input.get(0.0, tk.END)
				result = base64.b64decode(in_content.strip().encode('utf-8'))
				t_output.delete(0.0, tk.END)
				t_output.insert(0.0, result)
				self.display_results(self.tab_code, 'base64 decode completed')
			except Exception as e:
				self.display_results(self.tab_code, str(e))
		def fbase64_url_en():
			try:
				in_content = t_input.get(0.0, tk.END)
				result = base64.urlsafe_b64encode(in_content.strip().encode('utf-8'))
				t_output.delete(0.0, tk.END)
				t_output.insert(0.0, result)
				self.display_results(self.tab_code, 'base64 urlsafe encode completed')
			except Exception as e:
				self.display_results(self.tab_code, str(e))
		def fbase64_url_de():
			try:
				in_content = t_input.get(0.0, tk.END)
				result = base64.urlsafe_b64decode(in_content.strip().encode('utf-8'))
				t_output.delete(0.0, tk.END)
				t_output.insert(0.0, result)
				self.display_results(self.tab_code, 'base64 urlsafe decode completed')
			except Exception as e:
				self.display_results(self.tab_code, str(e))

		def fhtml_escape():
			try:
				in_content = t_input.get(0.0, tk.END)
				result = html.escape(in_content.strip())
				t_output.delete(0.0, tk.END)
				t_output.insert(0.0, result)
				self.display_results(self.tab_code, 'html escape completed')
			except Exception as e:
				self.display_results(self.tab_code, str(e))
		def fhtml_unescape():
			try:
				in_content = t_input.get(0.0, tk.END)
				result = html.unescape(in_content.strip())
				t_output.delete(0.0, tk.END)
				t_output.insert(0.0, result)
				self.display_results(self.tab_code, 'html unescape completed')
			except Exception as e:
				self.display_results(self.tab_code, str(e))
		def furl_encode():
			try:
				in_content = t_input.get(0.0, tk.END)
				result = urllib.parse.quote(in_content.strip(), safe='')
				t_output.delete(0.0, tk.END)
				t_output.insert(0.0, result)
				self.display_results(self.tab_code, 'html unescape completed')
			except Exception as e:
				self.display_results(self.tab_code, str(e))

		def furl_decode():
			try:
				in_content = t_input.get(0.0, tk.END)
				result = urllib.parse.unquote(in_content.strip())
				t_output.delete(0.0, tk.END)
				t_output.insert(0.0, result)
				self.display_results(self.tab_code, 'html unescape completed')
			except Exception as e:
				self.display_results(self.tab_code, str(e))
		def fhex_encode():
			try:
				in_content = t_input.get(0.0, tk.END)
				result = in_content.strip().encode('utf-8').hex()
				t_output.delete(0.0, tk.END)
				t_output.insert(0.0, '0x'+result)
			except Exception as e:
				self.display_results(self.tab_code, str(e))

		def fhex_decode():
			try:
				in_content = t_input.get(0.0, tk.END)
				result = bytes.fromhex(re.sub(r'^0x', '', in_content.strip()))
				t_output.delete(0.0, tk.END)
				t_output.insert(0.0, result)
			except Exception as e:
				self.display_results(self.tab_code, str(e))

		def fcount():
			try:
				out_content = t_output.get(0.0, tk.END)
				self.display_results(self.tab_code, len(out_content.strip()))
			except Exception as e:
				self.display_results(self.tab_code, str(e))
		
		b_base64_en = self.create_button(self.tab_code,fbase64en,'base64-en')
		b_base64_en.grid(row=1,column=0)
		b_base64_de = self.create_button(self.tab_code, fbase64de,'base64-de')
		b_base64_de.grid(row=2,column=0)

		b_base64_url_en = self.create_button(self.tab_code, fbase64_url_en,'b64-url-en')
		b_base64_url_en.grid(row=1,column=1)
		b_base64_url_de = self.create_button(self.tab_code, fbase64_url_de,'b64-url-de')
		b_base64_url_de.grid(row=2,column=1)

		b_html_escape = self.create_button(self.tab_code,fhtml_escape,'html-es')
		b_html_escape.grid(row=1,column=2)
		b_html_unescape = self.create_button(self.tab_code,fhtml_unescape,'html-unes')
		b_html_unescape.grid(row=2,column=2)

		b_url_encode = self.create_button(self.tab_code,furl_encode,'url-encode')
		b_url_encode.grid(row=1,column=3)
		b_url_decode = self.create_button(self.tab_code,furl_decode,'url-decode')
		b_url_decode.grid(row=2,column=3)

		b_hex_encode = self.create_button(self.tab_code,fhex_encode,'hex-encode')
		b_hex_encode.grid(row=1,column=4)
		b_hex_decode = self.create_button(self.tab_code,fhex_decode,'hex-decode')
		b_hex_decode.grid(row=2,column=4)

		t_input = self.create_text(self.tab_code,w=90,h=10)
		t_input.grid(row=0,column=0,columnspan=5)
		t_output = self.create_text(self.tab_code,w=90,h=10)
		t_output.grid(row=3,column=0,columnspan=5)
		b_count = self.create_button(self.tab_code, fcount, 'Count')
		b_count.grid(row=4, column=0, columnspan=5)

		b_output_clean = self.create_button(self.tab_code,foutput_clean,'Clean')
		b_output_clean.grid(row=3,column=5)
		b_input_clean = self.create_button(self.tab_code,finput_clean,'Clean')
		b_input_clean.grid(row=0,column=5)

		

##### Create tab scp
	# 判断IP是否存活
	def test_ip(self,ip):
		try:
			command = 'ping -n 2 -w 2 {}'.format(ip)
			p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			stdout = p.stdout.read().decode('gbk')
			if 'TTL' in stdout:
				return True
			else:
				return False
		except Exception as e:
			self.display_results(self.tab_scp, str(e))
	# 标签页scp
	def create_scp(self):
		result = None
		# vps/kali3按钮函数
		def fvps():
			e_ip.delete(0,tk.END)
			e_ip.insert(0,'45.77.34.43')
			e_port.delete(0,tk.END)
			e_port.insert(0,'31234')
		def fkali():
			e_ip.delete(0,tk.END)
			e_ip.insert(0,'192.168.133.128')
			e_port.delete(0,tk.END)
			e_port.insert(0,'22')
		def fcentos():
			e_ip.delete(0,tk.END)
			e_ip.insert(0,'192.168.231.129')
			e_port.delete(0,tk.END)
			e_port.insert(0,'22')

		# 使用paramiko实现文件下载
		def get_file(host,port,remote,local,name):
			try:
				private_key = paramiko.RSAKey.from_private_key_file("C:\\Users\\DC\\.ssh\\id_rsa")
				ssh = paramiko.SSHClient()
				ssh.load_host_keys("C:\\Users\\DC\\.ssh\\known_hosts")
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(hostname=host,port=port,username='root',pkey=private_key)
				sftp = ssh.open_sftp()
				sftp.get(f'{remote}',f'{local}'+'/'+f'{name}')
				result = 'Download success!'
			except Exception as e:
				result = f'{host} {port} {remote} {local} {name}'
			finally:
				ssh.close()
				sftp.close()
			return result

		# 使用paramiko实现文件上传
		def put_file(host,port,local,remote,name):
			try:
				private_key = paramiko.RSAKey.from_private_key_file("C:\\Users\\DC\\.ssh\\id_rsa")
				ssh = paramiko.SSHClient()
				ssh.load_host_keys("C:\\Users\\DC\\.ssh\\known_hosts")
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(hostname=host,port=port,username='root',pkey=private_key)
				sftp = ssh.open_sftp()
				sftp.put(f'{local}',f'{remote}'+'/'+f'{name}')
				result = 'Upload success!'
				
			except Exception as e:
				result = e
			finally:
				ssh.close()
				sftp.close()

			return result

		# 远程IP地址
		l_ip = tk.Label(self.tab_scp,text='IP:',width=8,height=1,font=('Consolas','12'))
		l_ip.grid(row=0,column=0,sticky=tk.W)
		e_ip = self.create_entry(self.tab_scp,w=20)
		e_ip.grid(row=0,column=1,sticky=tk.W)
		e_ip.insert(0,'45.77.34.43')

		# 设置端口
		l_port = tk.Label(self.tab_scp,text='Port:',width=8,height=1,font=('Consolas','12'))
		l_port.grid(row=0,column=2,sticky=tk.W)
		e_port = self.create_entry(self.tab_scp,w=8)
		e_port.grid(row=0,column=3,sticky=tk.W)
		e_port.insert(0,'31234')
		

		# 更改IP按钮
		b_vps = self.create_button(self.tab_scp,fvps,'VPS')
		b_vps.grid(row=1,column=0,sticky=tk.W)

		b_kali = self.create_button(self.tab_scp,fcentos,'centos')
		b_kali.grid(row=1,column=1,sticky=tk.W)

		b_kali = self.create_button(self.tab_scp,fkali,'KALI')
		b_kali.grid(row=1,column=3,sticky=tk.W)
		
		# 按钮调用函数
		def button_download():
			# 是否写入IP地址
			if e_ip.get():
				# IP地址是否存活
				if self.test_ip(e_ip.get()):
					# 是否写入远程文件路径
					if e_down_remote_file.get() and e_down_remote_path.get():
						# 是否写入分隔符
						if e_down_separator.get():
							# 取出文件名
							separator = e_down_separator.get()
							file_list = e_down_remote_file.get().strip().split(separator)
							path = e_down_remote_path.get()
							for name in file_list:
								if path[-1] != '/' and path[-1] != '\\':
									file_name = path + '/' + name
								else:
									file_name = path + name

								# 调用 get_file函数，实现scp
								result = get_file(e_ip.get(),e_port.get(),file_name.replace('~/','/root/').strip(),e_local_down.get().replace('~/','/root/').strip(),name.strip())
								self.display_results(self.tab_scp, result)
						else:
							self.display_results(self.tab_scp,'Empty separator!')
					else:
						self.display_results(self.tab_scp,'Need path/file!')
				else:
					self.display_results(self.tab_scp,'Remote Ip dose not alive!')
			else:
				self.display_results(self.tab_scp,'Remote IP is empty!')

		def button_upload():
			# 是否写入IP地址
			if e_ip.get():
				# IP地址是否存活
				if self.test_ip(e_ip.get()):
					# 是否写入本地文件路径
					if e_upload_local_file.get() and e_upload_local_path.get():
						# 是否写入远程文件路径
						if e_remote_upload.get():
							# 是否写入分隔符
							if e_upload_separator.get():
								separator = e_upload_separator.get()
								file_list = e_upload_local_file.get().strip().split(separator)
								path = e_upload_local_path.get()
								for name in file_list:
									if path[-1] != '/' and path[-1] != '\\':
										file_name = path + '/' + name
									else:
										file_name = path + name

									# 调用 put_file函数，实现scp
									result = put_file(e_ip.get(),e_port.get(),file_name.replace('~/','/root/').strip(),e_remote_upload.get().replace('~/','/root/'),name.strip())
									self.display_results(self.tab_scp,result)

						else:
							self.display_results(self.tab_scp,'Need a remote path!')
					else:
						self.display_results(self.tab_scp,'Need a local file!')
				else:
					self.display_results(self.tab_scp,'Remote Ip dose not alive!')
			else:
				self.display_results(self.tab_scp,'Remote IP is empty!')

		# 分隔符
		l_separator_ = tk.Label(self.tab_scp,text='—'*75,height=1)
		l_separator_.grid(row=2,column=0,columnspan=10)

		# 下载
		# 文件名分隔符
		l_down_separator = self.create_label(self.tab_scp,'Separator:',w=20,h=2)
		l_down_separator.grid(row=3,column=0,sticky=tk.W)
		e_down_separator = self.create_entry(self.tab_scp,w=10)
		e_down_separator.grid(row=3,column=1,sticky=tk.W)
		e_down_separator.insert(0,'  ')

		# 文件内容

		l_down_remote_file = self.create_label(self.tab_scp,'Down_Remote_File:',w=20,h=2)
		l_down_remote_file.grid(row=4,column=0,sticky=tk.W)
		e_down_remote_file = self.create_entry(self.tab_scp,w=70)
		e_down_remote_file.grid(row=4,column=1,columnspan=3,sticky=tk.W)

		
		l_down_remote_path = self.create_label(self.tab_scp,'Down_Remote_Path:',w=20,h=2)
		l_down_remote_path.grid(row=5,column=0,sticky=tk.W)
		e_down_remote_path = self.create_entry(self.tab_scp,w=70)
		e_down_remote_path.grid(row=5,column=1,columnspan=3,sticky=tk.W)
		e_down_remote_path.insert(0,'/root/workspace/')

	
		l_local_down = self.create_label(self.tab_scp,'Down_Local:',w=20,h=2)
		l_local_down.grid(row=6,column=0,sticky=tk.W)
		e_local_down = self.create_entry(self.tab_scp,w=70)
		e_local_down.grid(row=6,column=1,columnspan=3,sticky=tk.W)
		e_local_down.insert(0,'C:\\Users\\DC\\Desktop\\')
		
		b_download = self.create_button(self.tab_scp,button_download,'Download')
		b_download.grid(row=7,column=0,columnspan=4)
		
		# 分隔空间
		l_separator_label = tk.Label(self.tab_scp,text='',font=('Consolas','12'),width=15,height=1)
		l_separator_label.grid(row=8,column=0)
				
		# 上传
		# 文件分隔符
		l_upload_separator = self.create_label(self.tab_scp,'Separator:',w=20,h=2)
		l_upload_separator.grid(row=9,column=0,sticky=tk.W)
		e_upload_separator = self.create_entry(self.tab_scp,w=10)
		e_upload_separator.grid(row=9,column=1,columnspan=3,sticky=tk.W)
		e_upload_separator.insert(0,'  ')

		# 文件内容

		l_upload_local_file = self.create_label(self.tab_scp,'Upload_local_file:',w=20,h=2)
		l_upload_local_file.grid(row=10,column=0,sticky=tk.W)
		e_upload_local_file = self.create_entry(self.tab_scp,w=70)
		e_upload_local_file.grid(row=10,column=1,columnspan=3,sticky=tk.W)

		l_upload_local_path = self.create_label(self.tab_scp,'Upload_local_path:',w=20,h=2)
		l_upload_local_path.grid(row=11,column=0,sticky=tk.W)
		e_upload_local_path = self.create_entry(self.tab_scp,w=70)
		e_upload_local_path.grid(row=11,column=1,columnspan=3,sticky=tk.W)
		e_upload_local_path.insert(0,'C:\\Users\\DC\\Desktop\\')

		l_remote_upload = self.create_label(self.tab_scp,'Upload_Remote:',w=20,h=2)
		l_remote_upload.grid(row=12,column=0,sticky=tk.W)
		e_remote_upload = self.create_entry(self.tab_scp,w=70)
		e_remote_upload.grid(row=12,column=1,columnspan=3,sticky=tk.W)
		
		
		b_upload = self.create_button(self.tab_scp,button_upload,'Upload')
		b_upload.grid(row=13,column=0,columnspan=4)		

if __name__ == '__main__':
	
	window = tk.Tk()
	Root(window)
	window.mainloop()