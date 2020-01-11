# -*- coding:utf-8 -*-
import mechanize
import lxml.html
import re


class PyCrawl:
    # 特殊配列
    class CrawList(list):
        def xpath(self, locator, single=False):
            if self != []:
                return self[0].xpath(locator, single)
            else:
                return PyCrawl(doc=None).xpath(locator, single)

        def css(self, locator, single=False):
            if self != []:
                return self[0].css(locator, single)
            else:
                return PyCrawl(doc=None).css(locator, single)

        def attr(self, name):
            if self != []:
                return self[0].attr(name)
            else:
                return PyCrawl(doc=None).attr(name)

        def inner_text(self, shaping=True):
            if self != []:
                return self[0].inner_text(shaping)
            else:
                return PyCrawl(doc=None).inner_text(shaping)

        def outer_text(self):
            if self != []:
                return self[0].outer_text()
            else:
                return PyCrawl(doc=None).outer_text()

    def __init__(self, url=None, doc=None, html=None):
        ## -----*----- コンストラクタ -----*----- ##
        self.agent = mechanize.Browser()
        self.agent.set_handle_robots(False)

        if url != None:
            # urlを受け取り
            self.get(url)
        elif doc != None:
            # docを受け取り
            self.doc = doc
            self.html = self.outer_text()
            self.__table_to_dict()
        else:
            # htmlを受け取り
            self.__update_params(html)

        # 送信するデータを格納
        self.params = []

    def get(self, url):
        ## -----*----- ページ推移 -----*----- ##
        self.url = url
        page = self.agent.open(self.url)
        html = page.read().decode('utf-8')
        self.__update_params(html)

    def send(self, **opts):
        ## -----*----- フォームデータ指定 -----*----- ##
        #
        # テキスト，数値など　  => value（String）を指定
        # チェックボックス　　  => check（Bool）を指定
        # ファイルアップロード  => file_name（String）を指定
        self.params.append({})
        for key, value in opts.items():
            exec ('self.params[-1]["{0}"] = value'.format(key))

    def submit(self, **opts):
        ## -----*----- フォーム送信 -----*----- ##
        # フォームの選択
        for key, value in opts.items():
            try:
                exec ('self.agent.select_form({0}="{1}")'.format(key, value))
            except:
                return

        # フォームの送信
        for param in self.params:
            selecter = list(param.keys())
            if 'value' in param:
                # テキスト，数値など
                selecter.remove('value')
                selecter = param[selecter[0]]
                if param['value'] != None:
                    self.agent.form[selecter] = param['value']
            if 'check' in param:
                # チェックボックス
                selecter.remove('check')
                selecter = param[selecter[0]]
                if param['check'] != None:
                    self.agent.form[selecter].selected = param['check']
            if 'file_name' in param:
                # チェックボックス
                selecter.remove('file_name')
                selecter = param[selecter[0]]
                if param['file_name'] != None:
                    self.agent.form[selecter].file_name = param['file_name']

        # 送信
        self.agent.submit()
        self.__update_params(self.agent.response().read().decode('utf-8'))

    def xpath(self, locator, single=False):
        ## -----*----- HTMLからXPath指定で要素取得 -----*----- ##
        elements = self.CrawList([PyCrawl(doc=node) for node in self.doc.xpath(locator)])
        if single:
            # シングルノード
            if elements == []:
                return self.CrawlList()
            else:
                return elements[0]
        else:
            # 複数ノード
            return elements

    def css(self, locator, single=False):
        ## -----*----- HTMLからCSSセレクタで要素取得 -----*----- ##
        elements = self.CrawList([PyCrawl(doc=node) for node in self.doc.cssselect(locator)])
        if single:
            # シングルノード
            if elements == []:
                return self.CrawlList()
            else:
                return elements[0]
        else:
            # 複数ノード
            return elements

    def attr(self, name):
        ## -----*----- ノードの属性情報取得 -----*----- ##
        if name in self.doc.attrib:
            return self.doc.attrib[name]
        else:
            return ''

    def inner_text(self, shaping=True):
        ## -----*----- タグ内（タグ除く）の文字列を取得 -----*----- ##
        if shaping:
            return self.__shaping_string(self.doc.text_content())
        else:
            return self.doc.text

    def outer_text(self):
        ## -----*----- タグ内（タグ含む）の文字列を取得 -----*----- ##
        return lxml.html.tostring(self.doc, encoding="utf-8").decode('utf-8')

    def __update_params(self, html):
        ## -----*----- パラメータを更新 -----*----- ##
        if html == None or html == '':
            html = '<html></html>'
        self.html = html
        self.url = self.agent.geturl()
        self.doc = lxml.html.fromstring(self.html)
        self.__table_to_dict()

    def __table_to_dict(self):
        ## -----*----- テーブル内容をDictに変換 -----*----- ##
        self.tables = {}
        for tr in self.doc.cssselect('tr'):
            if tr.cssselect('th') != [] and tr.cssselect('td') != []:
                key = self.__shaping_string(tr.cssselect('th')[0].text_content())
                value = self.__shaping_string(tr.cssselect('td')[0].text_content())
                self.tables[key.replace("\n", "").replace(" ", "")] = value
        for dl in self.doc.cssselect('dl'):
            if dl.cssselect('dt') != [] and dl.cssselect('dd') != []:
                key = self.__shaping_string(dl.cssselect('dt')[0].text_content())
                value = self.__shaping_string(dl.cssselect('dd')[0].text_content())
                self.tables[key.replace("\n", "").replace(" ", "")] = value

    def __shaping_string(self, text):
        ## -----*----- 文字例の整形 -----*----- ##
        # 余分な改行，空白を全て削除
        text = str(text)
        text = text.replace(" ", ' ')
        text = re.sub(r"\s+", ' ', text)
        text = text.replace("\n \n", "\n").replace("\n ", "\n").replace("\r", "\n")
        text = re.sub(r"\n+", "\n", text)
        return text.replace("\t", "").strip()