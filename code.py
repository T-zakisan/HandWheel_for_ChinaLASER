"""
中華レーザー(K40 Whisperer)用のハンドホイールのプログラム
K40 Whispererのショートカット
	https://www.scorchworks.com/K40whisperer/k40w_manual.html#keyboard

ボタン
 [X]	ヘッドの移動方向をＸ軸にする（右：＋）
 [Y]	　　　〃　　　　　Ｙ軸　〃
 [x1]	ヘッドの移動距離を１mmにする（上：＋）
 [x5]	　〃　の　　〃　　５mm　〃
 [home]	ヘッドをホーミング

ロータリーエンコーダ
　＋(時計回)　ヘッドの移動方向を軸に対して＋方向に移動
　－(反時計)　ヘッドの　　　　〃　　　　　－方向　〃


"""


import board		# 基板関係(アサインとか)
import rotaryio		# ロータリーエンコーダ
import usb_hid		# HID
import digitalio	# GPIO
import neopixel		# LEDテープ
import rainbowio	# LEDテープを虹
import time 
from adafruit_debouncer    import Debouncer
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard import Keycode


### 初期設定 ############################################################

# キーボードのオブジェクト
kbd = Keyboard( usb_hid.devices )


# 複数の端子をリスト化してデバウンス
#	       0           1           2          3          4           5           6          7          8
#	       [X]     SW, [X]    LED, [Y]    SW, [Y]   LED, [x1]    SW, [x1]   LED, [x5]   SW, [x5]  LED, [HOME] SW
myPins = ( board.GP25, board.GP26, board.GP3, board.GP4, board.GP27, board.GP28, board.GP1, board.GP2, board.GP0 )
myBtns = []
for ii, pin in enumerate( myPins ) :		# enumerate(添字)込みの繰り返し
	tmp_pin = digitalio.DigitalInOut( pin )	# 端子の指定
	
	#偶数：ボタン(入力)
	if ii % 2 == 0 :
		tmp_pin.pull = digitalio.Pull.UP 		# 内部のプルアップ抵抗を有効化
		myBtns.append( Debouncer( tmp_pin ) )	# スイッチ　※Debouncer()必須

	#奇数：ＬＥＤ(出力)
	elif ii % 2 == 1 :
		tmp_pin.direction = digitalio.Direction.OUTPUT	# 出力
		myBtns.append( tmp_pin )						# LED　※Debouncer不要
	
	else :
		pass	
	

# エンコーダ
encoder = rotaryio.IncrementalEncoder( board.GP15, board.GP14 )	# エンコーダの設定
position_last = None											# 初期値
tmp_pin = digitalio.DigitalInOut( board.GP16 )	# LED用の端子の指定
tmp_pin.direction = digitalio.Direction.OUTPUT	# 　 〃　端子を出力
tmp_pin.value = True							#  　　　端子をHigh


# Neopixel（フルカラーLED）
num_leds = 1	# LEDの数
led = neopixel.NeoPixel( board.GP13, num_leds, brightness=0.1 )


# ボタン状態の変数
XY = 0	# 0:X,  1:Y
xx = 0	# 0:x1, 1:x5
myBtns[1].value = True	# [X] 点灯
myBtns[5].value = True	# [x1]点灯



### ループ ############################################################
while True:
	
	# SWの取得
	for ii in range( 0, len( myBtns ), 2 ):	# 2ずつ増やす
		myBtns[ii].update()	#値の更新
		
		# ボタンが押されたときのイベント	
		if myBtns[ii].fell :
			myBtns[ii+1].value = True	# LED点灯	※消灯は条件ごと！

			# [X] が押された
			if ii == 0 :
				XY = 0
				myBtns[3].value = False	# Y LED消灯

			# [Y] が押された
			elif ii == 2 :
				XY = 1
				myBtns[1].value = False	# X LED消灯

			# [x1] が押された
			elif   ii == 4 :
				xx = 0
				myBtns[7].value = False			# x5 LED消灯
				kbd.send( Keycode.BACKSPACE )	# 文字を消して"1"を入力
				kbd.send( Keycode.ONE )			# 	※一文字を前提としている！	

			# [x5] が押された
			elif ii == 6 :
				xx = 1
				myBtns[5].value = False			# x1 LED消灯
				kbd.send( Keycode.BACKSPACE )	# 文字を消して”5”を入力
				kbd.send( Keycode.FIVE )		# 	※一文字を前提としている！

			# [home] が押された
			elif ii == 8 :
				kbd.send( Keycode.LEFT_CONTROL, Keycode.H )	# Ctl + H

			else :
				pass


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
	led[0] = rainbowio.colorwheel( int( 50 * time.monotonic() ) % 255  )	# LEDを虹色に変更
	led.show()  # LEDの値を変更後更新

	position_last = position 
