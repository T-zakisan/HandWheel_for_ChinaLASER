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

import board, digitalio, usb_hid, time, keypad, rotaryio, neopixel,  rainbowio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard import Keycode

### 初期設定 ############################################################

# キーボードのオブジェクト
kbd = Keyboard( usb_hid.devices )


# 入力(SW)    0 [Y]      1 [x5]     2 [X]       3 [x1]      4 [HOME]
myPinsIN  = ( board.GP3, board.GP1, board.GP25, board.GP27, board.GP0 )
myBtns = keypad.Keys( myPinsIN, value_when_pressed=False, pull=True )	# ボタン化(Keypad使用)

# 出力(LED)   0 [Y]      1 [x5]     2 [X]       3 [x1]      4 [NeoP…]  5 [RotaryEncoder]
myPinsOUT = ( board.GP4, board.GP2, board.GP26, board.GP28, board.GP18, board.GP16 )
myLEDs = []
for ii, pin in enumerate( myPinsOUT ) :		# enumerate(添字)込みの繰り返し
	tmp_pin = digitalio.DigitalInOut( pin )	# 端子の指定	
	tmp_pin.direction = digitalio.Direction.OUTPUT	# 出力
	myLEDs.append( tmp_pin )						# LED　※Debouncer不要
	if ii > 2 : myLEDs[ii].value = True		
XY = 0	# 状態(  軸  ) => 0:X,  1:Y


# Neopixelの制御
num_leds = 3		  #( 信号端子  , LEDの数 , 明るさ         )
led = neopixel.NeoPixel( board.GP17, num_leds, brightness=0.2 )


# エンコーダ
encoder = rotaryio.IncrementalEncoder( board.GP15, board.GP14 )	# エンコーダの設定
position_last = None											# 初期値



### ループ ############################################################
while True:

	# ボタンを押したときのイベント
	myBtn = myBtns.events.get()
	if myBtn and myBtn.presed :
		
		# [X]が押された場合
		if myBtn.key_number == 2 :
			XY == 0
			myLEDs[2].value = True	# X LED点灯
			myLEDs[0].value = False	# Y LED消灯

		# [Y]が押された場合
		elif myBtn.key_number == 0 :
			XY == 1
			myLEDs[2].value = False	# X LED消灯
			myLEDs[0].value = True	# Y LED点灯

		# [x1]が押された場合
		elif myBtn.key_number == 3 :
			myBtns[3].value = True			# x1 LED点灯
			myBtns[1].value = False			# x5 LED消灯
			kbd.send( Keycode.BACKSPACE )	# 文字を消して"1"を入力
			kbd.send( Keycode.ONE )			# 	※一文字を前提としている！

		# [x5]が押された場合
		elif myBtn.key_number == 1 :
			myBtns[3].value = False			# x1 LED消灯
			myBtns[1].value = True			# x5 LED点灯
			kbd.send( Keycode.BACKSPACE )	# 文字を消して”5”を入力
			kbd.send( Keycode.FIVE )		# 	※一文字を前提としている！

		# [home]が押された場合
		elif myBtn.key_number == 4 :
			kbd.send( Keycode.LEFT_CONTROL, Keycode.H )	# Ctl + H


	# ロータリーエンコーダーを回したときのイベント
	position = encoder.position	#値更新
	if not( position_last is None ) and ( position != position_last ) :	#非初期値 かつ 値変更

		# 右移動 Ctrl + →
		if   ( XY == 0 ) and ( (position - position_last) > 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.RIGHT_ARROW )

		# 左移動 Ctrl + ←
		elif ( XY == 0 ) and ( (position - position_last) < 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.LEFT_ARROW )

		# 上移動 Ctrl + ↑
		elif ( XY == 1 ) and ( (position - position_last) > 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.UP_ARROW )
	
		# 下移動 Ctrl + ↓
		elif ( XY == 1 ) and ( (position - position_last) < 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.DOWN_ARROW )

	position_last = position	#値保存
	

	# NeoPixcelの色変更
	for ii in range( num_leds ) : led[ii] = rainbowio.colorwheel( int( 50 * time.monotonic() ) % 255  )	# LEDをエンコーダ値で虹色に変更
	led.show()  # LEDの値を変更後更新
