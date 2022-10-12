from cnbc_scrape import cnbc_scrape

# query parameters
query_params=dict(
    QUERY='ekonomi',
    KANAL='',
    TIPE='',
    MIN_DATE='2022-03-01',
    MAX_DATE='2022-03-03'
)

# run the scrapping
cnbc_scrape(query_params=query_params, delay=1)