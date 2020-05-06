# -*- coding:utf-8 -*-
import mechanize
import lxml.html
import re
from .carray import carray


class pycrawl:
    def __init__(self, url=None, doc=None, html=None, user_agent=None, timeout=10, encoding='utf-8'):
        #--------------------------------------------
        # コンストラクタ
        # params:
        #   - url:str -> 対象サイトのURL
        #   - doc:lxml -> lxmlオブジェクト
        #   - html:str -> スクレイピングするHTML
        #   - user_agent:str -> user-agent
        #   - timeout:int -> read timeout sec
        #   - encoding:str -> read encoding
        #--------------------------------------------
        self.agent = mechanize.Browser()
        self.agent.keep_alive = False
        self.agent.set_handle_refresh(False)
        self.agent.set_handle_equiv(False)
        self.agent.set_handle_robots(False)

        # user-agent
        if user_agent is not None:
            self.agent.addheaders = [
                ('User-agent', user_agent),
            ]
        # timeout
        self.timeout = timeout
        # encoding
        self.encoding = encoding
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
        page = self.agent.open(self.url, timeout=self.timeout)
        html = page.read().decode(self.encoding, 'ignore')
        self.__update_params(html)


    def send(self, **opts):
        #--------------------------------------------
        # クエリパラメータをセット
        # params:
        #   - opts:dict -> フォームデータ
        #       - テキスト/数値    => (selector, value:string/int/float)
        #       - チェックボックス => (selector, check:bool)
        #       - ファイル         => (selector, file_name:str)
        #       - selector => name / id / type / nr / label / kind / predicate
        #--------------------------------------------
        self.params.append({})
        for selector, value in opts.items():
            exec('self.params[-1]["%s"] = value' % selector)


    def submit(self, **opts):
        #--------------------------------------------
        # フォーム送信
        # params:
        #   - opts:dict -> {selector: name:str}
        #       - selector => id, class_, name, nr...
        #--------------------------------------------
        # フォームの選択
        for selector, value in opts.items():
            if isinstance(value, int):
                exec('self.agent.select_form(%s=%d)' % (selector, value))
            else:
                exec('self.agent.select_form(%s="%s")' % (selector, value))

        self.agent.form.set_all_readonly(False)
        button = None

        for param in self.params:
            # テキスト，数値など
            if 'value' in param:
                value = param.pop('value')
                if value is None:  continue
                ctrl = self.__find_ctrl(**param)
                if not ctrl is None:
                    ctrl.value = value

            # チェックボックス
            if 'check' in param:
                check = param.pop('check')
                if check is None:  continue
                ctrl = self.__find_ctrl(**param)
                if not ctrl is None:
                    ctrl.selected = check

            # ファイルアップロード
            if 'file_name' in param:
                file_name = param.pop('file_name')
                if file_name is None:  continue
                ctrl = self.__find_ctrl(**param)
                if not ctrl is None:
                    ctrl.file_name = file_name

        # Submit
        self.agent.submit()
        self.__update_params(self.agent.response().read().decode(self.encoding, 'ignore'))


    def __find_ctrl(self, **attr):
        #--------------------------------------------
        # Controlを取得
        # params:
        #   - attr -> HTML attr（※ classは，class_と指定）
        # return:
        #   - mechanize._form_controls.xxxxControl
        #--------------------------------------------
        attr = {list(attr.items())[0][0].replace('_', ''): list(attr.items())[0][1]}
        try:
            return self.agent.form.find_control(**attr)
        except:
            pass

        # 属性から検索
        for key, value in attr.items():
            for ctrl in self.agent.form.controls:
                if 'attrs' in vars(ctrl):
                    if key in ctrl.attrs:
                        if str(value) in str(ctrl.attrs[key]).split(' '):
                            return ctrl
                else:
                    try:
                        id = self.xpath('//*[@%s="%s"]' % (key, value)).attr('id')
                        return self.agent.form.find_control(id=id)
                    except:
                        continue
        return None


    def xpath(self, locator, single=False):
        #--------------------------------------------
        # XPathを指定しノードを抽出
        # params:
        #   - locator:str -> XPath
        # return:
        #   - pycrawl.carray
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
        # return:
        #   - pycrawl.carray
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
        # return:
        #   - 指定した属性の文字列
        #--------------------------------------------
        if name in self.doc.attrib:
            return self.doc.attrib[name]
        else:
            return ''


    def inner_text(self, shaping=True):
        #--------------------------------------------
        # タグ内の文字列を抽出
        # params:
        #   - shaping:bool -> 文字列を整形するか
        # return:
        #   - タグ内の文字列
        #--------------------------------------------
        if shaping:
            return self.__shaping_string(self.doc.text_content())
        else:
            return self.doc.text


    def outer_text(self):
        #--------------------------------------------
        # タグ外の文字列を抽出
        # return:
        #   - タグ外の文字列
        #--------------------------------------------
        return lxml.html.tostring(self.doc, encoding=self.encoding).decode(self.encoding, 'ignore')


    def __update_params(self, html):
        #--------------------------------------------
        # パラメータを更新
        # params:
        #   - html:str -> HTML
        #--------------------------------------------
        if self.agent._response is None:
            self.url = ''
        else:
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
        # return:
        #   - 整形後の文字列
        #--------------------------------------------
        # 余分な改行，空白を全て削除
        text = str(text)
        text = text.replace(' ', ' ')
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('\n \n', '\n').replace('\n ', '\n').replace('\r', '\n')
        text = re.sub(r'\n+', '\n', text)
        return text.replace('\t', '').strip()