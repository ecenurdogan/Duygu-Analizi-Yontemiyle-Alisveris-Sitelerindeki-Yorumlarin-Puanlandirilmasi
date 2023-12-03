import pandas as pd
import zemberek_python
import nltk
from pandas import DataFrame 
from pandas import ExcelWriter
from zemberek_python import main_libs as ml

#
#Exceldeki dosyayı belli bir sheetindeki tüm verileri okuma
df=pd.read_excel('yorumlar.xlsx',sheetname='SATRANÇ Stefan Zweig 28004')
#
#Zemberek ile ilgili dosya uygun klasöre yerleştirildi.
zemberek_api = ml.zemberek_api(libjvmpath="C:\Program Files\Java\jre1.8.0_152\bin\server",
                               zemberekJarpath="./zemberek_python/zemberek-tum-2.0.jar").zemberek()
  

yorumSayisi=df.shape[0]   
yorumKelimeDict = {} #bu matrix olusturmaya calistigimiz dictionary 

yorum = df.loc[0][2]                                                                                                
yorum = yorum.lower()  # Tüm harfleri küçük harf haline getirme
yorumKelimeList = ml.ZemberekTool(zemberek_api).cumleyi_parcalara_ayir(yorum)
yorumKelimeListKok= ml.ZemberekTool(zemberek_api).metinde_gecen_kokleri_bul(yorumKelimeList) 

for kelime in yorumKelimeListKok:
    yorumKelimeDict.update({kelime:[1]})
    
for i in range(1,yorumSayisi): #her bir yorum icin  
    for kel in yorumKelimeDict:
            gorulmeListesi = yorumKelimeDict[kel]
            gorulmeListesi.append(0) 
            yorumKelimeDict[kel] = gorulmeListesi
        
    yorum = df.loc[i][2]                                                                                                
    yorum = yorum.lower()  # Tüm harfleri küçük harf haline getirme
    yorumKelimeList = ml.ZemberekTool(zemberek_api).cumleyi_parcalara_ayir(yorum)
    yorumKelimeListKok= ml.ZemberekTool(zemberek_api).metinde_gecen_kokleri_bul(yorumKelimeList)
    #kelimeSayisi = len(yorumKelimeListKok)
    
    for kelime in yorumKelimeListKok: #her bir kelime icin
        suAnaDekGorulmusKelimeler = list(yorumKelimeDict.keys())
        if kelime in suAnaDekGorulmusKelimeler: #eger kelime daha once gorulmusse
            gorulmeListesi = yorumKelimeDict[kelime]
            gorulmeListesi[-1]= gorulmeListesi[-1] +1 #kelimenin gorulme sayisini 1 artir
            yorumKelimeDict[kelime] = gorulmeListesi
        else:  #eger kelime daha once gorulmemisse 
            yeniGorulmeListesi = [0]*(i+1)
            yeniGorulmeListesi[-1] = 1
            yorumKelimeDict.update({kelime:yeniGorulmeListesi})
            
yorumPuani= df.iloc[:,3] #yorumlarin oldugu kolon           
finalDF = myDF=DataFrame(yorumKelimeDict, columns=list(yorumKelimeDict.keys()))
finalDF.insert(finalDF.shape[1],"Yorum Puani", yorumPuani)
#yorum_kelime_sayisi.xlsx isimli yeni bir excel dosyasının oluşturulması
file = ExcelWriter('yorum_kelime_sayisi.xlsx') 
finalDF.to_excel(file,'Sheet1',index=False)
#Oluşturulan dosyanın kaydedilmesi
file.save()
