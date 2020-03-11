from bs4 import BeautifulSoup
import requests


def run(cik_str, category_str, date_str=None):
    page = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type={cat}&dateb=&owner=exclude&count=100&output=atom".format(cat=category_str, cik=cik_str)
    resp = requests.get(page)                           # requests gets the response from the url ping as argument
    soup = BeautifulSoup(resp.text, 'html.parser')      # BeautifulSoup parses the html page of the body of the response
    for lk in soup.find_all('entry'):
        filing_url = getattr(lk, 'filing-href').text    # getattr().text is used to get the url for the attribute 'filing-href'; use getattr cos the attirbute cannot be accessed directly
        f_resp = requests.get(filing_url)
        filing_page_parser(f_resp.text)                 # call function to access independent text documents with the filing info


def filing_page_parser(html):
    soup_1 = BeautifulSoup(html, 'html.parser')
    tb = soup_1.find_all('table', attrs={"summary": "Document Format Files"})  # searching only for tables with the summary 'Document Format Files' to access the correct document
    tr = tb[0].find_all('tr')                                                  # searching for the tr bodies in table
    td = tr[-1].find_all('td')                                                 # searching for the last td body that contains the link to filing document
    sec_str = "sec.gov"                                                        # string to be appended to access link
    filing_doc = sec_str + td[-3].a['href']                                    # create string that contains url of filing document
    print(filing_doc)



run('0000320193','10-K')