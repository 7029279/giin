# giin
国会議員データのスクレイピング、統計 in java, python. Data scraping and statistical analysis of Japanese lawmakers

１．衆議院ホームページから現職議員のリストをスクレイピングしました。（特に利点はないですがJavaが書きたかったのでJsoupとJackson使いました）

２．リスト化した一人ひとりを wikipediaで検索して学歴、有名な親族、前職のデータをスクレイピング（ここもJava）

3. pythonでanalyzerを書きました。

どういった経歴やバックグラウンドの人が政治家として成功しやすいかを分析しました。主に２種類の分析方法を試してみましたがどちらでも”政治家としての成功”は再選回数/（年齢ー２５）としました（２５歳が衆院の被選挙権なため）。この値で測るのが正しいのかは異論かなりあると思いますがデータが手っ取り早く手に入るのがこれだったのでこれ使いました。

まずsimpleplotの方は院卒か、大学で政治の勉強したか、身内に経営者や政治家がいるか、過去に政治家の秘書、記者、弁護士、国家公務員やっていたかなどの項目とをregressionしてみました。相関係数がどれも０．１以下でplotしたものも相関が見えづらいのでこちらは失敗っぽいです。


bio()のほうはMecabとK-meansで学歴、親族、職歴をクラスタリングしています。plotではk-meansの二次元に圧縮したものをXY軸で、再選回数/（年齢ー２５）をZ軸にして三次元scatter図を描きました。
上の方にあるGroup1-5はそれぞれのクラスタのメンバー数（ｎ）、平均のZ値[再選回数/（年齢ー２５）]（avg cons.）（これが高いほどこのクラスタは政治的に成功していることになります）、例として三名のクラスタメンバーの経歴。

現国会議員全員でやったものに加え、地域別、政党別でやったものもあります。

plotしたものは画像として一つずつplot-imagesに入ってますが、pdfにまとめたものの方が見やすいです。
(https://github.com/7029279/giin/blob/master/test/bio.pdf)
(https://github.com/7029279/giin/blob/master/test/simpleplot.pdf)


クラスタリングしたものの中で面白いと思ったのをいくつか画像でピックアップしてみました。
![bio-2dimensions-education-日本-all](https://user-images.githubusercontent.com/28686892/72840999-13cb4300-3c5b-11ea-8c96-ae1f6b9036fa.png)
まず全衆議院議員のを見てみるとクラスタ３が慶応でクラスタ１が早稲田になってますが、慶応の方が再選回数しやすいことがわかります。クラスタ２の東大と同じレベルです。


![bio-2dimensions-previously-日本-all](https://user-images.githubusercontent.com/28686892/72841051-31001180-3c5b-11ea-9134-b67ff8d9acf3.png)
職歴ではきれいに１地方議員　２国家公務員　３秘書　４弁護士に分かれてます。　国家公務員と秘書が政治キャリアに有利な様です。



![bio-2dimensions-previously-日本-自民](https://user-images.githubusercontent.com/28686892/72841275-abc92c80-3c5b-11ea-8543-bf3668cafb62.png)
自民党内では国家公務員よりも民間企業社員のほうがZ値の平均が高いです。また、地方議員より、国会議員の秘書のほうが圧倒的に再選しやすいようです。



![bio-2dimensions-previously-日本-立国社](https://user-images.githubusercontent.com/28686892/72841261-a1a72e00-3c5b-11ea-96e6-467a76c8167a.png)
立国社はリベラル系野党３党ですが、自民党に比べて全体的にZ値が低い、つまり再選回数が少ない人が多いです。



![bio-2dimensions-education-比例-all](https://user-images.githubusercontent.com/28686892/72841493-1e3a0c80-3c5c-11ea-9dc8-1c4d4086c4af.png)
比例で当選した議員の中では、東大、早稲田、院卒組クラスタを抑えて創価大学出身者（group1）の平均Z値が一番高いです。公明党は比例で強いというのがよくわかります。

