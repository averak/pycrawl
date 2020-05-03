# -*- coding:utf-8 -*-
import mechanize
import lxml.html
import re


class pycrawl:
    def __init__(self, url=None, doc=None, html=None, user_agent=None, timeout=10):
        #--------------------------------------------
        # コンストラクタ
        # params:
        #   - url:str -> 対象サイトのURL
        #   - doc:lxml -> lxmlオブジェクト
        #   - html:str -> スクレイピングするHTML
        #   - user_agent:str -> user-agent
        #   - timeout:int -> read timeout sec
        #--------------------------------------------
        self.agent = mechanize.Browser()
        self.agent.keep_alive = False
        self.agent.set_handle_robots(False)

        # user-agent
        if user_agent is not None:
            browser.addheaders = [
                ('User-agent', user_agent),
            ]
        # timeout
        self.timeout = timeout
        # クエリパラメータを格納
        self.params = []

        # agentを設定
        ## 1. URLからagentを設定
        if url != None:
            self.get(url)
            return
        ## 2. docからagentを設定
        if doc != None:
            self.doc = doc
            self.html = self.outer_text()
            return
        ## 3. HTMLからagentを設定
        self.__update_params(html)


    def get(self, url):
        #--------------------------------------------
        # URLでアクセス
        # params:
        #   - url:str -> 対象サイトのURL
        #--------------------------------------------
        self.url = url
        page = self.agent.open(self.url, timeout)
        html = page.read().decode('utf-8')
        self.__update_params(html)


    def send(self, **opts):
        #--------------------------------------------
        # クエリパラメータをセット
        # params:
        #   - opts:dict -> フォームデータ
        #       - テキスト/数値    => (selector, value:string/int/float)
        #       - チェックボックス => (selector, check:bool)
        #       - ファイル         => (selector, file_name:str)
        #--------------------------------------------
        self.params.append({})
        for selector, value in opts.items():
            exec ('self.params[-1]['{0}'] = value'.format(selector))


    def submit(self, **opts):
        #--------------------------------------------
        # フォーム送信
        # params:
        #   - opts:dict -> {selector: name:str}
        #--------------------------------------------
        # フォームの選択
        for selector, value in opts.items():
            try:
                exec ('self.agent.select_form({0}='{1}')'.format(selector, value))
            except:
                return

        # フォームの送信
        for param in self.params:
            selector = list(param.keys())
            if 'value' in param:
                # テキスト，数値など
                selector.remove('value')
                selector = param[selector[0]]
                if param['value'] != None:
                    self.agent.form[selector] = param['value']
            if 'check' in param:
                # チェックボックス
                selector.remove('check')
                selector = param[selector[0]]
                if param['check'] != None:
                    self.agent.form[selector].selected = param['check']
            if 'file_name' in param:
                # チェックボックス
                selector.remove('file_name')
                selector = param[selector[0]]
                if param['file_name'] != None:
                    self.agent.form[selector].file_name = param['file_name']

        # 送信
        self.agent.submit()
        self.__update_params(self.agent.response().read().decode('utf-8'))


    def xpath(self, locator, single=False):
        #--------------------------------------------
        # XPathを指定しノードを抽出
        # params:
        #   - locator:str -> XPath
        #--------------------------------------------
        nodes = carray([pycrawl(doc=node) for node in self.doc.xpath(locator)])
        if single:
            # シングルノード
            if nodes == []:
                return carray()
            else:
                return nodes[0]
        else:
            # 複数ノード
            return nodes


    def css(self, locator, single=False):
        #--------------------------------------------
        # CSSセレクタを指定しノードを抽出
        # params:
        #   - locator:str -> css selector
        #--------------------------------------------
        nodes = carray([pycrawl(doc=node) for node in self.doc.cssselect(locator)])
        if single:
            # シングルノード
            if nodes == []:
                return carray()
            else:
                return nodes[0]
        else:
            # 複数ノード
            return nodes


    def attr(self, name):
        #--------------------------------------------
        # ノードの属性情報を抽出
        # params:
        #   - name:str -> node's attribute
        #--------------------------------------------
        if name in self.doc.attrib:
            return self.doc.attrib[name]
        else:
            return None


    def inner_text(self, shaping=True):
        #--------------------------------------------
        # タグ内の文字列を抽出
        # params:
        #   - shaping:bool -> 文字列を整形するか
        #--------------------------------------------
        if shaping:
            return self.__shaping_string(self.doc.text_content())
        else:
            return self.doc.text


    def outer_text(self):
        #--------------------------------------------
        # タグ内の文字列を抽出
        #--------------------------------------------
        return lxml.html.tostring(self.doc, encoding='utf-8').decode('utf-8')


    def __update_params(self, html):
        #--------------------------------------------
        # パラメータを更新
        # params:
        #   - html:str -> HTML
        #--------------------------------------------
        self.url = self.agent.geturl()
        if html == None or html == '':
            html = '<html></html>'
        self.html = html
        self.doc = lxml.html.fromstring(self.html)
        self.__table_to_dict()


    def __table_to_dict(self):
        #--------------------------------------------
        # table属性をDictに格納
        #--------------------------------------------
        self.tables = {}

        for tr in self.doc.cssselect('tr'):
            if tr.cssselect('th') != [] and tr.cssselect('td') != []:
                key = self.__shaping_string(tr.cssselect('th')[0].text_content())
                value = self.__shaping_string(tr.cssselect('td')[0].text_content())
                self.tables[key.replace('\n', '').replace(' ', '')] = value
        for dl in self.doc.cssselect('dl'):
            if dl.cssselect('dt') != [] and dl.cssselect('dd') != []:
                key = self.__shaping_string(dl.cssselect('dt')[0].text_content())
                value = self.__shaping_string(dl.cssselect('dd')[0].text_content())
                self.tables[key.replace('\n', '').replace(' ', '')] = value


    def __shaping_string(self, text):
        #--------------------------------------------
        # 文字列を整形
        # params:
        #   - text:str -> 整形対象の文字列
        #--------------------------------------------
        # 余分な改行，空白を全て削除
        text = str(text)
        text = text.replace(' ', ' ')
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('\n \n', '\n').replace('\n ', '\n').replace('\r', '\n')
        text = re.sub(r'\n+', '\n', text)
        return text.replace('\t', '').strip()