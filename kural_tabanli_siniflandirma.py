
#############################################
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
# Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak seviye tabanlı (level based) yeni müşteri tanımları (persona)
# oluşturmak ve bu yeni müşteri tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete
# ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.
#############################################
# Veri Seti Hikayesi
#############################################
# Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını ve bu ürünleri satın alan kullanıcıların bazı
# demografik bilgilerini barındırmaktadır. Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo
# tekilleştirilmemiştir. Diğer bir ifade ile belirli demografik özelliklere sahip bir kullanıcı birden fazla alışveriş yapmış olabilir.

# Price: Müşterinin harcama tutarı
# Source: Müşterinin bağlandığı cihaz türü
# Sex: Müşterinin cinsiyeti
# Country: Müşterinin ülkesi
# Age: Müşterinin yaşı

################# Uygulama Öncesi #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# Uygulama Sonrası #####################

#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C


#############################################
# PROJE GÖREVLERİ
#############################################

#############################################

# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option("display.max_rows",None)
df=pd.read_csv("persona.csv")
df.head()
df.describe()
df.shape
df.info()
# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique() #kac tane unique var 
df["SOURCE"].unique() #ve bunlar nelerdir
df["SOURCE"].value_counts(normalize=True) #her değerden ne kadar olduğunu
#hesaplayıp normalize ile yüzdeliğe çevirdim

# Soru 3: Kaç unique PRICE vardır?
df["PRICE"].nunique()
# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts(normalize=True)
df["PRICE"].hist()
plt.show()
# Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()
df.groupby("COUNTRY")["PRICE"].count() #ülkeye göre gruplandır prıce a gore sayı al
df.pivot_table(values="PRICE",index="COUNTRY",aggfunc="count")

# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY")["PRICE"].sum()
df.groupby("COUNTRY").agg({"PRICE":"sum"})
df.pivot_table(values="PRICE",index="COUNTRY",aggfunc="sum")
#agg() fonksiyonu, bir grup üzerinde birden fazla işlem gerçekleştirmek için oldukça kullanışlıdır
# ve gruplama işlemleri sonrası uygulanabilir.


# Soru 7: SOURCE türlerine göre satış sayıları nedir?
df["SOURCE"].value_counts()

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?
df["PRICE"].mean()

# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE")["PRICE"].mean()

# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(by=["COUNTRY","SOURCE"]).agg({"PRICE":"mean"})

#############################################
# GÖREV 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################
df.groupby(by=["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"})

#############################################
# GÖREV 3: Çıktıyı PRICE'a göre sıralayınız.
#############################################
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.
agg_df=df.groupby(by=["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}).sort_values("PRICE",ascending=False)
agg_df

#############################################
# GÖREV 4: Indekste yer alan isimleri değişken ismine çeviriniz.
#############################################
agg_df.reset_index()
agg_df.reset_index(inplace=True)
agg_df
#inplace=True, Pandas'ta yapılan işlemlerin orijinal DataFrame veya seriyi doğrudan etkilemesini sağlar. 
# Bu, özellikle büyük veri setlerinde bellek verimliliği açısından faydalıdır

#############################################
# GÖREV 5: AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
#############################################
bins=[0,18,23,30,40,agg_df["AGE"].max()]
mylabels=["0_18","18_23","23_30","31_40","41_"+str(agg_df["AGE"].max())]
agg_df["age_cat"]=pd.cut(agg_df["AGE"],bins,labels=mylabels)
agg_df

#############################################
# GÖREV 6: Yeni level based müşterileri tanımlayınız ve veri setine değişken olarak ekleyiniz.
#############################################
agg_df["customers_level_based"]=agg_df[["COUNTRY","SOURCE","SEX","age_cat"]].agg(
    lambda x:"_".join(x).upper(),axis=1
)
#her bir satır için COUNTRY, SOURCE, SEX ve age_cat sütunlarının değerlerini _ ile 
# birleştirerek büyük harfe dönüştürüp yeni bir customers_level_based sütunu oluşturur. 

agg_df=agg_df.groupby("customers_level_based").agg({"PRICE":"mean"})
# her grup için ortalama fiyat değerlerini içeren yeni bir DataFrame oluşturur
#tekilleştirme işlemş yaptım 
agg_df=agg_df.reset_index()
agg_df.head()
#customer level basedi indexteydi onu sutuna cektim
#############################################
# GÖREV 7: Yeni müşterileri (USA_ANDROID_MALE_0_18) segmentlere ayırınız.
#############################################
agg_df["SEGMENT"]=pd.qcut(agg_df["PRICE"],4,labels=["D","C","B","A"])
#4 SEGMENT OLUŞTURDUM PRICE A GORE 
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE":"mean"})

#############################################
# GÖREV 8: Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user="TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"]==new_user]


# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?
new_user="FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"]==new_user]
