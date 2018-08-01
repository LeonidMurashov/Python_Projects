from html.parser import HTMLParser
import urllib.request

tr_was = False
td_num = 0
got_score = 0
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global tr_was, td_num, got_score
        if tag == 'tr':
            tr_was = True
            print()
            print()
        if tr_was:
            if tag == 'td':
                td_num += 1
                got_score = 0
            #print("Encountered a start tag:", tag,attrs)

    def handle_endtag(self, tag):
        global tr_was, td_num, got_score
        if tag == 'tr':
            tr_was = False
            td_num = 0
        if tr_was:
            pass##print("Encountered an end tag :", tag)

    def handle_data(self, data):
        global tr_was, td_num, got_score
        if tr_was:
            if got_score < 1 and (td_num == 2 or td_num == 9):
                print(["Name:", "Score:"][got_score], data)
                got_score += 1

parser = MyHTMLParser()
f = urllib.request.urlopen("https://tanks.geekclass.ru/stats")
parser.feed(str(f.read()))