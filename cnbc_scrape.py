import time
import datetime
import pandas as pd
import requests as rs
from bs4 import BeautifulSoup
from tqdm import tqdm, trange


def _time_parse(days="all", custom_range=False):
    if custom_range:
        min_date=custom_range[0]
        max_date=custom_range[1]
    else:
        min_date=min_date
        max_date=max_date         
    min_date_l = [int(d) for d in min_date.split("-")]
    max_date_l = [int(d) for d in max_date.split("-")]
    min_date_dt = datetime.date(min_date_l[0], min_date_l[1], min_date_l[2])
    max_date_dt = datetime.date(max_date_l[0], max_date_l[1], max_date_l[2])
    time_dif = max_date_dt-min_date_dt
    num_days = time_dif.days
    if days=="all":
        time_list=[(min_date_dt+datetime.timedelta(i)).strftime("%Y/%m/%d")\
                for i in range(num_days+1)]
    else:
        time_list=[]
        for i in range(num_days+1):
            date=min_date_dt+datetime.timedelta(i)
            if date.strftime("%A") in days:
                time_list.append(date.strftime("%Y/%m/%d"))
    return time_list


def cnbc_scrape(query_params={}, date_list=None, use_range=False, delay=1):

    QUERY = query_params['QUERY']
    KANAL = query_params['KANAL']
    TIPE = query_params['TIPE']
    MIN_DATE = query_params['MIN_DATE']
    MAX_DATE = query_params['MAX_DATE']
    
    print("-"*50)
    print("Scraping news from CNBC Indonesia")
    print("-"*50)
    print("Query parameters:\n", query_params)
    print("-"*50)
    print("Progress:")

    if date_list == None:
        date_list=_time_parse(days="all",custom_range=[MIN_DATE,MAX_DATE])
    for date in tqdm(date_list, desc='Total'):
        r_f=rs.get(f'https://www.cnbcindonesia.com/search?query={QUERY}&p=1&kanal={KANAL}\
                     &tipe={TIPE}&date={date}')
        soup_f = BeautifulSoup(r_f.text, "html.parser")
        total_pages_el = soup_f.select('.gtm_paging')
        if len(total_pages_el) == 0:
            continue
        total_pages=int(total_pages_el[0].select('a')[-2].text)
        page_iterator=trange(total_pages, desc=date)
        for page in page_iterator:
            data_dict=dict(dates=[], titles=[], labels=[], links=[], details_text=[],authors=[])
            df=pd.DataFrame(data_dict)
            r=rs.get(f'https://www.cnbcindonesia.com/search?query={QUERY}&p={page+1}&kanal={KANAL}\
                     &tipe={TIPE}&date={date}')
            soup=BeautifulSoup(r.text, "html.parser")
            gtm_articles=soup.select('.gtm_indeks_feed')
            articles=gtm_articles[0].select('article')
            titles=[articles[i].select('h2')[0].text for i in range(len(articles))]
            labels=[articles[i].select('.label')[0].text for i in range(len(articles))]
            links=[articles[i].a['href'] for i in range(len(articles))]

            details_text=[]
            authors=[]
            for url in tqdm(links, desc=f"Page {page+1}"):
                rd=rs.get(url)
                soupd=BeautifulSoup(rd.text, "html.parser")
                detail_text=soupd.select('.detail_text')

                detail_text_parsed=''
                paragraphs=detail_text[0].select('p')
                for p in paragraphs:
                    detail_text_parsed+=p.text

                details_text.append(detail_text_parsed)
                authors.append(soupd.select('.author')[0].text)
                time.sleep(delay)
                
            dates=[date for i in range(len(titles))]
            df_temp=pd.DataFrame(dict(dates=dates, titles=titles, labels=labels, links=links, details_text=details_text,authors=authors))
            df=df.append(df_temp)
            if page < 10:
                page_indicator = "0"+str(page+1)
            else:
                page_indicator  = str(page+1)
            df.to_csv(f"{QUERY}_{date.replace('/','')}_{page_indicator}_cnbc.csv",index=False)