import tkinter as tk
from tkinter import ttk
import subprocess
import pyperclip



class Root():
	# 构造函数
	def __init__(self,window):
		self.window = window
		self.set_window()
		# 创建notebook容器
		self.notebook = ttk.Notebook(self.window)

		# 创建标签页scp
		self.tab_scp = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_scp,text="SCP")
		self.create_scp()

		# 创建标签页replace
		self.tab_replace = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_replace,text="Replace")
		self.create_replace()

		# 创建标签页pings
		self.tab_pings = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_pings,text="Pings")
		self.create_pings()
		
		self.notebook.pack()
	# 主面板设置
	def set_window(self):
		self.window.title('SmallTools')
		width = 930
		height = 650
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

	# 标签页pings创建函数
	def create_pings(self):
		# ping按钮函数
		def fping():
			ips = t_input.get(0.0,tk.END)
			# 循环内容
			for ip in ips.strip().split('\n'):
				# 判断IP是否为空
				if ip:
					com = 'ping -n 1 -w 1 %s' %(ip)
					p = subprocess.Popen(com,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
					result = p.stdout.read().decode('gbk')
					if not p.stderr.read():
						if result:
							t_output.insert('insert',result)
							t_output.insert('insert','—————————————————————————————————————————————')

		
		# 清空按钮函数
		def finputclean():
			t_input.delete(0.0,tk.END)

		def foutputclean():
			t_output.delete(0.0,tk.END)


		# 设置控件	
		t_input = self.create_text(self.tab_pings,w=45,h=31)
		t_input.grid(row=1,column=0,rowspan=2)

		t_output = self.create_text(self.tab_pings,w=45,h=31)
		t_output.grid(row=1,column=2,rowspan=2)

		b_ping = self.create_button(self.tab_pings,fping,'Ping')
		b_ping.grid(row=1,column=1)

		b_clean_input = self.create_button(self.tab_pings,finputclean,'Clean')
		b_clean_input.grid(row=0,column=0)

		b_clean_output = self.create_button(self.tab_pings,foutputclean,'Clean')
		b_clean_output.grid(row=0,column=2)


	# 创建标签页replace
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

		# def foutputclean():
		# 	t_output.delete('1.0','end')

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

		t_output = self.create_text(self.tab_replace,90,15)
		t_output.grid(row=2,column=0,columnspan=4)

		# b_output_clean = self.create_button(self.tab_replace,foutputclean,'Clean')
		# b_output_clean.grid(row=2,column=4)

		b_copy = self.create_button(self.tab_replace,fcopy,'Copy')
		b_copy.grid(row=2,column=4)


	# 创建标签页scp
	# 输入框绑定的事件
	# def clean(self,display_result):
	#	 self.display_result('')

	# 结果显示
	def display_result(self,result):
		# l_result = self.create_label(result)
		l_result = tk.Label(self.tab_scp,text=result,font=('Consolas','12'),width=100,height=5)
		l_result.grid(row=30,column=0,columnspan=10)

	# 判断IP是否存活
	def test_ip(self,ip):
		command = 'ping -n 1 -w 1 {}'.format(ip)
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
			e_ip.insert(0,'45.32.104.206')
		def fkali():
			e_ip.delete(0,tk.END)
			e_ip.insert(0,'192.168.1.80')
		def fkali3():
			e_ip.delete(0,tk.END)
			e_ip.insert(0,'192.168.124.182')

		# 远程IP地址
		l_ip = tk.Label(self.tab_scp,text='IP:',width=25,height=1,font=('Consolas','12'))
		l_ip.grid(row=0,column=0,sticky=tk.W)
		e_ip = self.create_entry(self.tab_scp,w=20)
		e_ip.grid(row=0,column=1,sticky=tk.W)
		e_ip.insert(0,'192.168.124.182')

		# 更改IP按钮
		b_vps = self.create_button(self.tab_scp,fvps,'VPS')
		b_vps.grid(row=1,column=0,sticky=tk.W)

		b_kali = self.create_button(self.tab_scp,fkali3,'KALI3')
		b_kali.grid(row=1,column=1,sticky=tk.W)

		b_kali = self.create_button(self.tab_scp,fkali,'KALI')
		b_kali.grid(row=1,column=2,sticky=tk.W)
		
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
								command = 'scp root@{ip}:{remote} {local}'.format(ip=e_ip.get(),remote=file_name,local=e_local_down.get())
								try:
									p = subprocess.Popen(command,shell=True,stderr=subprocess.PIPE)
									stderr = p.stderr.read()
									if stderr:
										result = stderr
									else:
										result = 'Download success!'
								except Exception as e:
									result = e
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
								file_list = e_upload_local_file.get().split(separator)
								path = e_upload_local_path.get()
								for name in file_list:
									if path[-1] != '/' and path[-1] != '\\':
										file_name = path + '/' + name
									else:
										file_name = path + name
									command = 'scp {local} root@{ip}:{remote}'.format(local=file_name,ip=e_ip.get(),remote=e_remote_upload.get())
									try:
										p = subprocess.Popen(command,shell=True,stderr=subprocess.PIPE)
										stderr = p.stderr.read()
										if stderr:
											result = stderr
										else:
											result = 'Upload success!'
									except Exception as e:
										result = e

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

		# upload clean button
		def clean_upload():
			e_upload_local_file.delete(0,tk.END)

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


if __name__ == '__main__':
	
	window = tk.Tk()
	Root(window)
	window.mainloop()