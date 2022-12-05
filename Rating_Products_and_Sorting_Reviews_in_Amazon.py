# Rating Product&Sorting Reviews in Amazon
import pandas as pd
import math
import scipy.stats as st
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv("csv/amazon_review.csv")
df.head()

##################################################################################################################
# Görev 1
# Paylaşılan veri setinde kullanıcılar bir ürüne puanlar vermiş ve yorumlar yapmıştır. Bu görevde amacımız verilen
# puanları tarihe göre ağırlıklandırarak değerlendirmek.İlk ortalama puan ile elde edilecek tarihe göre ağırlıklı puanın
# karşılaştırılması gerekmektedir.

# Adım 1:   Ürünün ortalama puanını hesaplayınız.



df["overall"].mean()

# Adım 2 Tarihe göre ağırlıklı puan ortalamasını hesaplayınız
# •reviewTime değişkenini tarih değişkeni olarak tanıtmanız
# •reviewTime'ın max değerini current_date olarak kabul etmeniz
# •her bir puan-yorum tarihi ile current_date'in farkını gün cinsinden ifade ederek yeni değişken oluşturmanız ve gün cinsinden ifade edilen
# değişkeni quantile fonksiyonu ile 4'e bölüp (3 çeyrek verilirse 4 parça çıkar)çeyrekliklerden gelen değerlere göre ağırlıklandırmayapmanız gerekir.
# Örneğin q1 = 12 ise ağırlıklandırırken 12 günden az süre önce yapılan yorumların ortalamasını alıp bunlara yüksek ağırlık vermek gibi.

df["reviewTime"] = pd.to_datetime(df["reviewTime"])

current_date = df["reviewTime"].max()

df["recency_rating_review"] = (current_date - df["reviewTime"]).dt.days
df["recency_rating_review"].describe().T

df["recency_cut"]= pd.qcut(df["recency_rating_review"], 4, labels= ["q1", "q2", "q3", "q4" ])



# 0-280-430-600-1063

df.loc[df["recency_cut"] == "q1", "overall"].mean()*30/100 + \
    df.loc[df["recency_cut"] == "q2", "overall"].mean() * 28/100 + \
    df.loc[df["recency_cut"] == "q3", "overall"].mean() * 26/100 + \
    df.loc[df["recency_cut"] == "q4", "overall"].mean() * 16/100



# Alternatif

def time_based_weighted_average(dataframe, w1=30, w2=28, w3=26, w4=16):
    return dataframe.loc[df["recency_cut"] == "q1", "overall"].mean() * w1 / 100 + \
           dataframe.loc[df["recency_cut"] == "q2", "overall"].mean() * w2 / 100 + \
           dataframe.loc[df["recency_cut"] == "q3", "overall"].mean() * w3 / 100 + \
           dataframe.loc[df["recency_cut"] == "q4", "overall"].mean() * w4 / 100

time_based_weighted_average(df)


########################################################################################################################
#Alternatif
# zaman bazlı ortalama ağırlıkların belirlenmesi
def time_based_weighted_average(dataframe, w1=50, w2=25, w3=15, w4=10):
    return dataframe.loc[dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.25), "overall"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > dataframe["day_diff"].quantile(0.25)) & (dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.50)), "overall"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > dataframe["day_diff"].quantile(0.50)) & (dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.75)), "overall"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > dataframe["day_diff"].quantile(0.75)), "overall"].mean() * w4 / 100


########################################################################################################################
# Alternatif

df["days"]=(current_date-df["reviewTime"]).dt.days
df["days"].describe().T

df.loc[df["days"] <= 30, "overall"].mean()

df.loc[(df["days"] > 30) & (df["days"] <= 90), "overall"].mean()

df.loc[(df["days"] > 90) & (df["days"] <= 180), "overall"].mean()

df.loc[df["days"] > 180, "overall"].mean()

def time_based_weighted_averege(dataframe,w1=30, w2=28, w3=22, w4=20):
    return df.loc[df["days"] <= 30, "overall"].mean()*w1/100\
           +df.loc[(df["days"] > 30) & (df["days"] <= 90), "overall"].mean()*w2/100\
           +df.loc[(df["days"] > 90) & (df["days"] <= 180), "overall"].mean()*w3/100\
           +df.loc[df["days"] > 180, "overall"].mean()*w4/100

######################################################################################################################

# Adım 3 Ağırlıklandırılmış puanlamada her bir zaman diliminin ortalamasını karşılaştırıp yorumlayınız


# q1 (0, 280]
df.loc[df["recency_cut"] == "q1", "overall"].mean()

# q2 (280, 430]
df.loc[df["recency_cut"] == "q2", "overall"].mean()

# q3 (430, 600]
df.loc[df["recency_cut"] == "q3", "overall"].mean()

# (600, 1063]
df.loc[df["recency_cut"] == "q4", "overall"].mean()

# Analiz gününe en yakın yapılan puanlamanın en yüksek olduğunu görüyoruz. Eski puanlamalara doğru gittikçe verilen puan
# ortalamaları düşmüştür. Bunun sebebi son dönemlerde üründe yapılan iyileştirmeler olabilir. Belki üründe verilen geri
# dönüşlere göre iyileştirmeler yapılmıştır ve bu sebeple son dönemde müşteri memnuniyeti artmıştır.

########################################################################################################################

# Görev 2 Ürün için ürün detay sayfasında görüntülenecek 20 review’i belirleyiniz
# Adım 1  helpful_no değişkenini üretiniz.
# total_vote bir yoruma verilen toplam up-down sayısıdır.
# •up, helpful demektir.
# •Veri setinde helpful_no değişkeni yoktur, var olan değişkenler üzerinden üretilmesi gerekmektedir.
# •Toplam oy sayısından (total_vote) yararlı oy sayısı (helpful_yes) çıkarılarak yararlı bulunmayan oy sayılarını (helpful_no) bulunuz.

df.head()
df["helpful_no"] = df["total_vote"] - df["helpful_yes"]

# Adım 2 score_pos_neg_diff, score_average_rating ve wilson_lower_bound skorlarını hesaplayıp veriye ekleyiniz
# score_pos_neg_diff, score_average_rating ve wilson_lower_boundskorlarını hesaplayabilmek için score_pos_neg_diff,
# score_average_ratingve wilson_lower_boundfonksiyonlarını tanımlayınız.
# •score_pos_neg_diff'a göre skorlar oluşturunuz. Ardından; df içerisindescore_pos_neg_diff ismiyle kaydediniz.
# •score_average_rating'agöre skorlar oluşturunuz. Ardından; df içerisinde score_average_rating ismiyle kaydediniz.
# •wilson_lower_bound'agöre skorlar oluşturunuz. Ardından; df içerisinde wilson_lower_boundismiyle kaydediniz

def score_pos_neg_diff(pos, neg):
    return pos - neg

df["score_pos_neg_diff"] = score_pos_neg_diff(df["helpful_yes"], df["helpful_no"])
df.head(20)
df.tail()


def score_average_rating(pos, neg):
    if pos + neg == 0:
        return 0
    return pos / (pos + neg)

df["score_average_rating"] = df.apply(lambda x: score_average_rating(x["helpful_yes"], x["helpful_no"]), axis=1)



def wilson_lower_bound(pos, neg, confidence=0.95):
    n = pos + neg
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * pos / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)



df["wilson_lower_bound"] = df.apply(lambda x: wilson_lower_bound(x["helpful_yes"], x["helpful_no"]), axis=1)

# Adım 3
df.sort_values("wilson_lower_bound", ascending=False).head(20)

# WLB ile yapılan sıralamada ilk dörtte en çok oy alan yorumlar yer alıyor bu da bize WLB'un social proofu dikkate
# aldığını gösterir. Aynı zamanda faydalı bulunma oranı da dikkate alınmıştır. Aynı zamanda score_average_ratinge göre
# sıralama yapsaydık gözlem 5 gözlem 4 ün önüne geçecekti fakat burda 4. gözlemde daha çok oylama yapıldığı için WBL hesabında 5'in önüne geçmiştir.

df.sort_values("total_vote", ascending=False).head()