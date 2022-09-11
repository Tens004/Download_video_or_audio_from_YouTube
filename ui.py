# Thiếu tính năng đang tải xuống thì muốn hủy

import tkinter, main
from tkinter import *
from tkinter import scrolledtext, messagebox, messagebox, filedialog
from functools import partial
bg_color = '#b0b0b0'
scr = Tk()
scr.title('Tải xuống video/audio từ YouTube')
scr.geometry('335x200')
try:
	scr.iconbitmap('appicon.ico')
except:
	pass
scr.configure(background=bg_color)

# url = StringVar()
font_en = ('arial', 13)
radiofont = ('arial', 12)
mode = StringVar()
select_sttStart = StringVar()
select_sttEnd = StringVar()

def huy():
	global url, select_sttStart, select_sttEnd
	select_sttStart.set('')
	select_sttEnd.set('')
	# url.set('')
	home()
def dowloading(fileExtension):
	global select_sttStart, select_sttEnd, url
	
	if selectStt_enStart.get().isdigit():
		main.stt_start = int(selectStt_enStart.get())
		main.stt_end = int(selectStt_enEnd.get())
	
	totalDownload = main.stt_end - main.stt_start + 1
	if 0 < totalDownload <= len(main.videos):
		selectStt_str1.config(fg='#7a7a7a')
		selectStt_str2.config(fg='#7a7a7a')
		selectStt_enStart.config(state='disabled')
		selectStt_enEnd.config(state='disabled')
		download_bt_mp3.config(state='disabled', bg='#999999')
		download_bt_mp4.config(state='disabled', bg='#999999')
		huyDown_bt1.config(state='disabled', bg='#999999')
		
		main.downloadExtension = fileExtension #mp4/mp3
		# Chọn nơi lưu
		main.saveIn = filedialog.askdirectory()
		# Hiện thông báo tải xuống
		info = 'Đang tải xuống '+str(totalDownload)+ ' file '+main.downloadExtension.upper()+'...'
		lb = Label(scr, text=info, bg=bg_color, font=('arial bold', 14), fg='#e80505')
		lb.place(x=28, y=60)
		scr.update()

		main.run()
		lb.place_forget()
		str_comlete = 'Đã tải xuống '+str(main.totalCompleted)+' file '+main.downloadExtension+'.\nLưu tại: '+main.saveIn
		if main.totalFailed == 0:
			messagebox.showinfo('Tải xuống hoàn tất', str_comlete)
		else:
			err = '\nKhông thể tải xuống '+str(main.totalFailed)+' file từ:'
			for url in main.faileds:
				err += '\n'+url
			messagebox.showinfo('Tải xuống hoàn tất', str_comlete+'\n'+err)
		select_sttStart.set('')
		select_sttEnd.set('')
		# url.set('')
		home()
	else:
		messagebox.showerror('Không thể tải xuống!', 'Lỗi không xác định!')
def beforeDownload():
	# Ẩn nút get link
	getObj_bt.place_forget()
	# Bật nút tải xuống va  hiện nut huy
	download_bt_mp4.config(bg='#04d119')
	download_bt_mp3.config(bg='#04d119')
	download_bt_mp4.config(state='normal')
	download_bt_mp3.config(state='normal')
	huyDown_bt1.place(x = 258, y = 19)
def selectStt():
	global select_sttStart, select_sttEnd
	select_sttStart.set('1')
	select_sttEnd.set(len(main.videos))
	# Bật lựa chọn số video muốn tải
	selectStt_str1.config(fg='black')
	selectStt_str2.config(fg='black')
	selectStt_enStart.config(state='normal')
	selectStt_enEnd.config(state='normal')
def createObj():
	# Vô hiệu hóa chọn mode, lb_url, en_url
	mode1.config(state='disabled')
	mode2.config(state='disabled')
	mode3.config(state='disabled')
	en_url.config(state='disabled')
	lb.config(fg='#7a7a7a')
	getObj_bt.config(state='disabled', bg='#999999')
	scr.update()

	main.mode = mode.get()
	if main.createObject(en_url.get()):
		if len(main.videos) == 1:
			main.stt_start = 1
			main.stt_end = 1
			beforeDownload()
		else:
			selectStt()
			beforeDownload()
	else:
		home()
		messagebox.showerror('Lỗi không xác định!', 'Vui lòng kiểm tra lại liên kết hoặc\ntùy chọn video/playlist/channel')
def home():
	global mode,  lb, en_url, mode1, mode2, mode3, selectStt_str1, selectStt_str2, huyDown_bt1, download_bt_mp3, download_bt_mp4, getObj_bt, selectStt_enEnd, selectStt_enStart

	# đặt lại các giá trị cho hàm main
	main.mode = 'video'
	main.downloadExtension = 'mp4'
	main.stt_start = 1
	main.stt_end = 1
	main.saveIn = None
	main.faileds = completeds = videos = []
	main.totalFailed = totalCompleted = 0
	main.mp4_file = None
	main.mp3_file = None
	mode.set('video') # đặt nút mặc định được chọn
	lb = Label(scr, text='URL', font=('arial bold', 14), bg=bg_color)
	en_url = Entry(scr, width=23, font=font_en) #, textvariable=url
	en_url.focus()
	mode1 = Radiobutton(scr, text='Video', variable=mode, value='video', bg=bg_color, font=radiofont)
	mode2 = Radiobutton(scr, text='Playlist', variable=mode, value='playlist', bg=bg_color, font=radiofont)
	mode3 = Radiobutton(scr, text='Channel', variable=mode, value='channel', bg=bg_color, font=radiofont)
	selectStt_str1 = Label(scr, text='Chọn từ video video số', font=('arial', 12), bg=bg_color, fg='#7a7a7a')
	selectStt_str2 = Label(scr, text='đến', font=('arial', 12), bg=bg_color, fg='#7a7a7a')
	selectStt_enStart = Entry(scr, textvariable=select_sttStart, width=4, justify='center', state='disabled')
	selectStt_enEnd = Entry(scr, textvariable=select_sttEnd, width=4, justify='center', state='disabled')
	getObj_bt = Button(scr, text='➜', height=1, width=3, bg='#04d119', command=createObj, font=('arial bold', 9))
	download_bt_mp4 = Button(scr, text='↓ Video (mp4)', height=2, width=12, font=('arial bold', 10), bg='#999999', fg='white', state='disabled', command=partial(dowloading, 'mp4'))
	download_bt_mp3 = Button(scr, text='↓ Audio (mp3)', height=2, width=12, font=('arial bold', 10), bg='#999999', fg='white', state='disabled', command=partial(dowloading, 'mp3'))
	huyDown_bt1 = Button(scr, text='X', height=1, width=3, font=('arial blod', 9), bg='#bd0404', fg='white', command=huy)

	en_url.place(x = 78, y = 20)
	lb.place(x=28, y = 20)
	mode1.place(x = 30, y = 60)
	mode2.place(x = 110, y = 60)
	mode3.place(x = 200, y = 60)
	selectStt_str1.place(x = 28, y = 95)
	selectStt_str2.place(x = 230, y = 95)
	selectStt_enStart.place(x = 198, y = 97)
	selectStt_enEnd.place(x = 265, y = 97)
	getObj_bt.place(x = 258, y = 19)
	download_bt_mp4.place(x = 47, y = 130)
	download_bt_mp3.place(x = 175, y = 130)


home()

Label(scr, text='thanhtien.vn2004@gmail.com', font=('arial', 8), bg=bg_color).place(x=3, y=180)
scr.mainloop()