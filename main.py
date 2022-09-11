# Dùng link chanel vẫn có thể chọn mode video và tải về một video
# Nếu chương trình tải xuống mp4 bị lỗi 
#pytube.exceptions.RegexMatchError: get_throttling_function_name: could not find match for multiple
# thì update pytube bằng lệnh pip install --upgrade pytube

import os, glob, shutil
from pytube import Playlist, YouTube, Channel
# os.environ["IMAGEIO_FFMPEG_EXE"] = r'C:\ffmpeg\bin'
# from moviepy.video.io.VideoFileClip import VideoFileClip 
from moviepy.editor import *

mode = 'playlist'
downloadExtension = 'mp3'
stt_start = 1
stt_end = 1
saveIn = r'C:'
faileds = completeds = videos = []
totalFailed = totalCompleted = 0
mp4_file = None
mp3_file = None
# Convert MP4 to MP3
def convert(mp3_file, mp4_file):
	videoclip = VideoFileClip(mp4_file)
	audioclip = videoclip.audio
	audioclip.write_audiofile(mp3_file)
	audioclip.close()
	videoclip.close()

# Download MP4 file
def downMP4(video):
	global mp4_file
	try:
		stream = video.streams.filter(progressive=True, file_extension='mp4')
		if downloadExtension == 'mp4':
			stream = stream.last()
			stream.download(saveIn)
			mp4_file = glob.glob(saveIn + r'\*.mp4')[0]
		else:
			stream = stream.first()
			stream.download(saveIn + r'\DownloadYT_không can thiệp vào folder này')
			mp4_file = glob.glob(saveIn + r'\DownloadYT_không can thiệp vào folder này' + r'\*.mp4')[0]
	except Exception as bug:
		print('downMP4 failed:', bug)
def createObject(url):
	global videos
	videos = []
	try:
		if mode == 'playlist':
			p = Playlist(url)
			for video in p.videos:
				videos.append(video)
		elif mode == 'channel':
			p = Channel(url)
			for video in p.videos:
				videos.append(video)
		elif mode == 'video':
			p = YouTube(url)
			videos.append(p)
		#test
		print('Download ', len(videos), 'video...')
		if len(videos) < 1: return False
		return True
	except Exception as bug:
		print('createObject failed:', bug)
		return False
def run():
	global faileds, completeds, totalFailed, totalCompleted
	faileds = []
	completeds = []
	totalFailed = 0
	totalCompleted = 0
	for i in range(stt_start-1, stt_end):
		try:
			downMP4(videos[i])
			name = os.path.basename(mp4_file).split('.')[0]
			if downloadExtension == 'mp3':
				mp3_file = saveIn + '\\' + name + r'.mp3'
				convert(mp3_file, mp4_file)
				# Xóa thư mục tạm thời chứa file mp4
				if os.path.isdir(saveIn + r'\DownloadYT_không can thiệp vào folder này'):
					shutil.rmtree(saveIn + r'\DownloadYT_không can thiệp vào folder này')
				completeds.append(name)
				totalCompleted += 1
			elif downloadExtension == 'mp4':
				completeds.append(name)
				totalCompleted += 1
		except Exception as bug:
			print('run failed:', bug)
			faileds.append(videos[i].title)
			totalFailed += 1
		print('Completed', totalCompleted)
		print('Failed', totalFailed)
	print('RUN COMPLETED')
	
# if createObject(r'https://www.youtube.com/watch?v=rJtuwsj4b-g&list=PLtTKbxO5emsH1Biy7Eo-Zi1CGoSrHOQtp&index=4'):
# 	run()