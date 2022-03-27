from bs4 import BeautifulSoup
import time
import requests
import json
import re




# Could automate this process... is there an API to find out what archives exist within web.archive.org?
draft_year_links = {
    # 2024: [
    #         'https://web.archive.org/web/20210304181637/https://walterfootball.com/draft2024.php',
    #         'https://web.archive.org/web/20210329202451/https://walterfootball.com/draft2024.php',
    #         'https://web.archive.org/web/20210417210521/https://walterfootball.com/draft2024.php',
    #         'https://web.archive.org/web/20210927144324/https://walterfootball.com/draft2024.php',
    #         'https://web.archive.org/web/20211009215604/https://walterfootball.com/draft2024.php',
    #         'https://web.archive.org/web/20211117192736/https://walterfootball.com/draft2024.php',
    # ],
    # 2023: [ 'https://web.archive.org/web/20200526003534/https://walterfootball.com/draft2023.php',
    #         'https://web.archive.org/web/20200901030043/https://walterfootball.com/draft2023.php',
    #         'https://web.archive.org/web/20201101022828/https://walterfootball.com/draft2023.php',
    #         'https://web.archive.org/web/20210120162358/https://walterfootball.com/draft2023.php',
    #         'https://web.archive.org/web/20210421171304/https://walterfootball.com/draft2023.php',
    #         'https://web.archive.org/web/20210927144515/https://walterfootball.com/draft2023.php',
    #         'https://web.archive.org/web/20211021195017/https://walterfootball.com/draft2023.php',
    #         'https://web.archive.org/web/20220105111149/https://walterfootball.com/draft2023.php'
    # ],
    # 2022: [
    #         'https://web.archive.org/web/20200117021430/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20200218204510/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20200425225253/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20200603054005/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20200810161900/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20200926022459/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20201028031344/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20201115011513/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20210430221801/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20210507215850/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20210609042804/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20210715204009/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20210908140814/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20211006175722/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20211103162254/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20211202134152/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20220106045915/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20220203192840/https://walterfootball.com/draft2022.php',
    #         'https://web.archive.org/web/20220309082546/https://walterfootball.com/draft2022.php'
    # ],
    2012: [
            'https://web.archive.org/web/20100723172127/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20101130023450/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20101223175253/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20110521041158/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20110606051413/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20110710170223/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20110802055237/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20110902012045/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20111005164859/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20111117055005/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20111213143042/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20120112051941/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20120215161409/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20120301112751/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20120318081125/https://walterfootball.com/draft2012.php',
            'https://web.archive.org/web/20120404200232/https://walterfootball.com/draft2012.php'
    ]
}


mock_url_template = 'https://web.archive.org/web/{mock_yyyy_mm_dd}/http://www.walterfootball.com/draft{year}{round_modifier}.php'


def parse_dt_from_url(url):

    modified_url = url
    modified_url = modified_url.replace('https://web.archive.org/web/', '')
    modified_url_split = modified_url.split('/')

    url_dt = modified_url_split[0]
    return url_dt


def scrape_wayback(wayback_url, last_url):


    source = requests.get(wayback_url)
    print(source)
    print(source.url)
    if last_url == source.url:
        print('SKIPPING')
        return {'last_url': last_url, 'action': 'skip'}

    last_url = source.url
    print(parse_dt_from_url(source.url))
    
    soup = BeautifulSoup(source.content,'html.parser')
    #print(soup)

    loop_count = 1
    for elem in soup.select('.article li b'):
        #data = {'from_json': False, 'wayback_url': wayback_url, 'b': elem}
        #player_list.append(Player(data))
        elem_text = str(elem)
        elem_text = elem_text.replace('<b>', '')
        elem_text = elem_text.replace('</b>', '')
        elem_text = elem_text.replace(':', ',')
        elem_text = elem_text.strip()

        elem_split = elem_text.split(',')
        elem_split = [i.strip() for i in elem_split]

        if '<a href="draft' in elem_text:
            continue

        mocked_team = elem_split[0]
        player_name = elem_split[1]
        player_position = elem_split[2]
        player_college = elem_split[3]

        print(elem, elem_split)


        loop_count +=1



    time.sleep(1)

    return {'last_url': last_url}

    #return player_list


def scrape_stuff():
    last_url = ''
    counter = 1
    for mock_year in range(2011, 2012):
        print('mock_year', mock_year)


        for mock_web_year in range(mock_year - 3, mock_year + 1):
            print('mock_web_year', mock_web_year)
            for mock_web_month in range(1, 12 + 1):
                mock_url = mock_url_template
                mock_url = mock_url.replace('{mock_yyyy_mm_dd}', f'{mock_web_year}{mock_web_month}01')
                mock_url = mock_url.replace('{year}', f'{mock_year}')
                mock_url = mock_url.replace('{round_modifier}', '_1')

                results = scrape_wayback(mock_url, last_url)
                last_url = results['last_url']

                counter +=1

                if counter > 5:
                    return 0
                

scrape_stuff()



#scrape_wayback('https://web.archive.org/web/20090101/http://www.walterfootball.com/draft2012_1.php')

# for mock_draft_year, mock_links in draft_year_links.items():
#     print(mock_draft_year, mock_links)

#     for mock_link in mock_links:
#         scrape_wayback(mock_link)