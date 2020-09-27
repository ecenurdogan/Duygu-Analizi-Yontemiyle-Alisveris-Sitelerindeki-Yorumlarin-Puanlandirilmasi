import pandas as pd
import numpy as np
import nltk
from pandas import DataFrame 
from pandas import ExcelWriter
import zemberek_python
from zemberek_python import main_libs as ml
from sklearn.linear_model import LinearRegression

#
#Exceldeki dosyayı belli bir sheetindeki tüm verileri okuma
df=pd.read_excel('yorumlar.xlsx',sheetname='Fahrenheid 451 39202')

zemberek_api = ml.zemberek_api(libjvmpath="C:\Program Files\Java\jre1.8.0_152\bin\server",
                               zemberekJarpath="./zemberek_python/zemberek-tum-2.0.jar").zemberek()
    

yorumSayisi=df.shape[0]   
yorumKelimeDict = {} #bu matrix olusturmaya calistigimiz dictionary 

yorum = df.loc[0][2]                                                                                                
yorum = yorum.lower()  # Tüm harfleri küçük harf haline getirme
yorumKelimeList = ml.ZemberekTool(zemberek_api).cumleyi_parcalara_ayir(yorum)
#yorumKelimeListKok= ml.ZemberekTool(zemberek_api).metinde_gecen_kokleri_bul(yorumKelimeList) 

for kelime in yorumKelimeList:
    yorumKelimeDict.update({kelime:[1]})
    
for i in range(1,yorumSayisi): #her bir yorum icin  
    #herbir yorumda 
    for kel in yorumKelimeDict:
            gorulmeListesi = yorumKelimeDict[kel]
            gorulmeListesi.append(0) #listenin sonuna 0 ekle
            yorumKelimeDict[kel] = gorulmeListesi
        
    yorum = df.loc[i][2]                                                                                                
    yorum = yorum.lower()  # Tüm harfleri küçük harf haline getirme
    yorumKelimeList = ml.ZemberekTool(zemberek_api).cumleyi_parcalara_ayir(yorum)
    #yorumKelimeListKok= ml.ZemberekTool(zemberek_api).metinde_gecen_kokleri_bul(yorumKelimeList)
    #kelimeSayisi = len(yorumKelimeListKok)
    
    for kelime in yorumKelimeList: #her bir kelime icin
        suAnaDekGorulmusKelimeler = list(yorumKelimeDict.keys())
        if kelime in suAnaDekGorulmusKelimeler: #eger kelime daha once gorulmusse
            gorulmeListesi = yorumKelimeDict[kelime]
            gorulmeListesi[-1]= gorulmeListesi[-1] +1 #kelimenin gorulme sayisini 1 artir
            yorumKelimeDict[kelime] = gorulmeListesi
        else:  #eger kelime daha once gorulmemisse 
            yeniGorulmeListesi = [0]*(i+1)
            yeniGorulmeListesi[-1] = 1
            yorumKelimeDict.update({kelime:yeniGorulmeListesi})
            
yorumPuani= df.iloc[:,3] #yorumlarin oldugu colon           
finalDF =DataFrame(yorumKelimeDict, columns=list(yorumKelimeDict.keys()))
#finalDF.insert(finalDF.shape[1],"Yorum Puani", yorumPuani)
#file = ExcelWriter('sth2.xlsx')
#finalDF.to_excel(file,'Sheet1',index=False)
#file.save()

###Regresyon bolumu#######
finalDFnp=np.array(finalDF)
yorumPuaninp=np.array(yorumPuani)
model = LinearRegression().fit(finalDFnp, yorumPuaninp)
############################

########yorumu al###########
kisiYorumu= input('Kitap hakkindaki yorumlarinizi yaziniz: \n') #amacimiz bu yorumu binary vektor haline getirmek
kisiYorumu = kisiYorumu.lower()
kisiYorumKelimeList = ml.ZemberekTool(zemberek_api).cumleyi_parcalara_ayir(kisiYorumu)
#yorum kelime list'teki her bir kelimenin daha once gorulup gorulmedigine bakalim
suAnaDekGorulmusKelimeler = list(yorumKelimeDict.keys())
suAnaDekGorulmusToplamKelimeSayisi=len(suAnaDekGorulmusKelimeler)
kisiYorumuVektor=[0]*suAnaDekGorulmusToplamKelimeSayisi 


for kelime in kisiYorumKelimeList: #her bir kelime icin
    if kelime in suAnaDekGorulmusKelimeler: #eger kelime daha once gorulmusse
       kacinciKelime=suAnaDekGorulmusKelimeler.index(kelime)
       kisiYorumuVektor[kacinciKelime]=1
       
kisiYorumuVektor = np.array(kisiYorumuVektor)        
############## Tahmin######
tahminiSkor =np.dot(kisiYorumuVektor,model.coef_)+ model.intercept_

print('Yazdiginiz yoruma gore kitaba vereceginiz tahmini puan:', round(tahminiSkor,2))
