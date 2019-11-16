import tkinter, shelve, os, time, base64, subprocess
from icon_file import ico
from tkinter import filedialog, ttk
from tkinter.scrolledtext import ScrolledText
from threading import Thread

class RootWindow(tkinter.Tk):
	def __init__(self):
		super(). __init__()
		
		ico_decode = base64.b64decode(ico)
		ico_p_image_obj = tkinter.PhotoImage(data = ico_decode)
		self.wm_iconphoto(True, ico_p_image_obj)
		
		#close button options
		self.protocol('WM_DELETE_WINDOW', self.exit_commands)
		self.resizable ('false', 'false')
					
		def ok_button_action():
#			print('def ok_button_action():') #test line
			ok_button.config(state ='disable')
			get_path_button.config(state = 'disable')
			stop_button.config(state = 'active')
			self._FINISH = False
			self.log_add('Service started')
			self.settings['string'] = instance_entry.get().strip()
			self.settings['db_name'] = db_name_entry.get().strip()
			self.settings['radio_button_login'] = self.radio_button_login.get()
			self.settings['username'] = username_entry.get().strip()
			self.settings['pass'] = password_entry.get().strip()
			self.settings['backup_path_entry'] = backup_path_entry.get().strip()
			self.settings['delay'] = delay_entry.get().strip()
			self.settings['interval'] = interval_entry.get().strip()
						 
			#shelve data to var
			data_obj = shelve.open('data')
			data_obj['settings'] = self.settings
			data_obj.close()

			self.generate_command()
			
			#threads defs
			t_count_to_backup = Thread(target = self.count_to_backup)
			t_count_to_backup.start()
			
			#get path button	
		def get_path_button_action():
#			print('get_path_button_action():') #test line
			self.settings['backup_path_entry'] = filedialog.askdirectory()
			self.settings['backup_path_entry'] = self.settings['backup_path_entry'].replace('/','\\')
			if self.settings['backup_path_entry'].endswith('\\'):
				pass
			else:
				self.settings['backup_path_entry'] += '\\'
#			print(self.settings['backup_path_entry']) #test line
			backup_path_entry.delete(0, 'end')
			backup_path_entry.insert(0, self.settings['backup_path_entry'])
			
			#About window
		def about_button_action():
			about_w = tkinter.Toplevel(self)
			about_w.resizable('false','false')
			about_w.geometry('400x120')
			about_w_label = tkinter.Label(about_w, text = 'SQL AutoBackup BETA,\n createb by MJS\n THE SOFTWARE IS PROVIDED\n"AS IS", WITHOUT WARRANTY OF ANY KIND', font = ('default', '10', 'bold'))
			about_w_ok_button = tkinter.Button(about_w, text = 'OK', command = about_w.destroy)
			about_w_label.pack()
			about_w_ok_button.pack()
			
		def stop_button_action():
#			print('stop_button_action')
			ok_button.config(state = 'active')
			stop_button.config(state = 'disable')
			get_path_button.config(state = 'active')
			self._FINISH = True
			
			
		#variables
		self.settings = {'radio_button_login': '', 'backup_path_entry' : ''}
		self.radio_button_login = tkinter.StringVar()
		self.entry_lenght = 50

#		print(self.settings) #test line
		
		#root window
		self.geometry('1000x365')
		self.title('SQL Auto Backup BETA')
		
		#elements:
		instance_label = tkinter.Label(self, text = 'Connection string', font = ('calibri', '10'))
		instance_entry = tkinter.Entry(self, width = self.entry_lenght, font = ('calibri', '10'))
		db_name_label = tkinter.Label(self, text = 'Database name', font = 'calibri 10')
		db_name_entry = tkinter.Entry(self, width = self.entry_lenght, font = ('calibri', '10'))
		login_radio_label = tkinter.Label(self, text = 'Login type', font = 'calibri 10')
		username_entry_label = tkinter.Label(self, text = 'Username', font = 'calibri 10')
		username_entry = tkinter.Entry(self, width = self.entry_lenght, font = ('calibri', '10'))
		password_entry_label = tkinter.Label(self, text = 'Password', font = 'calibri 10')
		password_entry = tkinter.Entry(self, width = self.entry_lenght, font = ('calibri', '10'))
		backup_path_entry_label = tkinter.Label(self, text = 'Path' , font = 'calibri 10')
		backup_path_entry = tkinter.Entry(self, width = self.entry_lenght, font = ('calibri', '10'))
		get_path_button = tkinter.Button(self, text = 'Location of backups', command = get_path_button_action, width = 20, font = ('calibri', '10'))
		delay_entry_label = tkinter.Label(self, text = 'Start after (minutes)',font = 'calibri 10')
		delay_entry = tkinter.Entry(self, width = 5, font = ('calibri', '10'))
		interval_entry_label = tkinter.Label(self, text = 'Backup interval (minutes)', font = 'calibri 10')
		interval_entry = tkinter.Entry(self, width = 5, font = ('calibri', '10'))
		self.progress_bar = ttk.Progressbar(self, orient = 'horizontal', length = 990, mode = 'determinate', maximum = 100, value = 0)
		self.scrolled_text = ScrolledText(self, width = 78, font = ('default', 8))
		#radio button
		radio_button_int = tkinter.Radiobutton(self, text="Integrated", variable = self.radio_button_login, value = 0, font = ('calibri', '10'))
		radio_button_log = tkinter.Radiobutton(self, text="User / Pass", variable = self.radio_button_login, value = 1, font = ('calibri', '10'))
		about_button = tkinter.Button(self, text = "About", command = about_button_action, width = 20, font = ('calibri', '10'))
		ok_button = tkinter.Button(self, text = 'Save settings\n &\n Launch backups', command = ok_button_action, width = 20, font = ('calibri', '10'))
		ok_button.focus_set()
		stop_button = tkinter.Button(self, text = 'Stop', width = 20, command = stop_button_action, state = 'disable', font = ('calibri', '10'))
		
		#load settings
		if os.path.isfile('data.bak'):
			data_obj = shelve.open('data')
			self.settings = data_obj['settings']
#			print(self.settings) #test line
			data_obj.close()
		
		#set loaded data
		if 'string' in self.settings:
			instance_entry.insert(0, self.settings['string'])
		if 'db_name' in self.settings:
			db_name_entry.insert(0, self.settings['db_name'])
		if 'radio_button_login' in self.settings:
			if self.settings['radio_button_login'] == '':
				self.settings['radio_button_login'] = '1'
			self.radio_button_login.set(self.settings['radio_button_login'])
		if 'username' in self.settings:
			username_entry.insert(0, self.settings['username'])
		if 'pass' in self.settings:
			password_entry.insert(0, self.settings['pass'])
		if 'backup_path_entry' in self.settings:
			if self.settings['backup_path_entry'] == '':
				self.settings['backup_path_entry'] = os.getcwd() + '\\'
			backup_path_entry.insert(0, self.settings['backup_path_entry'])
		if 'delay' in self.settings:
			delay_entry.insert(0, self.settings['delay'])
		
		if 'interval' in self.settings:
			interval_entry.insert(0, self.settings['interval'])
		
		#packs it as:
		self.columnconfigure(2, weight = 1)
		self.columnconfigure(3, weight = 2)
		instance_label.grid(column = 1, row = 1, sticky = 'w')
		instance_entry.grid(column = 1, row = 2, sticky = 'w')
		db_name_label.grid(column = 1, row = 3, sticky = 'w')
		db_name_entry.grid(column = 1, row = 4, sticky = 'w')
		login_radio_label.grid(column = 1, row = 5, sticky = 'w')
		radio_button_int.grid(column = 1, row = 6, sticky = 'w')
		radio_button_log.grid(column = 1, row = 7, sticky = 'w')
		username_entry_label.grid(column = 1, row = 8, sticky = 'w')
		username_entry.grid(column = 1, row = 9, sticky = 'w')
		password_entry_label.grid(column = 1, row = 10, sticky = 'w')
		password_entry.grid(column = 1, row = 11, sticky = 'w')
		backup_path_entry_label.grid(column = 1, row = 12, sticky = 'w')
		backup_path_entry.grid(column = 1, row = 13, sticky = 'w')	
		self.scrolled_text.grid(column = 3, row = 1, rowspan = 14)
		self.progress_bar.grid(column = 1, row = 15, columnspan = 3, pady = 5)
		ok_button.grid(column = 2, row = 6, rowspan = 3, sticky = 'w')
		stop_button.grid(column = 2, row = 9, sticky = 'w')
		about_button.grid(column = 2, row = 12, sticky = 'w')
		get_path_button.grid(column = 2, row = 13, sticky = 'w')
		delay_entry_label.grid(column = 2, row = 1, sticky = 'w')
		delay_entry.grid(column = 2, row = 2, sticky = 'w')
		interval_entry_label.grid(column = 2, row = 3, sticky = 'w')
		interval_entry.grid(column = 2, row = 4, sticky = 'w')
		
		#backup timer
	def count_to_backup(self):
#		print('def counting(self):') #test line
		if int(self.settings['delay']) > 0 :
			timer = (int(self.settings['delay']) * 60)
			self.settings['delay'] = 0
		else:
			timer = (int(self.settings['interval']) * 60)
		progress_bar_step = 100 / timer
		while timer > 0:
#			print(timer)
			self.progress_bar['value'] += progress_bar_step
			timer -= 1
			time.sleep(1)
			if self._FINISH == True:
#				print('hanging')
				self.log_add('Service stopped...')
				self.progress_bar['value'] = 0
				return 0
			if timer == 0:
				self.backup()
				
	def backup(self):
#		print('def backup(self):') #test line
#		print(self.settings['radio_button_login']) #test line
		self.log_add('Backuping...')
		self.generate_command()
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		if self.settings['radio_button_login'] == '0':
			process = subprocess.Popen(self.settings['string_system_backup'], stdin = subprocess.PIPE, stderr = subprocess.PIPE, stdout = subprocess.PIPE, startupinfo = si)
			result = process.communicate()
			self.log_add(result[0].decode('utf-8'))
			#result = process.communicate()
#			print(result[0].decode('utf-8'))
			#self.log_add(result[0].decode('utf-8'))
			#self.log_add(results.read())
#			print(results.read())
		else:
			process = subprocess.Popen(self.settings['string_login_backup'], stdin = subprocess.PIPE, stderr = subprocess.PIPE, stdout = subprocess.PIPE, startupinfo = si)
			result = process.communicate()
			self.log_add(result[0].decode('utf-8'))
		self.progress_bar['value'] = 0
		self.count_to_backup()

		#generatr backup links		
	def generate_command(self):
		self.generate_filename()
		
		self.settings['string_system_backup'] = 'sqlcmd -S ' + self.settings['string'] + ' -E -Q "BACKUP DATABASE ' + \
			self.settings['db_name'] + ' TO DISK = \'' +  self.settings['backup_path_entry'] + self.settings['bak_name'] + '\'"'
		
		self.settings['string_login_backup'] = 'sqlcmd -U ' + self.settings['username'] + ' -P ' + self.settings['pass'] + \
			' -S ' + self.settings['string'] + ' -Q ' + '"BACKUP DATABASE ' + self.settings['db_name'] + ' TO DISK =\'' + \
			self.settings['backup_path_entry'] + self.settings['bak_name'] + '\'"'
		
		#generate name for backup file		
	def generate_filename(self):
		self.settings['bak_name'] = time.strftime('%Y_%d_%B_T_%H_%M') + '.bak'
		
		#add to log
	def log_add(self, i = ''):
		if i.endswith('\n'):
			i = i [0:(len(i) - 2)]
		self.scrolled_text.insert('end', time.strftime('%Y_%d_%B_T:_%H:%M') + '\n')
		self.scrolled_text.insert('end', i + '\n')
		self.scrolled_text.see('end')
		
	#close button functions			
	def exit_commands(self):
#		print('def exit_commands(self):')
		self._FINISH = True
		time.sleep(2)
#		print('stop')
		self.destroy()
				
if __name__ == '__main__':
	root_w = RootWindow()
	root_w.mainloop()
