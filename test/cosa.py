import pandas as pd
from advertools import crawl



url = 'https://www.gogozo.gal'

#averiguo dominio


crawl(url, 'gogozo.jl', follow_links=False)
enczp = pd.read_json('gogozo.jl', lines=True)
print(enczp["resp_headers_link"])
