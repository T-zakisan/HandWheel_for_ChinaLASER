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
