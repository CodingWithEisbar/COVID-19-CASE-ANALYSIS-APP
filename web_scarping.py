from bs4 import BeautifulSoup
import requests

def parse(d): #read indivitual dictionary
    dictionary = dict()
    # Removes curly braces and splits the pairs into a list
    pairs = d.strip('{}').split(', ')
    for i in pairs:
        pair = i.split(': ')
        # Other symbols from the key-value pair should be stripped.
        dictionary[pair[0].strip('\'\'\"\"')] = pair[1].strip('\'\'\"\"')
    return dictionary


def update_Data1(save_file): 
    #https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19/S%E1%BB%91_ca_nhi%E1%BB%85m_theo_t%E1%BB%89nh_th%C3%A0nh_t%E1%BA%A1i_Vi%E1%BB%87t_Nam#cite_note-1
    html = requests.get("https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19/S%E1%BB%91_ca_nhi%E1%BB%85m_theo_t%E1%BB%89nh_th%C3%A0nh_t%E1%BA%A1i_Vi%E1%BB%87t_Nam#cite_note-1").text
    soup = BeautifulSoup(html, "html5lib")

    table_tag = soup.find('table')
    #print(table_tag.prettify())

    #get table content
    td_tag = table_tag.findAll('td')
    #get table lable
    th_tag = table_tag.findAll('th')

    table_header = []

    for th in th_tag:
        table_header.append(th.text.strip())

    table =[]

    for td in td_tag:
        if td.find('a', title=True): 
            table.append(td.find('a').text)
        else:
            table.append(td.text.strip())

    table_full = []
    i = 0
    holder = {}
    target = open(save_file, "w", encoding="utf8")

    for unit in table:
        holder[table_header[i]] = unit
        i+=1
        if i == 6:
            i = 0;
            target.write(str(holder) + "\n")
            table_full.append(holder)
            del holder; holder = {}

    target.close()
    
    return table_full


def update_Data2(save_file):
    LIST = []
    
    f = requests.get("https://coronavirus-19-api.herokuapp.com/countries").text
        
    rawData = f.strip("[]").replace("},{", "}\n{").replace(",", ", ").replace(":", ": ")
    lines = rawData.split("\n")
        
    target = open(save_file, "w", encoding="utf8")

    for i in lines:
        diction = parse(i)
        target.write(str(diction) + "\n")
        LIST.append(diction)

    target.close()

    return lines    


def getDictionatyData(file_name):
    LIST = []
    try:
        f = open(file_name, "r", encoding="utf8")
        lines = f.read().split("\n")
        for l in lines:
            diction = parse(l)
            LIST.append(diction)
        f.close()
    except f.errors:
            print("error")
    finally:
        return LIST


def getListData(file_name):
    LIST=[]
    try:
        f = open(file_name, "r", encoding="utf8")
        lines = f.read().split("\n")
        for l in lines:
            LIST.append(l)
        f.close()
    except f.errors:
        print("error")
    finally:
        return LIST




