# 中華レーザー用のハンドホイール
中華レーザー（K40 Whisperer）用のハンドホイールをHIDで作成した。  
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


## アサイン
ここでは、マイコンが[RP2040マイコンボードキット](https://akizukidenshi.com/catalog/g/gK-17542/)の場合とする。  
※各スイッチ(LED)は、電流調整用の抵抗(1kΩ)を接続のこと！
| マイコン端子 | パーツ端子 |
|:----:|:----|
| 5V | ロータリーエンコーダ(LED+) |
| GND | ロータリーエンコーダ(C,LED-), 各スイッチ(-), NeoPixcel(-) |
| 0 | [home] \(SW+\) |
| 1 | [x5] \(SW+\) |
| 2 | [x5] \(LED+\) |
| 3 | [Y] \(SW+\) |
| 4 | [Y] \(LED+\) |
| 14 | ロータリーエンコーダ(A) |
| 15| ロータリーエンコーダ(B) |
| 16 | ロータリーエンコーダ(LED+) |
| 17 | [NeoPixcel] \(Di\) |\
| 18 | [NeoPixcel] \(+5V\) |\
| 25 | [X] \(SW+\) |
| AD0(26) | [X] \(LED+\) |
| AD1(27) | [x1] \(SW+\) |
| AD2(28) | [x1] \(LED+\) |

