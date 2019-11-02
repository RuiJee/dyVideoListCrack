# -*- coding: utf-8 -*-
import re
import signal

import requests
import json
import os
import uuid
import sys

from selenium.common.exceptions import TimeoutException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from settings import PRO_DIR, CHROME_DRIVER, PROXIES
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from settings import PRO_DIR

ua_gen = UserAgent(path=os.path.join(PRO_DIR, 'opt/fake_useragent_0.1.10.json'))

class Kol(object):
    proxy = Proxy(
        {
            'proxyType': ProxyType.MANUAL,
            'httpProxy': PROXIES
        }
    )
    ua = ua_gen.random


    def __init__(self):
        self.driver=None

    def set_up(self):
        option = webdriver.ChromeOptions()
        option.headless = True
        option.add_argument('disable-infobars')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')

        option.add_argument('--disable-gpu')
        option.add_argument('--user-agent={}'.format(self.ua))
        self.driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=option)
        # self.driver.get('https://www.baidu.com')
        js = "window.open('')"
        self.driver.execute_script(js)


    def get_sig_dytk(self, uid):
        #  获取到 tac 和 dytk
        p1 = r'<script>tac=\'(?P<tac>[\W\w]{150,300}?)\'</script>'
        pattern1 = re.compile(p1)

        p2 = r'dytk ?: ?\'(?P<dytk>[0-9a-z]*?)\''
        pattern2 = re.compile(p2)
        html = requests.get('https://www.douyin.com/share/user/{}/?share_type=link'.format(uid), headers={
            'user-agent': ua_gen.random}, proxies={
                                                                            'http': 'http://' + '118.190.122.25:10240',
                                                                            'https': 'http://' + '118.190.122.25:10240'
                                                                        }, timeout=3).text
        tac = pattern1.search(html).group('tac')
        dytk = pattern2.search(html).group('dytk')
        # print('22',tac,dytk)

        #  拼接html页面
        s_tac = "tac=\'{}\'".format(tac)
        print(s_tac)
        s1 = """
        <!DOCTYPE html>
        <html style="font-size: 50px;"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">  <title>抖音_signature破解</title>

        </head>
        <body></body>
        </html>
        <script type="text/javascript">
        """

        s2 = """
        !function(t) {
            if (t.__M = t.__M || {},
            !t.__M.require) {
                var e, n, r = document.getElementsByTagName("head")[0], i = {}, o = {}, a = {}, u = {}, c = {}, s = {}, l = function(t, n) {
                    if (!(t in u)) {
                        u[t] = !0;
                        var i = document.createElement("script");
                        if (n) {
                            var o = setTimeout(n, e.timeout);
                            i.onerror = function() {
                                clearTimeout(o),
                                n()
                            }
                            ;
                            var a = function() {
                                clearTimeout(o)
                            };
                            "onload"in i ? i.onload = a : i.onreadystatechange = function() {
                                ("loaded" === this.readyState || "complete" === this.readyState) && a()
                            }
                        }
                        return i.type = "text/javascript",
                        i.src = t,
                        r.appendChild(i),
                        i
                    }
                }, f = function(t, e, n) {
                    var r = i[t] || (i[t] = []);
                    r.push(e);
                    var o, a = c[t] || c[t + ".js"] || {}, u = a.pkg;
                    o = u ? s[u].url || s[u].uri : a.url || a.uri || t,
                    l(o, n && function() {
                        n(t)
                    }
                    )
                };
                n = function(t, e) {
                    "function" != typeof e && (e = arguments[2]),
                    t = t.replace(/\.js$/i, ""),
                    o[t] = e;
                    var n = i[t];
                    if (n) {
                        for (var r = 0, a = n.length; a > r; r++)
                            n[r]();
                        delete i[t]
                    }
                }
                ,
                e = function(t) {
                    if (t && t.splice)
                        return e.async.apply(this, arguments);
                    t = e.alias(t);
                    var n = a[t];
                    if (n)
                        return n.exports;
                    var r = o[t];
                    if (!r)
                        throw "[ModJS] Cannot find module `" + t + "`";
                    n = a[t] = {
                        exports: {}
                    };
                    var i = "function" == typeof r ? r.apply(n, [e, n.exports, n]) : r;
                    return i && (n.exports = i),
                    n.exports && !n.exports["default"] && Object.defineProperty && Object.isExtensible(n.exports) && Object.defineProperty(n.exports, "default", {
                        value: n.exports
                    }),
                    n.exports
                }
                ,
                e.async = function(n, r, i) {
                    function a(t) {
                        for (var n, r = 0, h = t.length; h > r; r++) {
                            var p = e.alias(t[r]);
                            p in o ? (n = c[p] || c[p + ".js"],
                            n && "deps"in n && a(n.deps)) : p in s || (s[p] = !0,
                            l++,
                            f(p, u, i),
                            n = c[p] || c[p + ".js"],
                            n && "deps"in n && a(n.deps))
                        }
                    }
                    function u() {
                        if (0 === l--) {
                            for (var i = [], o = 0, a = n.length; a > o; o++)
                                i[o] = e(n[o]);
                            r && r.apply(t, i)
                        }
                    }
                    "string" == typeof n && (n = [n]);
                    var s = {}
                      , l = 0;
                    a(n),
                    u()
                }
                ,
                e.resourceMap = function(t) {
                    var e, n;
                    n = t.res;
                    for (e in n)
                        n.hasOwnProperty(e) && (c[e] = n[e]);
                    n = t.pkg;
                    for (e in n)
                        n.hasOwnProperty(e) && (s[e] = n[e])
                }
                ,
                e.loadJs = function(t) {
                    l(t)
                }
                ,
                e.loadCss = function(t) {
                    if (t.content) {
                        var e = document.createElement("style");
                        e.type = "text/css",
                        e.styleSheet ? e.styleSheet.cssText = t.content : e.innerHTML = t.content,
                        r.appendChild(e)
                    } else if (t.url) {
                        var n = document.createElement("link");
                        n.href = t.url,
                        n.rel = "stylesheet",
                        n.type = "text/css",
                        r.appendChild(n)
                    }
                }
                ,
                e.alias = function(t) {
                    return t.replace(/\.js$/i, "")
                }
                ,
                e.timeout = 5e3,
                t.__M.define = n,
                t.__M.require = e
            }
        }(this)


        __M.define("douyin_falcon:node_modules/byted-acrawler/dist/runtime", function(l, e) {
            Function(function(l) {
                return 'e(e,a,r){(b[e]||(b[e]=t("x,y","x "+e+" y")(r,a)}a(e,a,r){(k[r]||(k[r]=t("x,y","new x[y]("+Array(r+1).join(",x[y]")(1)+")")(e,a)}r(e,a,r){n,t,s={},b=s.d=r?r.d+1:0;for(s["$"+b]=s,t=0;t<b;t)s[n="$"+t]=r[n];for(t=0,b=s=a;t<b;t)s[t]=a[t];c(e,0,s)}c(t,b,k){u(e){v[x]=e}f{g=,ting(bg)}l{try{y=c(t,b,k)}catch(e){h=e,y=l}}for(h,y,d,g,v=[],x=0;;)switch(g=){case 1:u(!)4:f5:u((e){a=0,r=e;{c=a<r;c&&u(e[a]),c}}(6:y=,u((y8:if(g=,lg,g=,y===c)b+=g;else if(y!==l)y9:c10:u(s(11:y=,u(+y)12:for(y=f,d=[],g=0;g<y;g)d[g]=y.charCodeAt(g)^g+y;u(String.fromCharCode.apply(null,d13:y=,h=delete [y]14:59:u((g=)?(y=x,v.slice(x-=g,y:[])61:u([])62:g=,k[0]=65599*k[0]+k[1].charCodeAt(g)>>>065:h=,y=,[y]=h66:u(e(t[b],,67:y=,d=,u((g=).x===c?r(g.y,y,k):g.apply(d,y68:u(e((g=t[b])<"<"?(b--,f):g+g,,70:u(!1)71:n72:+f73:u(parseInt(f,3675:if(){bcase 74:g=<<16>>16g76:u(k[])77:y=,u([y])78:g=,u(a(v,x-=g+1,g79:g=,u(k["$"+g])81:h=,[f]=h82:u([f])83:h=,k[]=h84:!085:void 086:u(v[x-1])88:h=,y=,h,y89:u({e{r(e.y,arguments,k)}e.y=f,e.x=c,e})90:null91:h93:h=0:;default:u((g<<16>>16)-16)}}n=this,t=n.Function,s=Object.keys||(e){a={},r=0;for(c in e)a[r]=c;a=r,a},b={},k={};r'.replace(/[-]/g, function(e) {
                    return l[15 & e.charCodeAt(0)]
                })
            }("v[x++]=v[--x]t.charCodeAt(b++)-32function return ))++.substrvar .length(),b+=;break;case ;break}".split("")))()('gr$Daten Иb/s!l y͒yĹg,(lfi~ah`{mv,-n|jqewVxp{rvmmx,&effkx[!cs"l".Pq%widthl"@q&heightl"vr*getContextx$"2d[!cs#l#,*;?|u.|uc{uq$fontl#vr(fillTextx$$龘ฑภ경2<[#c}l#2q*shadowBlurl#1q-shadowOffsetXl#$$limeq+shadowColorl#vr#arcx88802[%c}l#vr&strokex[ c}l"v,)}eOmyoZB]mx[ cs!0s$l$Pb<k7l l!r&lengthb%^l$1+s$jl  s#i$1ek1s$gr#tack4)zgr#tac$! +0o![#cj?o ]!l$b%s"o ]!l"l$b*b^0d#>>>s!0s%yA0s"l"l!r&lengthb<k+l"^l"1+s"jl  s&l&z0l!$ +["cs\\'(0l#i\\'1ps9wxb&s() &{s)/s(gr&Stringr,fromCharCodes)0s*yWl ._b&s o!])l l Jb<k$.aj;l .Tb<k$.gj/l .^b<k&i"-4j!+& s+yPo!]+s!l!l Hd>&l!l Bd>&+l!l <d>&+l!l 6d>&+l!l &+ s,y=o!o!]/q"13o!l q"10o!],l 2d>& s.{s-yMo!o!]0q"13o!]*Ld<l 4d#>>>b|s!o!l q"10o!],l!& s/yIo!o!].q"13o!],o!]*Jd<l 6d#>>>b|&o!]+l &+ s0l-l!&l-l!i\\'1z141z4b/@d<l"b|&+l-l(l!b^&+l-l&zl\\'g,)gk}ejo{cm,)|yn~Lij~em["cl$b%@d<l&zl\\'l $ +["cl$b%b|&+l-l%8d<@b|l!b^&+ q$sign ', [Object.defineProperty(e, "__esModule", {
                value: !0
            })])
        });

                dycs = __M.require("douyin_falcon:node_modules/byted-acrawler/dist/runtime")
                signc = dycs.sign(&&&)
                document.title=signc
                document.write("<p>"+signc+"</p>")

        </script>


        """
        s2 = s2.replace('&&&', uid)
        file = os.path.join(PRO_DIR, './htmls/', str(os.getpid()) + '.html')
        with open(file, 'w', encoding='utf-8') as fw:
            fw.write(s1 + s_tac + s2)
        print(len(self.driver.window_handles), self.driver.window_handles)
        # self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get('file://' + file)
        sig = WebDriverWait(self.driver, 2, 0.5).until(EC.presence_of_element_located((By.TAG_NAME, 'p')))
        sig = sig.text
        # try:
        #     print('==========',file)
        #     os.remove(file)
        # except IOError as e:
        #     print(e)
        return sig, dytk, self.ua

    def fetch_all_video(self, uid, page=1):
        sig, dytk, _ = self.get_sig_dytk(uid)

        max_cursor = 0
        headers = {
            'user-agent': self.ua
        }
        result = []
        while page > 0:
            r = requests.get(
                'https://www.douyin.com/aweme/v1/aweme/post/?user_id={}&count=21&max_cursor={}&aid=1128&_signature={}&dytk={}'.format(
                    uid, max_cursor, sig, dytk), timeout=3, headers=headers, proxies={
                    'http': 'http://' + '118.190.122.25:10240',
                    'https': 'http://' + '118.190.122.25:10240'
                }
            )
            if r.status_code == 200:
                data = json.loads(r.text)
                if data['status_code'] == 0:
                    if data['aweme_list']:
                        has_more = data['has_more']
                        max_cursor = data['max_cursor']
                        headers = r.request.headers
                        result.append(dict([('result_code', 1), ('aweme_list', data['aweme_list'])]))
                        if not has_more:
                            break
                    else:
                        result.append(dict([('result_code', 0), ('aweme_list', data['aweme_list'])]))
            page -= 1

        return result

    def checkout_user_agent(self):
        self.driver.quit()
        self.set_up()

        return self.ua


kol = Kol()
kol.set_up()
def quit(self, *arg, **kwargs):
    print('程序终止， 正在保存任务...')
    kol.driver.quit()
    os.popen("ps --ppid 1 | grep chrome | awk '{print $1}' | xargs kill")
    print('保存成功')

# signal.signal(signal.SIGINT, quit)
# signal.signal(signal.SIGTERM, quit)

if __name__ == '__main__':
    r = kol.fetch_all_video('89852104754')
    print(r)
