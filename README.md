# 中華レーザー用のハンドホイール
うちにある中華レーザーは、を **K40 Whisperer** でコントロールしている。
ハニカム台を使用しておらず、また位置決めとなる基準治具もない（めんどくさがっているだけ）。　  
加工時は、アクリル板などのワークを加工スペースにおいた後で、ヘッドの位置決めを行っている。  
そのため、**K40 Whisperer** によるヘッドの移動を謝るとレーザーがワークから出てしまうことになりかねない。  

そこで、ヘッドの位置決めを行いやすくするために、専用のハンドホイールを作製した。  
マイコンのＨＩＤで**K40 Whisperer**のショートカットを出力させた簡易的なモノであるが、中華レーザーとパソコンを見比べながら作業する必要がなくなった。  
マイコンの種類によって、ファームウェアやアサインによるコードが異なるが、記録として残しておく。



## [K40 Whispererのショートカット](https://www.scorchworks.com/K40whisperer/k40w_manual.html#keyboard)
下表に **K40 Whisperer** のショートカットを示す。  
ショートカットの内 :+1: マークのある項目の実装を行った。

| | ショートカット | 内容 |
|----|:----|:----| 
| | F1 | Open the Help dialog box. |
| | F2 | Opens General Settings Window |
| | F3 | Opens Raster Settings Window |
| | F4 | Opens Advanced Settings |
| | F5 | Refreshes items displayed in the main window. |
| :+1: | Home (or Ctrl-h) | Home Laser |
| :+1: | Ctrl-Up Arrow | Jog Laser up |
| :+1: | Ctrl-Down Arrow | Jog Laser Down |
| :+1: | Ctrl-Right Arrow | Jog Laser Right |
| :+1: | Ctrl-Left Arrow | Jog Laser Left |
| | Ctrl-i | Initialize Laser |



## 機能 
**ロータリーエンコーダ** を回転させた分だけ、下記ボタンの状態によって移動する

### 移動方向
**[ X ]**	レーザーヘッドを**Ｘ軸**に移動  
**[ Y ]** レーザーヘッドを**Ｙ軸**に移動  

### 移動量
**[ x1 ]** ヘッドの移動距離を**１ｍｍ**  
**[ x5 ]** ヘッドの移動距離を**５ｍｍ**  

### ホーミング（初期位置）
**[ home ]** レーザーヘッドをホーミング  


# 作成方法
## パーツリスト
| パーツ名 | 備考 |
|:----|:----|
| [RP2040マイコンボードキット](https://akizukidenshi.com/catalog/g/gK-17542/) | HIDが実装できいるマイコンであれば何でもよい |
| [LED付ロータリーエンコーダー（青）ツマミ付セット](https://akizukidenshi.com/catalog/g/gP-05768/) ||
| [ロータリーエンコーダDIP化基板　RECNV‐1](https://akizukidenshi.com/catalog/g/gP-07239/) ||
| [LED照光式タクトスイッチ　青　キートップ付き](https://akizukidenshi.com/catalog/g/gP-13871/) | ５個，ボタンを押した際に状態のOn/OffをLEDの点灯状態で示す |
| [ユニバーサル基板　Cタイプ(72×47mm)](https://akizukidenshi.com/catalog/g/gP-09747/) | ２枚重ねにして使用 |
| [ピンヘッダ 1x40 (40P)](https://akizukidenshi.com/catalog/g/gC-00167/) | ユニバーサル基板を上下で接続 |
| [分割ロングピンソケット 1x42 (42P)](https://akizukidenshi.com/catalog/g/gC-05779/) | 上記同様 |
| [カーボン抵抗（炭素皮膜抵抗） 1/6W1ｋΩ](https://akizukidenshi.com/catalog/g/gR-16102/) | ４個, SW付属のLED(電流調整)用 |
| [SK6812使用マイコン内蔵フルカラーテープLED 1m 60LED IP20](https://akizukidenshi.com/catalog/g/gM-12982/) | LED３個使用(以降NeoPixcel)|


## アサイン
ここでは、マイコンが[RP2040マイコンボードキット](https://akizukidenshi.com/catalog/g/gK-17542/)の場合とする。  
※各スイッチ(LED)は、電流調整用の抵抗(1kΩ)を接続のこと！
※ロータリーエンコーダ(LED+)とNeoPixcel(+5V)は、配線の取り回しの関係でGPIOから3.3Vを供給！
| マイコン端子 | パーツ端子 |
|:----:|:----|
| GND | ロータリーエンコーダ(C,LED-), 各スイッチ(-), NeoPixcel(-) |
| 0 | [home] \(SW+\) |
| 6 | [x5] \(SW+\) |
| 7 | [x5] \(LED+\) |
| 8 | [Y] \(LED+\) |
| 9 | [Y] \(SW+\) |
| 14 | ロータリーエンコーダ(A) |
| 15| ロータリーエンコーダ(B) |
| 16 | ロータリーエンコーダ(LED+) |
| 17 | [NeoPixcel] \(Di\) |\
| 18 | [NeoPixcel] \(+5V\) |\
| 21 | [X] \(SW+\) |
| 22 | [X] \(LED+\) |
| 23 | [x1] \(LED+\) |
| 24 | [x1] \(SW+\) |



## 必須ライブラリ
マイコン種によっては、[CircuitPythonのライブラリ](https://circuitpython.org/libraries)の全てを保存することができない。   
ここでは、使用する最低限のライブラリをリストアップしておく。  
少なくとも以下のライブラリは、**lib/** に保存する必要がある。
| ライブラリ名 | 備考 |
|:----|:----:|
| /adafruit_hid | ディレクトリごとコピー |
| neopixel.mpy |  |


# 使用方法
1. 中華レーザーを起動
2. **ハンドホイール** をＰＣに接続
3. **K40 Whisperer** を起動
4. **K40 Whisperer** の **Jog Step [ ]mm** にカーソルを合わせる
5. **[Initialize Laser Cutter]** を押して、初期化
6. ハンドホイールを使用し、位置をコントロール


# 反省点
X/Y、x1/x5は、それぞれ状態が２つであるため、切り替えをボタン１つでおこなえばよかった。  
そうすることにより、ボタンの数を減らすことができ、パーツ数、配線を減らすことができ、コストも当然抑えることができる。  
また、プログラムもいくらか簡略化できただろう。


以上




      
