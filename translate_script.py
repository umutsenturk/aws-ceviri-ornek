#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# AWS ile SDK bağlamtısı için gerekli modül.
import boto3

translate = boto3.client(service_name='translate', region_name='eu-central-1', use_ssl=True)

def translate_normal():
    
    result = translate.translate_text(Text="Prime Video", SourceLanguageCode="en", TargetLanguageCode="tr")

    print(result)
    print('Çeviri sonucu: ' + result.get('TranslatedText'))
    print('Kaynak çeviri dili: ' + result.get('SourceLanguageCode'))
    print('Hedef çeviri dili: ' + result.get('TargetLanguageCode'))




def terminoloji_import():
    # terminology.csv içindeki veriler:
    '''
    en,tr
    Amazon Family,Amazon Ailesi
    '''

    # Terminoloji dosyasını okuma
    with open('terminology.csv', 'rb') as f:
        data = f.read()
    file_data = bytearray(data)

    # Terminoloji verilerini, amazon'a import etme
    response = translate.import_terminology(Name='terminoloji',
                                            MergeStrategy='OVERWRITE',
                                            TerminologyData={"File": file_data, "Format": 'CSV'})

    # Terminolojinin özelliklerini görmek için kullanılan kod
    print(response.get('TerminologyProperties'))
    print("\n")


    # Import edilen terminolojiyi çekmek
    response = translate.get_terminology(Name='terminoloji',
                                        TerminologyDataFormat='CSV')
    
    # Import edilen terminoloji özellikleri
    print(response.get('TerminologyProperties'))


    # Terminoloji dosyasınnı indirmek için lokasyon, link
    response.get('TerminologyDataLocation').get('Location')
    
    
    print("\n")
    
    # MaxResults ile sınırlandırılabilen terminoloji listeleme
    response = translate.list_terminologies(MaxResults=10)
    
    # Bütün terminolojileri yazdırma
    print(response.get('TerminologyPropertiesList'))
    print("\n")




    




    # Terminolojisiz yazdırma
    response = translate.translate_text(Text="Amazon Family",
                                        SourceLanguageCode="en",
                                        TargetLanguageCode="tr")

    print("Çeviri sonrası: " + response.get('TranslatedText'))
    print("\n")
    
    # TerminologyNames=["terminology_name"] ile Terminolojili yazdırma
    response = translate.translate_text(Text="Amazon Family", TerminologyNames=["terminoloji"], SourceLanguageCode="en", TargetLanguageCode="tr")

    print("Çeviri sonrası: " + response.get('TranslatedText'))
    print("\n")



def terminoloji_update():
    # Güncellenen dosya içeriği:
    '''
    en,tr
    Amazon Family,Amazon Ailesi
    Prime Video, Prime Video
    '''
    # Güncellenmiş terminoloji dosyasını okuma
    with open('guncellenmis_terminoloji.csv', 'rb') as f:
        data = f.read()
    file_data = bytearray(data)


    # Terminolojiyi güncelleme
    response = translate.import_terminology(Name='terminoloji',
                                            MergeStrategy='OVERWRITE',
                                            TerminologyData={"File": file_data, "Format": 'CSV'})
    print("Güncellenmiş Dosya özellikleri: ")
    print(response.get('TerminologyProperties'))
    print("\n")


    # Terminoloji olmadan çeviri
    response = translate.translate_text(Text="Prime Video",
                                        SourceLanguageCode="en",
                                        TargetLanguageCode="tr")
    print("Güncelleme dosyası olmadan çeviri: " + response.get('TranslatedText'))
    print("\n")

    # Güncellenen terminoloji dosyası ile çeviri
    response = translate.translate_text(Text="Prime Video", TerminologyNames=["terminoloji"], SourceLanguageCode="en", TargetLanguageCode="tr")
    print("Güncelleme dosyası ile çeviri: " + response.get('TranslatedText'))
    print("\n")


def terminoloji_delete():
    translate.delete_terminology(Name="terminoloji")
    print("Terminoloji silindi.")



if __name__ == "__main__":
    translate_normal()
    terminoloji_import()
    terminoloji_update()
    terminoloji_delete()