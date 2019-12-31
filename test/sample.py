from pycrawl import PyCrawl


url = 'https://tabelog.com/osaka/A2701/A270202/27107603/'
doc = PyCrawl(url)


#@ ========== データ抽出（例） ====================
doc.css('.display-name').innerText()
# => 焼肉どうらく 千日前店

doc.xpath('//*[@id="rstdtl-head"]/div[1]/section/div[1]/div[1]/div/h2/span').innerText()
# => 焼肉どうらく 千日前店

doc.css('.rdheader-rstname').css('a').attr('href')
# => https://tabelog.com/osaka/A2701/A270202/27107603/

doc.css('a')
# => ページ内<a>タグ全てを配列で返す

doc.tables['予約・お問い合わせ']
# => 050-5596-6465
# doc.tables：ページ内のtable属性を辞書として格納（自動）


#@ ========== ページ推移 ====================
doc.get('URL')


#@ ========== フォーム送信 ====================
doc.send(name='email', value='test@test.com')
doc.send(id='password', value='11111111')
doc.submit(name='loginForm')