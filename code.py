"""
中華レーザー(K40 Whisperer)用のハンドホイールのプログラム
K40 Whispererのショートカット
	https://www.scorchworks.com/K40whisperer/k40w_manual.html#keyboard

［入力］
ボタン
 [X]	ヘッドの移動方向をＸ軸にする（右：＋）
 [Y]	　　　〃　　　　　Ｙ軸　〃
 [x1]	ヘッドの移動距離を１mmにする（上：＋）
 [x5]	　〃　の　　〃　　５mm　〃
 [home]	ヘッドをホーミング

ロータリーエンコーダ
　＋(時計回)　ヘッドの移動方向を軸に対して＋方向に移動
　－(反時計)　ヘッドの　　　　〃　　　　　ー方向　〃


"""

import board		# 基板関係(アサインとか)
import rotaryio		# ロータリーエンコーダ
import usb_hid		# HID
import digitalio	# GPIO
import neopixel		# LEDテープ
import rainbowio	# LEDテープを虹
import time
import keypad
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard import Keycode



### 初期設定 ############################################################

# キーボードのオブジェクト
kbd = Keyboard( usb_hid.devices )


# 複数の端子をリスト化してデバウンス
#	          0           1          2           3          4
#             [X]         [Y]        [x1]        [x5]       [HOME]
myPinsIN  = ( board.GP25, board.GP3, board.GP27, board.GP1, board.GP0 )	# SW
myPinsOUT = ( board.GP26, board.GP4, board.GP28, board.GP2 )			# LED
myBTNs = []
myLEDs = []
myBtns = keypad.Keys( myPinsIN, value_when_pressed=False, pull=True )	# ボタンの設定

for ii, pin in enumerate( myPinsOUT ) :		# enumerate(添字)込みの繰り返し
	tmp_pin = digitalio.DigitalInOut( pin )	# 端子の指定	
	tmp_pin.direction = digitalio.Direction.OUTPUT	# 出力
	myLEDs.append( tmp_pin )						# LED　※Debouncer不要


# エンコーダ
encoder = rotaryio.IncrementalEncoder( board.GP15, board.GP14 )	# エンコーダの設定
position_last = None											# 初期値
tmp_pin = digitalio.DigitalInOut( board.GP16 )	# LED用の端子の指定
tmp_pin.direction = digitalio.Direction.OUTPUT	# 　 〃　端子を出力
tmp_pin.value = True							#  　　　端子をHigh


# Neopixelの制御
num_leds = 1	# LEDの数
led = neopixel.NeoPixel( board.GP13, num_leds, brightness=0.2 )


# ボタン状態の変数
XY = 0	# 0:X,  1:Y
xx = 0	# 0:x1, 1:x5
myLEDs[0].value = True	# [X] 点灯
myLEDs[2].value = True	# [x1]点灯



### ループ ############################################################
while True:
	
	myBtn = myBtns.events.get()
	if myBtn :
		if myBtn.presed :
			# [X]
			if  myBtn.key_number == 0 :
				XY == 0
				myLEDs[0].value = True	# X LED点灯
				myLEDs[1].value = False	# Y LED消灯

			# [Y]
			elif  myBtn.key_number == 1 :
				XY == 1
				myLEDs[0].value = False	# X LED消灯
				myLEDs[1].value = True	# Y LED点灯

			# [x1]
			elif  myBtn.key_number == 2 :
				xx == 0
				myBtns[2].value = True			# x1 LED点灯
				myBtns[3].value = False			# x5 LED消灯
				kbd.send( Keycode.BACKSPACE )	# 文字を消して"1"を入力
				kbd.send( Keycode.ONE )			# 	※一文字を前提としている！

			# [x5]
			elif  myBtn.key_number == 3 :
				xx == 0
				myBtns[2].value = False			# x1 LED消灯
				myBtns[3].value = True			# x5 LED点灯
				kbd.send( Keycode.BACKSPACE )	# 文字を消して”5”を入力
				kbd.send( Keycode.FIVE )		# 	※一文字を前提としている！

			# [home]
			elif ii == 4 :
				kbd.send( Keycode.LEFT_CONTROL, Keycode.H )	# Ctl + H


	# ロータリーエンコーダーによる挙動
	position = encoder.position	#値取得
	
	if not(position_last is None) and position != position_last:	#非初期値 かつ 値変更
		#print( position )
		
		# 上移動
		if   ( XY == 1 ) and ( (position - position_last) > 0 ) :
			kbd.send( Keycode.LEFT_CONTROL, Keycode.UP_ARROW )	  # Ctrl + ↑

		# 下移動
		elif ( XY == 1 ) and ( (position - position_last) < 0 ) :
			kbd.send( Keycode.LEFT_CONTROL, Keycode.DOWN_ARROW )  # Ctrl + ↓

		# 右移動
		elif ( XY == 0 ) and ( (position - position_last) > 0 ) :
			kbd.send( Keycode.LEFT_CONTROL, Keycode.RIGHT_ARROW ) # Ctrl + →

		# 左移動
		elif ( XY == 0 ) and ( (position - position_last) < 0 ) :
			kbd.send( Keycode.LEFT_CONTROL, Keycode.LEFT_ARROW )  # Ctrl + ←

		else :
			pass
	

	#led[0] = rainbowio.colorwheel( int( 10 * position ) % 255  )	# LEDをエンコーダ値で虹色に変更
	led[0] = rainbowio.colorwheel( int( 50 * time.monotonic() ) % 255  )	# LEDをエンコーダ値で虹色に変更
	led.show()  # LEDの値を変更後更新

	position_last = position 
