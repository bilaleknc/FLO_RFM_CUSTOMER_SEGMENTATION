##############################################################################################################################
#                                 RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
##############################################################################################################################





########################################
###### İş Problemi (Business Problem)
########################################

""" FLO satış ve pazarlama faaliyetleri için roadmap belirlemek istemektedir. Şirketin orta uzun vadeli plan yapabilmesi için var olan 
müşterilerin gelecekte şirkete sağlayacakları potansiyel değerin tahmin edilmesi gerekmektedir.
"""

########################################
# Veri Seti Hikayesi
########################################

"""
Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş 
davranışlarından elde edilen bilgilerden oluşmaktadır
"""

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi



########################################
# GÖREVLER
########################################

# GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.
           # 2. Veri setinde
                     # a. İlk 10 gözlem,
                     # b. Değişken isimleri,
                     # c. Betimsel istatistik,
                     # d. Boş değer,
                     # e. Değişken tipleri, incelemesi yapınız.
           # 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
           # 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
           # 5. Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.
           # 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
           # 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
           # 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.

# GÖREV 2: RFM Metriklerinin Hesaplanması

# GÖREV 3: RF ve RFM Skorlarının Hesaplanması

# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması

# GÖREV 5: Aksiyon zamanı!
           # 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
           # 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye kaydediniz.
                   # a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
                   # tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Sadık müşterilerinden(champions,loyal_customers),
                   # ortalama 250 TL üzeri ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kuralacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına
                   # yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.
                   # b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir
                   # alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
                   # olarak kaydediniz.


# GÖREV 6: Tüm süreci fonksiyonlaştırınız.

###############################################################
# GÖREV 1: Veriyi  Hazırlama ve Anlama (Data Understanding)
###############################################################

import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 1000)


# 1. flo_data_20K.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz.
df_ = pd.read_csv("WEEK_3/FLO_RFM_Analizi/FLO_RFM_Analizi/flo_data_20k.csv")
df = df_.copy()
df.head()


# 2. Veri setinde
        # a. İlk 10 gözlem,
        # b. Değişken isimleri,
        # c. Boyut,
        # d. Betimsel istatistik,
        # e. Boş değer,
        # f. Değişken tipleri, incelemesi yapınız.

df.head(10)
df.columns
df.shape
df.describe().T
df.isnull().sum()
df.info()


# 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir.
# Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.
df.head()

df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

# 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz

# 1.Yöntem:
df.dtypes
for col in df.columns:
  if "date" in col:
    df[date_cols] = df[date_cols].apply(pd.to_datetime)
    #df[date_cols] = df[date_cols].astype('datetime64[ns]')


# 5. Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısı ve toplam harcamaların dağılımına bakınız.
df.head()
df.groupby("order_channel").agg({"master_id": "count",
                                 "order_num_total": "sum",
                                 "customer_value_total": "sum"})

# Görselleştirme:
# sns.catplot(x="order_channel", y="order_num_total", data=df)
# plt.show()

# 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.

df.sort_values("customer_value_total", ascending=False)[["master_id","customer_value_total"]][:10]

# 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
df.sort_values("order_num_total", ascending=False)[["master_id","order_num_total"]][:10]


# 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.
def data_prep(dataframe):
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    for col in df.columns:
        if "date" in col:
            df[date_cols] = df[date_cols].apply(pd.to_datetime)
            #df[date_cols] = df[date_cols].astype('datetime64[ns]')
    return dataframe

df = df_.copy()
# df.columns
# df.dtypes
df = data_prep(df)
df.head(2)

###############################################################
# GÖREV 2: RFM Metriklerinin Hesaplanması
###############################################################


# Adım 1: Recency, Frequency ve Monetary tanımlarını yapınız.
# Adım 2: Müşteri özelinde Recency, Frequency ve Monetary metriklerini hesaplayınız
# Adım 3: Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.
# Adım 4: Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.

# Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi olarak belirleyelim:
max(df["last_order_date"])

today_date = dt.datetime(2021,6, 2)
type(today_date)

# customer_id, recency, frequnecy ve monetary değerlerinin yer aldığı yeni bir rfm dataframe
rfm=pd.DataFrame({"CustomerId": df["master_id"],
                   "Recency": (today_date - df["last_order_date"]).dt.days,
                   "Frequency": df["order_num_total"],
                   "Monetary": df["customer_value_total"]})


# rfm[rfm["CustomerId"]=="f431bd5a-ab7b-11e9-a2fc-000d3a38a36f"]
rfm.head()

###############################################################
# GÖREV 3: RF ve RFM Skorlarının Hesaplanması (Calculating RF and RFM Scores)
###############################################################
# Adım 1: Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.
# Adım 2: Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.

# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydedilmesi
rfm["recency_score"] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['Frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm.head()

# Adım 3: recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RF_SCORE olarak kaydediniz.
rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))

rfm.head()

###############################################################
# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması
###############################################################
# Adım 1: Oluşturulan RF skorları için segment tanımlamaları yapınız.
# Adım 2: Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz.

# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlama ve  tanımlanan seg_map yardımı ile RF_SCORE'u segmentlere çevirme
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

rfm.head()

###############################################################
# GÖREV 5: Aksiyon zamanı!
###############################################################
# Adım 1: Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyini.
rfm.groupby("segment").agg({"Recency":  "mean",
                            "Frequency": "mean",
                            "Monetary": "mean"})


#                      Recency     Frequency Monetary
#                      mean         mean     mean
# segment
# about_to_sleep       113.79       2.40    359.01
# at_Risk              241.61       4.47    646.61
# cant_loose           235.44       10.70   1474.47
# champions            17.11        8.93    1406.63
# hibernating          247.95       2.39    366.27
# loyal_customers      82.59        8.37    1216.82
# need_attention       113.83       3.73    562.14
# new_customers        17.92        2.00    339.96
# potential_loyalists  37.16        3.30    533.18
# promising            58.92        2.00    335.67

rfm.head()


# Adım 2: RFM analizi yardımıyla aşağıda verilen 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv olarak kaydediniz

 """
 a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde.
 Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçilmek isteniliyor.
 Bu müşterilerin sadık ve kadın kategorisinden alışveriş yapan kişiler olması planlandı. Müşterilerin id numaralarını csv dosyasına
 yeni_marka_hedef_müşteri_id.csv olarak kaydediniz.
"""

# 2 segment seçelim: sadık ve şampiyonlar
segments = ["loyal_customers", "champions"]
rfm[rfm["segment"].isin(segments)].head()
high_segments= rfm[rfm["segment"].isin(segments)][["CustomerId", "segment"]]


# Kadın kategorisinde işlem yapanlar:
# df[df["interested_in_categories_12"].apply(lambda x: x.upper()).str.contains("KADIN")]
related_categories = df[df["interested_in_categories_12"].str.contains("KADIN")][["master_id", "interested_in_categories_12"]]
related_categories.rename(columns={"master_id": "CustomerId"}, inplace=True)
related_categories.head()

high_segments.head(2)
related_categories.head(2)

# Şimdi bu 2 dataframe'i merge edelim:
hedef_müşteri_df = related_categories.merge(high_segments, on="CustomerId", how="inner")
hedef_müşteri_df.head()
hedef_müşteri_df.to_csv("hedef_müşteri_id.csv", index=False)
hedef_müşteri_df.shape # 2497


# # Alternatif çözüm:
#
# target_segments_customer_ids = rfm[rfm["segment"].isin(["champions","loyal_customers"])]["CustomerId"]
# cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) &(df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
# cust_ids.shape # 2497
# cust_ids.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)


# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi
# müşterilerden olan ama uzun süredir alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor.
# Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv olarak kaydediniz.

rfm.groupby("segment").agg({"Recency": ["count", "mean"],
                            "Frequency": "mean",
                            "Monetary": "mean"})


# Segment Seçimi:
rfm.columns
target_segments_customers = rfm[rfm["segment"].isin(["need_attention", "cant_loose", "new_customers"])]["CustomerId"]
target_segments_customers.head()
# target_segments_customers.rename(columns={"customer_id": "master_id"}, inplace=True)

# Erkek ve çocuk ürünlerinde alışveriş yapan:

df.head()
cust_list=df[(df["interested_in_categories_12"].str.contains("ERKEK")) | (df["interested_in_categories_12"].str.contains("COCUK"))]
campaign_customers=cust_list[cust_list["master_id"].isin(target_segments_customers)]["master_id"]
# cust_list.merge(target_segments_customers, on="master_id", how="inner")

campaign_customers.to_csv("indirim_hedef_müşteri_ids.csv", index=False)
# campaign_customers.shape

###############################################################
# BONUS
###############################################################
import pandas as pd

df_ = pd.read_csv("Datasets/flo_data_20k.csv")
df = df_.copy()


def create_rfm(dataframe):
    # Veriyi Hazırlma
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)

    # RFM METRIKLERININ HESAPLANMASI
    rfm = pd.DataFrame()
    rfm["customer_id"] = dataframe["master_id"]
    rfm["recency"] = (today_date - dataframe["last_order_date"]).astype('timedelta64[D]')
    rfm["frequency"] = dataframe["order_num_total"]
    rfm["monetary"] = dataframe["customer_value_total"]

    # RF ve RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))


    # SEGMENTLERIN ISIMLENDIRILMESI
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
    rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

    return rfm[["customer_id", "recency","frequency","monetary","RF_SCORE","RFM_SCORE","segment"]]

df = df_.copy()
rfm = create_rfm(df)
rfm.head()
