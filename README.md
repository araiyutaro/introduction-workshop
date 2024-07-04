## 導入ワークショップ

### 企業ホームページのテキストマイニング
 - sele.py  
基本的にこのファイルだけ見ればOK。  
URLを入力すると、Seleniumを使用してWebサイトの情報取得→Spacy,Ginzaでテキストを品詞分解→単語リスト作成する  
**事前に以下を実行し、それぞれのライブラリをインストールする必要あり**
```
pip install -U pip setuptools wheel
pip install -U spacy
pip install ja-ginza
pip install publicsuffix2
pip install -U selenium
```

### その他のファイルについて
 - mining.py  
Spacy+Ginzaの実験の残骸
 - g.py  
有報のPDFから単語を抽出するプログラム、第３回の時点で作ったもの
 - soup.py  
WebサイトのスクレイピングにBeautifulSoupというライブラリを使ってみた時の残骸。  
このライブラリはJSで動的に作られているWebサイトの場合テキストが取得出来ないことがあるため、Seleniumを採用した。