import os
import sys
import argparse
from difflib import SequenceMatcher
from pytube import YouTube
import ffmpeg
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
import urllib


defaultPath = "./downloaded/"


def main():
	global defaultPath

	parse = argparse.ArgumentParser(description='Downloader of youtube videos as mp3')
	parse.add_argument("-url", metavar="string", help="video url", type=str)
	parse.add_argument("-path", metavar="string", help="path to save file", type=str)

	if not len(sys.argv) > 1:
		parse.print_help()
		input("Press [Enter] to exit...")
		return

	args = parse.parse_args()

	if not args.url:
		return
	path = args.path if args.path else defaultPath

	if not os.path.exists(path):
		os.mkdir(path)

	if not path[len(path)-1] == '/':
		path += '/'

	video = YouTube(args.url)
	video.streams.get_audio_only().download(path)

	for file in os.listdir(path):
		ratio = SequenceMatcher(a=file,b=video.title).ratio()
		if ratio > 0.7:
			nPath = path+os.path.splitext(file)[0]+".mp3"
			stream = ffmpeg.input(path+file).output(nPath).run()
			imgData = urllib.request.urlopen(video.thumbnail_url).read()

			audiofile = MP3(nPath, ID3=ID3)

			try:
				audiofile.add_tags()
			except error:
				pass
			
			audiofile.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=imgData))
			audiofile.save()

			os.remove(path+file)


if __name__ == '__main__':
	main()