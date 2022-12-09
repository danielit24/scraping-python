import snscrape.modules.twitter as sntwitter
import pandas as pd
import re, string, argparse
from textblob import TextBlob


pd.options.display.max_colwidth = 1000

lang = " lang:en"
query = "Jakarta" + lang

print("kalimat yang dicari : "+ query)
hasilAnalisa = []
limit = 100

try:
    print("start crawling")
    for tweet in sntwitter.TwitterSearchScraper(query=query).get_items():
        hasilSearch = {}
        if len(hasilAnalisa) == limit:
            break
        else:
            tweet_bersih = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweet.content).split())
            hasilSearch["tanggal"] = tweet.date 
            hasilSearch["username"] = tweet.user.username
            hasilSearch["isi_tweet"] = tweet_bersih
            analisis = TextBlob(tweet_bersih)

            if analisis.sentiment.polarity > 0.0:
                hasilSearch["sentimen"] = "positif"
            elif analisis.sentiment.polarity == 0.0:
                hasilSearch["sentimen"] = "netral"
            else:
                hasilSearch["sentimen"] = "negatif"
            hasilAnalisa.append(hasilSearch)
    
    tweet_positif = [t for t in hasilAnalisa if t["sentimen"]=="positif"]
    tweet_netral = [t for t in hasilAnalisa if t["sentimen"]=="netral"]
    tweet_negatif = [t for t in hasilAnalisa if t["sentimen"]=="negatif"]

    print("hasil sentimen : \n")
    print("positif : ", len(tweet_positif), "({} %)".format(100*len(tweet_positif)/len(hasilAnalisa)))
    print("netral : ", len(tweet_netral), "({} %)".format(100*len(tweet_netral)/len(hasilAnalisa)))
    print("negatif : ", len(tweet_negatif), "({} %)".format(100*len(tweet_negatif)/len(hasilAnalisa)))

    # print(tweet_negatif)
    df = pd.DataFrame(hasilAnalisa, columns=['isi_tweet', 'sentimen'])

except Exception as e:
    print(e)
print("Finished")
print("------ \n")
print(df.head())