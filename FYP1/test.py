from bs4 import BeautifulSoup
import requests
import urllib


def post_html(url):
    headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
        'Cookie': '_ga=GA1.2.327590333.1528680236; _gat=1; _gid=GA1.2.2034975766.1529221699; templateColor=green; 85fda785538371be518fb5b360853ad6=dce67a7b0cd5c5b5423cf587b2f7aab6'
    }

    post_data = {
        'fabrik___filter[list_36_com_fabrik_36][value][0]': '2018'
    }

    try:
        url_data = requests.post(url, data=post_data, headers=headers).text
        url_data = url_data.decode('uft-8')

        return url_data
    except:
        print('Fail to access')


def delete_string(string):
    string = string.replace('\n', '').replace('\t', '')
    return string

def add_head(url):
    url_full = urllib.request.Request(url, headers={
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Cookie': '_ga=GA1.2.930520018.1528698641; 85fda785538371be518fb5b360853ad6=f8f4fbf49f6a3dda609aea710ad409d4; templateColor=green; _gid=GA1.2.1395804024.1529306884'
    })
    return url_full

def get_html(url):
    try:
        url_data = urllib.request.urlopen(add_head(url), timeout=50).read()
        url_data = url_data.decode('UTF-8')

        return url_data
    except:
        print('Open url fail')


def save_html(html_data, file_name):
    try:
        file_data = open(file_name + '.html', 'w')
        file_data.write(html_data)
        file_data.close()
        print("Save file successful")
    except:
        print("fail to save file")


if __name__ == '__main__':
    # html = open('Players matches.html', 'r')
    url = 'http://results.ittf.link/index.php?option=com_fabrik&view=list&listid=1&Itemid=111&&limit1=100'
    html = get_html(url)
    save_html(html, 'post')
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    table = soup.form.find('table', class_='table table-striped table-condensed table-hover')

    results = table.tbody.find_all('tr', class_='fabrik_row', recursive=False)

    #print(results)
    #next_link = table.tfoot.find('ul', class_='pagination-list').find('li', class_='pagination-next')
    #page = table.tfoot.find_all('span', class_='add-on')



    print(len(results))

    matchList = []

    for result in results:
        tournament_id = result.find('td', class_='fab_tournaments___tournament_id').get_text()
        year = result.find('td', class_='fab_tournaments___code').get_text()
        tournament_name = result.find('td', class_='fab_tournaments___tournament').get_text()
        tournament_type = result.find('td', class_='fab_tournaments___type').get_text()
        tournament_kind = result.find('td', class_='fab_tournaments___kind').get_text()
        tournament_organizer = result.find('td', class_='fab_tournaments___organizer').get_text()
        tournament_matches = result.find('td', class_='fab_tournaments___matches').get_text()
        tournament_from = result.find('td', class_='fab_tournaments___from').get_text()
        tournament_to = result.find('td', class_='fab_tournaments___to').get_text()

        Profile = [int(delete_string(tournament_id)), delete_string(year), delete_string(tournament_name),
                   delete_string(tournament_type), delete_string(tournament_kind),
                   delete_string(tournament_organizer), delete_string(tournament_matches),
                   delete_string(tournament_from), delete_string(tournament_to)]

        print(Profile)
        matchList.append(Profile)

    #print(next_link.a.get('href'))
    print(len(matchList))
    #print(page[1])

    #html.close()