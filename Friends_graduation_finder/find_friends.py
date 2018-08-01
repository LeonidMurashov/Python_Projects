friends = ['Куманяев Сергей','Коваленко Иван','Абрамов Владислав']
output = 'pupils2.html'

code = '<HTML><style> \n\
* { font-family:font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;\n\
}\n\
table {\n\
border-collapse: collapse;\n\
border: 25px solid grey;\n\
width: 100%;\n\
border-collapse: collapse;\n\
}\n\
th , td {\n\
border: 1px solid grey;\n\
}\n\
tr:hover td {background: #A4C3E5;}\n\
tr:nth-child(2n) {background: #B8E5A4;}\n\
</style>'

import urllib.request
from bs4 import BeautifulSoup

admlist_adress ='http://admlist.ru'
with urllib.request.urlopen(admlist_adress + '/index.html') as file:
    text = file.read().decode('utf-8')

soup = BeautifulSoup(text, 'lxml')
VUZ_list = soup.findAll('tr')
link = None
for vuz in VUZ_list:
    td_vuz = vuz.find('td')
    if td_vuz is None:
        continue
    
    a = td_vuz.find('a')
    if a is not None:
        link = a.get('href').split('/')[0]
        
        # Opening faculties page
        vuz_name = a.text
        print('Searching', vuz_name)
        code += '<h1>' + vuz_name + '</h1>'
        with urllib.request.urlopen(admlist_adress + '/' + link + '/index.html') as file:
            text = file.read().decode('utf-8')

        soup = BeautifulSoup(text, 'lxml')        
        
        fac_list = soup.findAll('tr')
        for fac in fac_list:
            td_fac = fac.find('td')
            if td_fac is None:
                continue

            a = td_fac.find('a')
            if a is not None:
                link_to_list = admlist_adress + '/' + link + '/'+ a.get('href')

                # Opening page with list
                with urllib.request.urlopen(link_to_list) as file:
                    text = file.read().decode('utf-8')

                soup = BeautifulSoup(text, 'lxml')             
                
                if link in ['msu', 'mai']:
                    if len(soup.findAll('table')) < 3:
                        continue
                    pupils_list = soup.findAll('table')[2].findAll('tr')
                else:
                    pupils_list = soup.findAll('tr')                
                
                if len(pupils_list) <= 3:
                    continue
                title = pupils_list[2]
                pupils_list = pupils_list[3:]

                fac_table_refrashed = False
                for pupil in pupils_list:
                    splits = pupil.findAll('td')[3].text.split()
                    if len(splits) < 2:
                        continue
                    surname, name, *_ = splits
                    name = surname + ' ' + name
                    if name in friends:
                        print('Found',name, 'on', soup.find('h2').text)
                        if not fac_table_refrashed:                               
                            code += '<h2>' + soup.find('h2').text + '</h2>'
                            code += '<table><thead>'+ title.prettify() +'</thead><tbody>'
                            fac_table_refrashed = True
                        code += pupil.prettify()

                if fac_table_refrashed:
                    code += '</tbody></table><br><br>'
    if link == 'mai':
        break
                    
code += '</html>'

code = code.replace('..', 'http://admlist.ru')
with open(output,'w') as file:
    file.write(code)