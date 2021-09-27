from subprocess import PIPE, Popen
from guibot.guibot import GuiBot
from pathlib import Path
import time
import sys
import pyautogui
import argparse

def collect_webrtc(args, ts):

	guibot = GuiBot()
	guibot.add_path('media')

	if guibot.exists('create_dump.png', timeout=3):
		guibot.click('create_dump.png')

	if guibot.exists('download.png', timeout=3):
		guibot.click('download.png')

	time.sleep(2)

	res = Popen(f'mkdir webrtc', shell=True)

	res = Popen(f'mv ~/Downloads/webrtc_internals_dump.txt webrtc/{ts}.json', 
		shell=True)

	with open('stats.log', 'a') as f:
		f.write(f'\n{ts}-{args.vca}-{args.browser}-{args.record}')

	return

def capture_traffic(args, ts):

	_ = Popen(f'mkdir captures', shell=True)

	filename = f'captures/{ts}.pcap'

	cmd = f'tshark -i {args.interface} -w {filename} -a duration:{str(args.time)}'
	res = Popen(cmd, shell=True)
	res.wait()

	return

def launch_meet(args):

	res = Popen('open chrome.app', shell=True)
	time.sleep(2)

	pyautogui.write('chrome://webrtc-internals')
	pyautogui.hotkey('enter')
	time.sleep(1)

	pyautogui.hotkey('command', 't')
	time.sleep(1)

	pyautogui.write(args.id)
	pyautogui.hotkey('enter')

	guibot = GuiBot()
	guibot.add_path('media')

	if guibot.exists('maximize.png', timeout=5):
		guibot.click('maximize.png')

	if guibot.exists('meet_join_now.png', timeout=20):
		guibot.click('meet_join_now.png')

	ts = int(time.time())

	capture_traffic(args, ts)

	time.sleep(1)
	pyautogui.hotkey('ctrl', 'tab')

	
	collect_webrtc(args, ts)

	pyautogui.hotkey('command', 'w')

	if guibot.exists('meet_end_call.png', timeout=5):
		guibot.click('meet_end_call.png')

	if guibot.exists('meet_leave_call.png', timeout=5):
		guibot.click('meet_leave_call.png')

	pyautogui.hotkey('command', 'w')

	return 

def launch_zoom(args):
	guibot = GuiBot()
	guibot.add_path('media')

	res = Popen('open chrome.app', shell=True)

	time.sleep(2)

	pyautogui.write(args.id)
	pyautogui.hotkey('enter')


	if args.browser:

		if guibot.exists('maximize.png', timeout=5):
			guibot.click('maximize.png')

		if guibot.exists('zoom_cancel.png', timeout=10):
			guibot.click('zoom_cancel.png')
		
		if guibot.exists('zoom_launch_meeting.png', timeout=10):
			guibot.click('zoom_launch_meeting.png')

		if guibot.exists('zoom_cancel.png', timeout=10):
			guibot.click('zoom_cancel.png')

		if guibot.exists('zoom_join_from_browser.png', timeout=10):
			guibot.click('zoom_join_from_browser.png')

		if guibot.exists('zoom_browser_join.png', timeout=10):
			guibot.click('zoom_browser_join.png')

		time.sleep(15)

		ts = int(time.time())

		capture_traffic(args, ts)

		pyautogui.moveTo(1200, 850, duration=2)

		if guibot.exists('zoom_browser_leave.png', timeout=5):
			guibot.click('zoom_browser_leave.png')

		time.sleep(1)

		pyautogui.hotkey('enter')

		time.sleep(1)

		pyautogui.hotkey('command', 'w')

		with open('stats.log', 'a') as f:
			f.write(f'\n{ts}-{args.vca}-{args.browser}-{args.record}')

		res = Popen('killall "Google Chrome"', shell=True)

	else:

		if guibot.exists('zoom_open_client.png', timeout=10):
			guibot.click('zoom_open_client.png')

		if guibot.exists('zoom_join_with_video.png', timeout=10):
			guibot.click('zoom_join_with_video.png')

		time.sleep(15)

		if guibot.exists('maximize.png', timeout=5):
			guibot.click('maximize.png')

		ts = int(time.time())

		capture_traffic(args, ts)

		pyautogui.moveTo(1200, 850, duration=2)

		if guibot.exists('zoom_client_leave.png', timeout=3):
			guibot.click('zoom_client_leave.png')

		if guibot.exists('zoom_client_leave_meeting.png', timeout=2):
			guibot.click('zoom_client_leave_meeting.png')

		with open('stats.log', 'a') as f:
			f.write(f'\n{ts}-{args.vca}-{args.browser}-{args.record}')

		time.sleep(2)

		pyautogui.hotkey('command', 'w')

		res = Popen('killall "Google Chrome"', shell=True)

	return

def launch_teams(args):

	guibot = GuiBot()
	guibot.add_path('media')

	res = Popen('open chrome.app', shell=True)

	time.sleep(2)

	pyautogui.write('chrome://webrtc-internals')
	pyautogui.hotkey('enter')
	time.sleep(1)

	pyautogui.hotkey('command', 't')
	time.sleep(1)

	pyautogui.write(args.id)
	pyautogui.hotkey('enter')

	if args.browser:

		if guibot.exists('teams_cancel.png', timeout=10):
			guibot.click('teams_cancel.png')
		if guibot.exists('teams_browser.png', timeout=5):
			guibot.click('teams_browser.png')
		time.sleep(10)
		if guibot.exists('teams_join_now.png', timeout=20):
			guibot.click('teams_join_now.png')
		if guibot.exists('maximize.png', timeout=5):
			guibot.click('maximize.png')

		pyautogui.moveTo(800, 620, duration=1.5)

		if guibot.exists('teams_camera_off.png', timeout=25):
			guibot.click('teams_camera_off.png')

		ts = int(time.time())

		capture_traffic(args, ts)

		pyautogui.hotkey('ctrl', 'tab')

		collect_webrtc(args, ts)

		pyautogui.hotkey('command', 'w')

		pyautogui.moveTo(800, 620, duration=1.5)

		if guibot.exists('teams_hang_up.png', timeout=5):
			guibot.click('teams_hang_up.png')

		time.sleep(2)

		pyautogui.hotkey('command', 'w')

	else:

		if guibot.exists('teams_launch_client.png', timeout=10):
			guibot.click('teams_launch_client.png')

		if guibot.exists('teams_client_join.png', timeout=10):
			guibot.click('teams_client_join.png')

		if guibot.exists('teams_client_join_now.png', timeout=10):
			guibot.click('teams_client_join_now.png')
		if guibot.exists('teams_client_x.png', timeout=10):
			guibot.click('teams_client_x.png')

		if guibot.exists('teams_maximize.png', timeout=5):
			guibot.click('teams_maximize.png')

		ts = int(time.time())

		capture_traffic(args, ts)

		pyautogui.moveTo(800, 620, duration=1.5)

		if guibot.exists('teams_client_leave', timeout=5):
			guibot.click('teams_client_leave')

		time.sleep(2)

		res = Popen('killall "Google Chrome"', shell=True)

		print("done")

		with open('stats.log', 'a') as f:
			f.write(f'\n{ts}-{args.vca}-{args.browser}-{args.record}')

	res = Popen('killall "Google Chrome"', shell=True)


def launch(args):

	if args.vca == 'meet':
		launch_meet(args)
	elif args.vca == 'zoom':
		launch_zoom(args)
	else:
		launch_teams(args)

def build_parser():

	parser = argparse.ArgumentParser(
		description='Initiate and capture video call')

	parser.add_argument(
		'vca',
		help="VCA to use"
	)

	parser.add_argument(
		'time',
		help='Length of call'
	)

	parser.add_argument(
		'-b', '--browser',
		default=False,
		action='store_true',
		help='Launch call in browser (as opposed to client)'
	)

	parser.add_argument(
		'-id', '--id',
		default=None,
		action='store',
		help='Meeting ID'
	)

	parser.add_argument(
		'-r', '--record',
		default=None,
		action='store',
		help='Name of test to log'
	)

	parser.add_argument(
		'-i', '--interface',
		default=None,
		action='store',
		help='Interface to capture network traffic'
	)

	return parser


def execute():

	parser = build_parser()
	args = parser.parse_args()

	launch(args)


if __name__ == '__main__':
	execute()