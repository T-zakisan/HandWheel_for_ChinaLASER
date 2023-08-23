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
myPinsIN  = ( board.GP9, board.GP6, board.GP21, board.GP24, board.GP0 )
myBtns = keypad.Keys( myPinsIN, value_when_pressed=False, pull=True )	# ボタン化(Keypad使用)

# 出力(LED)   0 [Y]      1 [x5]     2 [X]       3 [x1]      4 [NeoP…]  5 [RotaryEncoder]
myPinsOUT = ( board.GP8, board.GP7, board.GP22, board.GP23, board.GP18, board.GP16 )
myLEDs = []
for ii, pin in enumerate( myPinsOUT ) :		# enumerate(添字)込みの繰り返し
	tmp_pin = digitalio.DigitalInOut( pin )	# 端子の指定	
	tmp_pin.direction = digitalio.Direction.OUTPUT	# 出力
	myLEDs.append( tmp_pin )						# LED　※Debouncer不要
	if ii > 1 : myLEDs[ii].value = True
XY = True	# 状態(  軸  ) => True:X,  Fales:Y


# Neopixelの制御
num_leds = 3		  #( 信号端子  , LEDの数 , 明るさ         )
led = neopixel.NeoPixel( board.GP17, num_leds, brightness=0.1 )


# エンコーダ
encoder = rotaryio.IncrementalEncoder( board.GP15, board.GP14 )	# エンコーダの設定
position_last = None											# 初期値


### 関数 ############################################################
def myChange( num1, num2, Flag, chr ) :
	global XY
	myLEDs[num1].value = True
	myLEDs[num2].value = False
	if Flag==True :
		for ii in range( 5 ) :
			kbd.send( Keycode.BACKSPACE )	# 文字を消去
			kbd.send( Keycode.DELETE )		# 文字を消去
		kbd.send( chr )				# １を入力
	elif Flag==False :
		if   num1==2 : XY = True
		elif num1==0 : XY = False


### ループ ############################################################
while True:

	# ボタンを押したときのイベント
	myBtn = myBtns.events.get()
	if myBtn and myBtn.pressed :

		# [X]が押された場合
		if   myBtn.key_number == 2 : myChange( num1=2, num2=0, Flag=False, chr="null" )

		# [Y]が押された場合
		elif myBtn.key_number == 0 : myChange( num1=0, num2=2, Flag=False, chr="null" )

		# [x1]が押された場1
		elif myBtn.key_number == 3 : myChange( num1=3, num2=1, Flag=True, chr=Keycode.ONE )

		# [x5]が押された場合
		elif myBtn.key_number == 1 : myChange( num1=1, num2=3, Flag=True, chr=Keycode.FIVE )

		# [home]が押された場合
		elif myBtn.key_number == 4 : kbd.send( Keycode.LEFT_CONTROL, Keycode.H )	# Ctl + H

	# ロータリーエンコーダーを回したときのイベント
	position = encoder.position	#値更新
	if not( position_last is None ) and ( position != position_last ) :	#非初期値 かつ 値変更

		# 右移動 Ctrl + →
		if   ( XY == True )  and ( (position - position_last) > 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.RIGHT_ARROW )

		# 左移動 Ctrl + ←
		elif ( XY == True )  and ( (position - position_last) < 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.LEFT_ARROW )

		# 上移動 Ctrl + ↑
		elif ( XY == False ) and ( (position - position_last) > 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.UP_ARROW )
	
		# 下移動 Ctrl + ↓
		elif ( XY == False ) and ( (position - position_last) < 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.DOWN_ARROW )

	position_last = position	#値保存
	

	# NeoPixcelの色変更
	for ii in range( num_leds ) : led[ii] = rainbowio.colorwheel( int( 50 * time.monotonic() ) % 255  )	# LEDをエンコーダ値で虹色に変更
	led.show()  # LEDの値を変更後更新
