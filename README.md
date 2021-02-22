# 坂道ナビ

車椅子やベビーカーの利用者のための「坂道ナビ」

## 実行方法

Python3.xで開発しています．
実行には下記のライブラリなどが必要となります．
Mapboxのアクセス・トークンはRouteManager.pyに記述してください．

- [Mapbox アクセス・トークン](https://www.mapbox.com/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Open JTalk](http://open-jtalk.sp.nitech.ac.jp/)

実行の際は下記のコマンドを入力します．

```
$ python WebEasyRouteMap.py
```

Webサーバが起動したら，ブラウザで http://127.0.0.1:5000/ にアクセスしてください．

## 操作方法

スタート・マーカー（赤色）とゴール・マーカー（緑色）をドラッグして自由に移動させてください．
移動後，自動的に経路が再計算され，ナビゲーション音声も生成されます．

## デモ・ムービー

[![Image from Gyazo](https://i.gyazo.com/18283407ec911638e3ec4f496444b579.jpg)](https://youtu.be/w3WbhEtJ3tM)
