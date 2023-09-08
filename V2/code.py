"""
中華レーザー(K40 Whisperer)用のハンドホイールのプログラム
K40 Whispererのショートカット
	https://www.scorchworks.com/K40whisperer/k40w_manual.html#keyboard

［入力］
ボタン
 [X/Y]	ヘッドの移動軸（X/Y軸）を入れ替える
 [x1/5]	ヘッドの移動量（1/5mm）を　　〃
 [範囲]     各加工範囲端(左上、左下、右下、右上)に移動

ロータリーエンコーダ
　＋(時計回)　ヘッドの移動方向を軸に対して＋方向に移動
　－(反時計)　ヘッドの　　　　〃　　　　　－方向　〃
"""

import board, digitalio, usb_hid, time, keypad, rotaryio, neopixel, rainbowio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard import Keycode



### 関数 ############################################################
def myLED( num, Flag ) :
	global LEDst	# グローバル変数の読み込み
	if   Flag==True  : LEDst[num] = ( 100, 100, 255 ) # Blue
	elif Flag==False : LEDst[num] = ( 255, 100, 255 ) # Parple
	LEDst.show()



def myMove( num ) :
	for ii in range( num ) : kbd.send( Keycode.LEFT_SHIFT, Keycode.TAB ) # カーソル移動
	kbd.send( Keycode.SPACE ) # 範囲を押す
	for ii in range( num ) : kbd.send( Keycode.TAB )	# カーソル移動(戻)
	


def myInv( Flag ):
	Flag = not( Flag ) # 移動軸反転
	myLED( 0, Flag ) # インジゲータの更新



def myStep( Flag ) :
	# 既存の移動量削除
	for ii in range( 5 ) :
		kbd.send( Keycode.DELETE )		# 文字削除
		kbd.send( Keycode.BACKSPACE )	# 文字削除
	
	# 移動量の更新
	if   Flag==True  : kbd.send( Keycode.ONE )	# 1mm
	elif Flag==False : kbd.send( Keycode.FIVE )	# 5mm
	myInv( Flag )



### 初期設定 ############################################################
# キーボードのオブジェクト
kbd = Keyboard( usb_hid.devices )


# 入力(SW)    0 [X/Y]   1 [x1/5]  2 [左上]  3 [右上]  4 [左下]  5 [右下]
myPinsIN  = ( board.D3, board.D8, board.D5, board.D9, board.D4, board.D7 )
myBtns = keypad.Keys( myPinsIN, value_when_pressed=False, pull=True ) # ボタン化(Keypad使用)
XY = True	# True : X   False : Y
ST = True	# True : 1   False : 5


# Neopixelの制御
num_leds = 2		   # 信号端子, LEDの数,  明るさ
LEDob = neopixel.NeoPixel( board.NEOPIXEL, num_leds, brightness=0.05 )
LEDst = neopixel.NeoPixel( board.D0, num_leds, brightness=0.05 )
myLED( 0, XY )
myLED( 1, ST )


# エンコーダ
ledpin = digitalio.DigitalInOut( board.D6 )
ledpin.direction = digitalio.Direction.OUTPUT
ledpin.value = False # True（通常） ※今だけ！
encoder = rotaryio.IncrementalEncoder( board.D1, board.D2 ) # エンコーダの設定
position_last = None                                        # 初期値



### ループ ############################################################
while True:

	# ボタンを押したときのイベント
	myBtn = myBtns.events.get()
	if myBtn and myBtn.pressed :
		if   myBtn.key_number == 0 : myInv( XY )          # [X/Y]が押された場合
		elif myBtn.key_number == 1 : myStep( ST )        # [x1/5]が押された場合
		elif myBtn.key_number == 2 : myMove( num=5 )  # [左上]が押された場合
		elif myBtn.key_number == 3 : myMove( num=4 )  # [右上]が押された場合
		elif myBtn.key_number == 4 : myMove( num=2 )  # [左下]が押された場合
		elif myBtn.key_number == 5 : myMove( num=3 )  # [右下]が押された場合


	# ロータリーエンコーダーを回したときのイベント
	position = encoder.position	#値更新
	if not( position_last is None ) and ( position != position_last ) : #非初期値 かつ 値変更
		# 右移動 Ctrl + →
		if   ( XY==True )  and ( (position - position_last) > 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.RIGHT_ARROW )

		# 左移動 Ctrl + ←
		elif ( XY==True )  and ( (position - position_last) < 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.LEFT_ARROW )

		# 上移動 Ctrl + ↑
		elif ( XY==False ) and ( (position - position_last) > 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.UP_ARROW )

		# 下移動 Ctrl + ↓
		elif ( XY==False ) and ( (position - position_last) < 0 ) : kbd.send( Keycode.LEFT_CONTROL, Keycode.DOWN_ARROW )

	position_last = position #値保存
	
	LEDob[0] = rainbowio.colorwheel( int( 50 * time.monotonic() ) % 255 )
	LEDob.show()

