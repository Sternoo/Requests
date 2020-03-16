#crowTaobaoPrice.py
import requests
import re


def getHTMLText(url):
    try:
        # 淘宝加了登录验证
        headers = {
            'authority': 's.taobao.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'referer': 'https://s.taobao.com/search?q=%E4%B9%A6%E5%8C%85&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200306&ie=utf8',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie': 't=fa307f9bc33d5671716bec119fcba3bb; cna=GJl0Fo4LEnMCAXPvR7ztZG5Y; thw=cn; v=0; cookie2=17dbbfb5a53a3a3ac0eefc77ad26f354; _tb_token_=e6e3e07ea8d37; _samesite_flag_=true; unb=1080963353; uc3=id2=UoH38yRO0wY5yQ%3D%3D&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dBxd7H7wbfHM1bW2g%3D&nk2=0%2BIyDIonA9w%3D; csg=8b7e3e5b; lgc=%5Cu963F%5Cu6728%5Cu6728gk; cookie17=UoH38yRO0wY5yQ%3D%3D; dnk=%5Cu963F%5Cu6728%5Cu6728gk; skt=71a1168763420fe1; existShop=MTU4MzQ4MDY4Ng%3D%3D; uc4=nk4=0%400VmGy6%2BBsGVejgftxyJjvpYWuw%3D%3D&id4=0%40UOnojEE9HFlA%2F2CzA6LKJlARPaZu; tracknick=%5Cu963F%5Cu6728%5Cu6728gk; _cc_=UtASsssmfA%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=k36; _nk_=%5Cu963F%5Cu6728%5Cu6728gk; cookie1=Bvdzz%2BEK2UYziNjTRioNIEwBOdz5b1oJ7lJtEXiK2VI%3D; enc=HnvUMLhwlrSWyRb49u1kyhHA2karqbyDPU%2BffQL0ZftWizAtgR%2FbVke%2FDPkAGgBtKMPOokHihT5CsjY5iPPnxQ%3D%3D; tfstk=ceEcBDXRBbOC96LwREibC_37H-AGaIpqTlza4oXBiVcZrUEr3s0yze7H9TDLilL1.; mt=ci=5_1; hng=CN%7Czh-CN%7CCNY%7C156; JSESSIONID=280E9FBC7CDE337027417CDC26772CAE; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=VFC%2FuZ9ainBZ&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=false&pas=0&cookie14=UoTUOaqPGH2VkA%3D%3D&tag=8&lng=zh_CN; isg=BMbGoDTI5LME9LA3XrQaCwbLF7pIJwrhAt7YCbDr_OnDs2HNHbbh8eqBi-9_GwL5; l=dBx5EyURQOoKbR2BBOfgS72LX07OZCAffsPrq_Kn-ICP9F1vopzlWZq4bi8JCnGVHs3yW3SmUfZ3B7LFDPl-Jxpsw3k_J_DmndC..',
        }
        r = requests.get(url, timeout=30, headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parsePage(ilt, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price, title])
    except:
        print("")


def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))


def main():
    goods = '书包'
    depth = 3
    start_url = 'https://s.taobao.com/search?q=' + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    printGoodsList(infoList)


main()