# 中華レーザー用のハンドホイール
カメラ搭載のレーザー加工機では、ワークの位置決めが容易に行うことができる。  
しかし、ウチにある中華レーザーにはそのような機能は、搭載されていない。  
そこで、


うちにある中華レーザーは、を **K40 Whisperer** でコントロールしている。  
ハニカム台を使用しておらず、また位置決めとなる基準治具もない（めんどくさがっているだけ）。  
加工時は、アクリル板などのワークを加工スペースにおいた後で、ヘッドの位置決めを行っている。  
そのため、**K40 Whisperer** によるヘッドの移動を誤るとレーザーがワークから出てしまうことになりかねない。  

そこで、ヘッドの位置決めを行いやすくするために、専用のハンドホイールを作製した。  
マイコンのＨＩＤで**K40 Whisperer**のショートカットを出力させた簡易的なモノであるが、中華レーザーとパソコンを見比べながら作業する必要がなくなった。  
マイコンの種類によって、ファームウェアやアサインによるコードが異なるが、記録として残しておく。  

過去に作成したハンドホイールに関する情報は、上記の`V1`にデータを保存している。  


![image](https://github.com/T-zakisan/HandWheel_for_ChinaLASER/assets/43605763/040b6fec-b678-46f0-9a54-03511e38b134)




## [K40 Whispererのショートカット](https://www.scorchworks.com/K40whisperer/k40w_manual.html#keyboard)
下表に **K40 Whisperer** のショートカットを示す。  
ショートカットの内 :+1: マークのある項目の実装を行った。  
なお、**カーソル移動方法**は、カーソルが`Jog Step`にある場合とする。　　

| | ショートカット | 内容 |
|----|:----|:----| 
| | F1 | Open the Help dialog box. |
| | F2 | Opens General Settings Window |
| | F3 | Opens Raster Settings Window |
| | F4 | Opens Advanced Settings |
| | F5 | Refreshes items displayed in the main window. |
| | Home (or Ctrl-h) | Home Laser |
| :+1: | Ctrl-Up Arrow | Jog Laser up |
| :+1: | Ctrl-Down Arrow | Jog Laser Down |
| :+1: | Ctrl-Right Arrow | Jog Laser Right |
| :+1: | Ctrl-Left Arrow | Jog Laser Left |
| | Ctrl-i | Initialize Laser |

| | 加工範囲 | カーソル移動方法 |
|----|:----|:----| 
| :+1: | 左上端 | Shift+Tab ５回 → Space |
| :+1: | 右上端 | Shift+Tab ４回 → Space |
| :+1: | 右下端 | Shift+Tab ３回 → Space |
| :+1: | 左下端 | Shift+Tab ２回 → Space | 



## 機能 
**ロータリーエンコーダ** を回転させた分だけ、下記ボタンの状態によって移動する  
ただし、左上、右上、右下、左下ボタンを押すとそれぞれの加工範囲端にヘッドが移動する

### 移動方向
**[ X/Y ]**	レーザーヘッドの移動軸（**Ｘ軸**と**Ｘ軸**）を入れ替える

### 移動量
レーザーヘッドの移動量（**１ｍｍと５ｍｍ**）を入れ替える  

![ボタン説明](https://github.com/T-zakisan/HandWheel_for_ChinaLASER/assets/43605763/626807e6-1676-4a8c-b97e-5f45009a2538)



# 作成方法
## パーツリスト
| パーツ名 | 備考 |
|:----|:----|
| [Seeed Xiao RP2040](https://akizukidenshi.com/catalog/g/gM-17044/) |  |
| [LED付ロータリーエンコーダー（青）ツマミ付セット](https://akizukidenshi.com/catalog/g/gP-05768/) ||
| [ロータリーエンコーダDIP化基板　RECNV‐1](https://akizukidenshi.com/catalog/g/gP-07239/) ||
| [タクトスイッチ](https://akizukidenshi.com/catalog/g/gP-08073/) | ４個 |
| [タクトスイッチ](/) | ２個（側面用） |
| [ユニバーサル基板　Cタイプ(72×47mm)](https://akizukidenshi.com/catalog/g/gP-09747/) |  |
| []() |  |
| []() |  |
| []() |  |
| [SK6812使用マイコン内蔵フルカラーテープLED 1m 60LED IP20](https://akizukidenshi.com/catalog/g/gM-12982/) | LED２個使用(以降LEDテープ)|


## アサイン
ここでは、マイコンが[Seeed Xiao RP2040](https://akizukidenshi.com/catalog/g/gM-17044/)の場合とする。  

| マイコン端子 | パーツ端子 |
|:----:|:----|
| 3V3 | LEDテープ \(+\)|
| GND | ロータリーエンコーダ(C,LED-), 各スイッチ(-), LEDテープ(-) |
| 1 |  ロータリーエンコーダ |
| 2 |  ロータリーエンコーダ |
| 3 | [x/y] \(SW+\) |
| 4 | [左上] \(SW+\) |
| 5 | [左下] \(SW+\) |
| 6 |  ロータリーエンコーダ \(LED+\) |
| 7 | [右下] \(SW+\) |
| 8 | [1/5] \(SW+\) |
| 9 | [右上] \(SW+\) |
| 10 | LEDテープ \(Din\)|
| NEOPIXEL | オンボード |



## 必須ライブラリ
マイコン種によっては、[CircuitPythonのライブラリ](https://circuitpython.org/libraries)の全てを保存することができない。   
ここでは、使用する最低限のライブラリをリストアップしておく。  
少なくとも以下のライブラリは、***lib/*** に保存する必要がある。
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





      

