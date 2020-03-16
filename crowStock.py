import requests
from bs4 import BeautifulSoup
import traceback
import re


def getHTMLText(url, code='utf-8'):
    try:
        hd = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=hd, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""


def getStockList(lst, stockURL):
    html = getHTMLText(stockURL, 'GB2312')
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r'[s][hz]\d{6}', href)[0])
        except:
            continue


def getStockInfo(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        url = stockURL + stock
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')
            soup.prettify()

            stockName = soup.find('div', attrs={'class': 'stock-name'}).string
            stockValue = soup.find('div', attrs={'class': 'stock-current'}).string

            infoDict.update({stockName: stockValue})

            with open(fpath, 'a', encoding='utf-8') as f:
                f.write(str(infoDict) + '\n')
                count = count + 1
                print('\r当前速度:{:.2f}%'.format(count*100/len(lst)), end='')
        except:
            count = count + 1
            print('\r当前速度:{:.2f}%'.format(count * 100 / len(lst)), end='')
            traceback.print_exc()
            continue


def main():
    stock_list_url = 'http://quote.eastmoney.com/stock_list.html'
    stock_info_url = 'https://xueqiu.com/S/'
    output_file = '/users/lyle/Desktop/XueQiuStockInfo.txt'
    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)


if __name__ == '__main__':
    main()
