from requests.packages.urllib3.exceptions import InsecureRequestWarning
import tkinter as tk
from tkinter import ttk
import subprocess
import pyperclip
import requests
import time
import sys
import paramiko


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Root():
	# 构造函数
	def __init__(self,window):
		self.window = window
		self.set_window()
		# 创建notebook容器
		self.notebook = ttk.Notebook(self.window)

		# 创建标签页scp
		self.tab_scp = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_scp,text="SCP    ")
		self.create_scp()

		# 创建标签页 Websites, batch access to url
		self.tab_websites = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_websites,text="    Websites    ")
		self.create_websites()

		# 创建标签页 Open URL 自定义URL并且访问
		self.tab_openurl = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_openurl,text="    Open URL    ")
		self.create_openurl()

		# 创建标签页replace
		self.tab_replace = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_replace,text="    Replace    ")
		self.create_replace()


		
		# 创建标签页URLTest
		self.tab_urltest = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_urltest,text="    URLTest    ")
		self.create_urltest()

		# 创建标签页 dealwith 用于对URL做自定义处理
		self.tab_dealwith = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_dealwith,text="    Deal with URL    ")
		self.create_dealwith()



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

##### 创建标签页 Websites
	def display_websites(self,result):
		l_result = tk.Label(self.tab_websites,text=result,font=('Consolas','12'),width=100,height=5)
		l_result.grid(row=30,column=0,columnspan=10)
	def create_websites(self):
		# access button function 
		def faccess():
			urls = t_urls.get(0.0,tk.END)
			for url in urls.strip().split('\n'):
				try:
					if url:
						com = f'@start chrome {url.strip()}'
						p = subprocess.Popen(com,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
					else:
						pass
				except Exception as e:
					self.display_websites(str(e))

			if p.stderr.read():
				self.display_websites(p.stderr.read())
			else:
				self.display_websites('All URLs accessed')

		# 清空按钮函数
		def fclean():
			t_urls.delete(0.0,tk.END)
			self.display_websites('')

		l_description = self.create_label(self.tab_websites,'Access to websites.Pause access every N lines ->',w=65,h=1)
		l_description.grid(row=0,column=0)

		l_number = self.create_label(self.tab_websites,'Number:',w=10,h=1)
		l_number.grid(row=0,column=1)

		e_number = self.create_entry(self.tab_websites,w=10)
		e_number.grid(row=0,column=2,sticky=tk.W)

		t_urls = self.create_text(self.tab_websites,w=85,h=27)
		t_urls.grid(row=1,column=0,rowspan=4,columnspan=3)

		b_access = self.create_button(self.tab_websites,faccess,' Access ')
		b_access.grid(row=2,column=3)

		b_clean = self.create_button(self.tab_websites,fclean,' Clean ')
		b_clean.grid(row=5,column=0)



##### 创建标签页replace

	def create_replace(self):
		# 替换按钮函数
		def freplace():
			before = t_input.get(0.0,tk.END)
			a = e_a.get()
			b = e_b.get()
			after = before.replace(a,b)
			t_output.delete('1.0','end')
			t_output.insert('insert',after)
		# 清空按钮
		def finputclean():
			t_input.delete('1.0','end')

		# 清除空白字符
		def fstrip():
			t_output.delete('1.0','end')
			b = t_input.get(0.0,tk.END).strip().replace(' ','').replace('\n','').replace('\t','')
			t_output.insert('insert',b)
		# 复制按钮
		def fcopy():
			pyperclip.copy(t_output.get(0.0,tk.END).strip())

		t_input = self.create_text(self.tab_replace,90,15)
		t_input.grid(row=0,column=0,columnspan=4)

		b_input_clean = self.create_button(self.tab_replace,finputclean,'Clean')
		b_input_clean.grid(row=0,column=4)

		e_a = self.create_entry(self.tab_replace,w=10)
		e_a.grid(row=1,column=0)
		# 初始值为空格
		e_a.insert(0,' ')

		l_l = self.create_label(self.tab_replace,'Replace ——>')
		l_l.grid(row=1,column=1)

		e_b = self.create_entry(self.tab_replace,w=10)
		e_b.grid(row=1,column=2)

		b_replace = self.create_button(self.tab_replace,freplace,'Replace')
		b_replace.grid(row=1,column=3,columnspan=1)

		b_strip = self.create_button(self.tab_replace,fstrip,'Strip')
		b_strip.grid(row=1,column=4)

		t_output = self.create_text(self.tab_replace,90,15)
		t_output.grid(row=2,column=0,columnspan=4)

		# b_output_clean = self.create_button(self.tab_replace,foutputclean,'Clean')
		# b_output_clean.grid(row=2,column=4)

		b_copy = self.create_button(self.tab_replace,fcopy,'Copy')
		b_copy.grid(row=2,column=4)


##### 创建标签页scp

	# # 输入框绑定的事件
	# def clean(self,display_result):
	# 	self.display_result('')

	# 结果显示
	def display_result(self,result):
		# l_result = self.create_label(result)
		l_result = tk.Label(self.tab_scp,text=result,font=('Consolas','12'),width=100,height=5)
		l_result.grid(row=30,column=0,columnspan=10)

	# 判断IP是否存活
	def test_ip(self,ip):
		command = 'ping -n 2 -w 2 {}'.format(ip)
		p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		stdout = p.stdout.read().decode('gbk')
		if 'TTL' in stdout:
			return True
		else:
			return False
	# 标签页scp
	def create_scp(self):
		result = None
		# vps/kali3按钮函数
		def fvps():
			e_ip.delete(0,tk.END)
			e_ip.insert(0,'207.148.123.125')
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
				# self.display_result(result)
			except Exception as e:
				# result = e
				# self.display_result(result)
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
		e_ip.insert(0,'207.148.123.125')

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
								self.display_result(result)
						else:
							self.display_result('Empty separator!')
					else:
						self.display_result('Need path/file!')
				else:
					self.display_result('Remote Ip dose not alive!')
			else:
				self.display_result('Remote IP is empty!')

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
									self.display_result(result)

						else:
							self.display_result('Need a remote path!')
					else:
						self.display_result('Need a local file!')
				else:
					self.display_result('Remote Ip dose not alive!')
			else:
				self.display_result('Remote IP is empty!')

		# download clean button
		def clean_download():
			e_down_remote_file.delete(0,tk.END)
			self.display_result('')
		# upload clean button
		def clean_upload():
			e_upload_local_file.delete(0,tk.END)
			self.display_result('')


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
		e_down_remote_path.insert(0,'/root/result')

	
		l_local_down = self.create_label(self.tab_scp,'Down_Local:',w=20,h=2)
		l_local_down.grid(row=6,column=0,sticky=tk.W)
		e_local_down = self.create_entry(self.tab_scp,w=70)
		e_local_down.grid(row=6,column=1,columnspan=3,sticky=tk.W)
		e_local_down.insert(0,'C:\\Users\\DC\\Desktop\\')
		
		b_download = self.create_button(self.tab_scp,button_download,'Download')
		b_download.grid(row=7,column=0,columnspan=4)
		
		# clean按钮

		b_down_clean = self.create_button(self.tab_scp,clean_download,'Clean')
		b_down_clean.grid(row=7,column=4)


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

		# clean 按钮
		b_upload_clean = self.create_button(self.tab_scp,clean_upload,'Clean')
		b_upload_clean.grid(row=13,column=4)

##### 创建标签页URLTest
	
	# 结果显示
	def display(self,result):
		# l_result = self.create_label(result)
		l_result = tk.Label(self.tab_urltest,text=result,font=('Consolas','12'),width=100,height=4)
		l_result.grid(row=30,column=0,columnspan=10)

	def create_urltest(self):
		# 复制按钮
		def fcopy():
			pyperclip.copy(t_out.get(0.0,tk.END).strip())
			self.display('')
		# clean按钮
		def clean_download():
			t_path.delete(0.0,tk.END)
			self.display('')
		# yes 按钮
		def fyes():
			e_full.delete(0,tk.END)	
			e_full.insert(0,'yes')
			self.display('')
		#no 按钮
		def fno():
			e_full.delete(0,tk.END)	
			e_full.insert(0,'no')
			self.display('')
		# 404按钮
		def f404():
			e_code.delete(0,tk.END)
			e_code.insert(0,'404')
			self.display('')
		# 302按钮
		def f302():
			e_code.delete(0,tk.END)
			e_code.insert(0,'302')
			self.display('')
		# 302请求函数
		def req_302(url):
			try:
				res = requests.get(url=url,headers={"user-agent":"Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"},proxies={"http":"http://127.0.0.1:7890","https":"http://127.0.0.1:7890"},verify=False,allow_redirects=False)
				#
				code = res.status_code

				if "Location" in res.headers.keys():
					location = res.headers['Location']
				else:
					location = ""
				
				if code == 404:
					pass
				elif location == "/pageshow?pageId=1440505892360679424":
					pass
				else:
					t_out.insert('insert',url+' | '+str(code)+'\n')
				
				time.sleep(4)
			except Exception as e:
				self.display(e)

		# 404 请求函数
		def req_404(url):
			try:
				res = requests.get(url=url,headers={"user-agent":"Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"},proxies={"http":"http://127.0.0.1:7890","https":"http://127.0.0.1:7890"},verify=False,allow_redirects=False)
				#
				code = res.status_code

				if code == 404:
					pass
				else:
					t_out.insert('insert',url+' | '+str(code)+'\n')
				
				time.sleep(4)
			except Exception as e:
				self.display(e)



		def button_test():
			self.display('')
			yesno = e_full.get()
			statuscode = e_code.get()

			t_out.delete(0.0,tk.END)
			
			paths = t_path.get(0.0,tk.END).strip().split('\n')
			host = e_host.get()
			# 判断状态码
			if not statuscode:
				self.display('Fill in the Status_code!')

			elif statuscode == '404':

				# 判断是否为完整URL
				if not yesno:
					self.display('IsFullURL value is yes or no!')

				# 完整URL
				elif yesno == 'yes':
					self.display('')
					for path in paths:
						url = path.strip()
						url = url.replace('//','/').replace('https:/','https://').replace('http:/','http://')
						req_404(url)

				# 非完整URL
				elif yesno == 'no':

					# 测试输入是否为空
					if not host:
						self.display('host is empty!')
					else:
						self.display('')
						for path in paths:
							url = host.strip() + path.strip()
							url = url.replace('//','/').replace('https:/','https://').replace('http:/','http://')
							req_404(url)

				else:
					self.display('IsFullURL value is yes or no!')

			elif statuscode == '302':
				# 判断是否为完整URL
				if not yesno:
					self.display('IsFullURL value is yes or no!')

				# 完整URL
				elif yesno == 'yes':
					self.display('')
					for path in paths:
						url = path.strip()
						url = url.replace('//','/').replace('https:/','https://').replace('http:/','http://')
						req_404(url)

				# 非完整URL
				elif yesno == 'no':

					# 测试输入是否为空
					if not host:
						self.display('host is empty!')
					else:
						self.display('')
						for path in paths:
							url = host.strip() + path.strip()
							url = url.replace('//','/').replace('https:/','https://').replace('http:/','http://')
							req_404(url)

				else:
					self.display('IsFullURL value is yes or no!')
			else:
				self.display('Status_code will be 404 or 302!')

		# Host:
		l_host = self.create_label(self.tab_urltest,"Host:",w=15,h=1)
		l_host.grid(row=0,column=0)

		e_host = self.create_entry(self.tab_urltest,w=15)
		e_host.grid(row=0,column=1)

		# button
		b_test = self.create_button(self.tab_urltest,button_test,'Test')
		b_test.grid(row=0,column=2)
		
		# 是否是完整的URL
		l_full = self.create_label(self.tab_urltest,"IsFullURL:",w=10,h=1)
		l_full.grid(row=1,column=0)

		e_full = self.create_entry(self.tab_urltest,w=10)
		e_full.grid(row=1,column=1)
		e_full.insert(0,'no')

		# yes button 
		b_yes = self.create_button(self.tab_urltest,fyes,'yes')
		b_yes.grid(row=1,column=2)

		# no button 
		b_no = self.create_button(self.tab_urltest,fno,'no')
		b_no.grid(row=1,column=3)

		#http code
		l_code = self.create_label(self.tab_urltest,"Status_code:",w=15)
		l_code.grid(row=2,column=0)

		e_code = self.create_entry(self.tab_urltest,w=10)
		e_code.grid(row=2,column=1)
		e_code.insert(0,'404')

		# code botton
		b_404 = self.create_button(self.tab_urltest,f404,"404")
		b_404.grid(row=2,column=2)

		b_302 = self.create_button(self.tab_urltest,f302,"302")
		b_302.grid(row=2,column=3)

		# Path
		l_path = self.create_label(self.tab_urltest,"Path:",w=15,h=1)
		l_path.grid(row=3,column=0)

		t_path = self.create_text(self.tab_urltest,w=35,h=23)
		t_path.grid(row=3,column=1)

		# clean button
		b_down_clean = self.create_button(self.tab_urltest,clean_download,'Clean')
		b_down_clean.grid(row=4,column=1)

		# output
		l_out = self.create_label(self.tab_urltest,"Output:",w=10,h=1)
		l_out.grid(row=3,column=2)

		t_out = self.create_text(self.tab_urltest,w=35,h=23)
		t_out.grid(row=3,column=3)

		# copy button
		b_copy = self.create_button(self.tab_urltest,fcopy,'Copy')
		b_copy.grid(row=4,column=3)


##### 创建标签页 dealwith 用于对URL做自定义处理
	def display_dealwith(self,result):
		l_result = tk.Label(self.tab_dealwith,text=result,font=('Consolas','12'),width=100,height=5)
		l_result.grid(row=30,column=0,columnspan=10)

	def create_dealwith(self):
		# Button1 函数
		def Bone():
			username = t_input1.get(0.0,tk.END).strip().replace('。','').replace('@','').replace(';','').replace('；','').replace('.','').replace(',','').replace('，','')
			if username:
				url = "https://t.me/" + username
				command = "start chrome %s" %(url)
				try:
					p = subprocess.Popen(command,shell=True,stderr=subprocess.PIPE)
				except Exception as e:
					self.display_dealwith(e)

				if not p.stderr.read():
					self.display_dealwith('Access success!')						
				
			else:
				self.display_dealwith("username is Empty!")

			# self.display_dealwith(username)
		

		def Btwo():
			pass


		# 自定义说明
		Description = "快捷访问电报机器人"

		# 说明
		l_description = self.create_label(self.tab_dealwith,"Description:",w=20)
		l_description.grid(row=0,column=0)

		l_descriptions = self.create_label(self.tab_dealwith,display=Description,w=50)
		l_descriptions.grid(row=0,column=1)

		# 分隔符
		l_separator2 = self.create_label(self.tab_dealwith,display=' '*75,h=1)
		l_separator2.grid(row=1,column=0)

		# 输入框1
		l_input1 = self.create_label(self.tab_dealwith,"Input1:")
		l_input1.grid(row=2,column=0)

		t_input1 = self.create_text(self.tab_dealwith,w=50,h=10)
		t_input1.grid(row=2,column=1)

		# 输入框1 说明
		l_input1_des = self.create_label(self.tab_dealwith,"Des:")
		l_input1_des.grid(row=2,column=2)

		e_input1_des = self.create_entry(self.tab_dealwith)
		e_input1_des.grid(row=2,column=3)

		# 分隔符
		l_separator2 = self.create_label(self.tab_dealwith,display=' '*75,h=1)
		l_separator2.grid(row=3,column=0)

		# 输入框2
		l_input2 = self.create_label(self.tab_dealwith,"Input2:")
		l_input2.grid(row=4,column=0)

		t_input2 = self.create_text(self.tab_dealwith,w=50,h=10)
		t_input2.grid(row=4,column=1)

		# 输入框2 说明
		l_input2_des = self.create_label(self.tab_dealwith,"Des:")
		l_input2_des.grid(row=4,column=2)

		e_input2_des = self.create_entry(self.tab_dealwith)
		e_input2_des.grid(row=4,column=3)

		e_input2_des.insert(0,'Not enabled')

		# 分隔符
		l_separator2 = self.create_label(self.tab_dealwith,display=' '*75,h=1)
		l_separator2.grid(row=5,column=0)


		# 按钮1
		b_1 = self.create_button(self.tab_dealwith,Bone,'Button1')
		b_1.grid(row=8,column=1)

		l_b1 = self.create_label(self.tab_dealwith,"Des:")
		l_b1.grid(row=8,column=2)

		e_b1_des = self.create_entry(self.tab_dealwith)
		e_b1_des.grid(row=8,column=3)

		# 分隔符
		l_separator2 = self.create_label(self.tab_dealwith,display=' '*75,h=1)
		l_separator2.grid(row=9,column=0)

		# 按钮2
		b_2 = self.create_button(self.tab_dealwith,Btwo,"Button2")
		b_2.grid(row=10,column=1)

		l_b2 = self.create_label(self.tab_dealwith,"Des:")
		l_b2.grid(row=10,column=2)

		e_b2_des = self.create_entry(self.tab_dealwith)
		e_b2_des.grid(row=10,column=3)
		e_b2_des.insert(0,'Not enabled')

##### 创建标签页 Open URL 自定义URL并且访问
	def display_openurl(self,result):
		l_result = tk.Label(self.tab_openurl,text=result,font=('Consolas','12'),width=100,height=5)
		l_result.grid(row=30,column=0,columnspan=10)

	def create_openurl(self):
		# button function
		def button_open():
			url = e_url.get()
			plist = []
			p1 = e_1.get()
			p2 = e_2.get()
			p3 = e_3.get()
			p4 = e_4.get()
			p5 = e_5.get()
			if not url:
				self.display_openurl('URL is Empty!')
			else:
				if p1:
					plist.append(p1)
				if p2:
					plist.append(p2)
				if p3:
					plist.append(p3)
				if p4:
					plist.append(p4)
				if p5:
					plist.append(p5)
				for i in range(1,len(plist)+1):
					url = url.replace('${}'.format(i),plist[i-1])
				
				command = 'start chrome {url}'.format(url=url)
				try:
					p = subprocess.Popen(command,shell=True,stderr=subprocess.PIPE)
					stderr = p.stderr.read()
					if stderr:
						result = stderr
					else:
						result = 'Successfully opened: {}'.format(url)
				except Exception as e:
					result = e
				self.display_openurl(result)
			

		# 自定义说明
		Description = "用$number代表要替代的URL中的变量"

		# 说明
		l_description = self.create_label(self.tab_openurl,"Description:",w=15)
		l_description.grid(row=0,column=0)

		l_descriptions = self.create_label(self.tab_openurl,display=Description,w=50)
		l_descriptions.grid(row=0,column=1)

		# 分隔符
		l_separator = self.create_label(self.tab_openurl,display=' '*75,h=1)
		l_separator.grid(row=1,column=0)

		# URL输入框
		l_url = self.create_label(self.tab_openurl,'URL:',w=10,h=1)
		l_url.grid(row=2,column=0,sticky=tk.W)
		e_url = self.create_entry(self.tab_openurl,w=85)
		e_url.grid(row=2,column=1,sticky=tk.W)
		e_url.insert(0,'https://api.github.com/repos/$1/$2/releases/latest')
		# 分隔符2
		l_separator_2 = self.create_label(self.tab_openurl,display=' '*75,h=1)
		l_separator_2.grid(row=3,column=0)

		# 输入框1
		l_1 = self.create_label(self.tab_openurl,'Param1:',w=10,h=1)
		l_1.grid(row=4,column=0,sticky=tk.W)
		e_1 = self.create_entry(self.tab_openurl,w=20)
		e_1.grid(row=4,column=1,sticky=tk.W)

		# 输入框2
		l_2 = self.create_label(self.tab_openurl,'Param2:',w=10,h=1)
		l_2.grid(row=5,column=0,sticky=tk.W)
		e_2 = self.create_entry(self.tab_openurl,w=20)
		e_2.grid(row=5,column=1,sticky=tk.W)

		# 输入框1
		l_3 = self.create_label(self.tab_openurl,'Param3:',w=10,h=1)
		l_3.grid(row=6,column=0,sticky=tk.W)
		e_3 = self.create_entry(self.tab_openurl,w=20)
		e_3.grid(row=6,column=1,sticky=tk.W)

		# 输入框1
		l_4 = self.create_label(self.tab_openurl,'Param4:',w=10,h=1)
		l_4.grid(row=7,column=0,sticky=tk.W)
		e_4 = self.create_entry(self.tab_openurl,w=20)
		e_4.grid(row=7,column=1,sticky=tk.W)

		# 输入框1
		l_5 = self.create_label(self.tab_openurl,'Param5:',w=10,h=1)
		l_5.grid(row=8,column=0,sticky=tk.W)
		e_5 = self.create_entry(self.tab_openurl,w=20)
		e_5.grid(row=8,column=1,sticky=tk.W)

		# 访问按钮
		b_open = self.create_button(self.tab_openurl,button_open,'Open')
		b_open.grid(row=13,column=0,columnspan=4)	

if __name__ == '__main__':
	
	window = tk.Tk()
	Root(window)
	window.mainloop()