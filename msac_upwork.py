import json
import os
import cloudscraper
from bs4 import BeautifulSoup as bs
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import sys
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from time import sleep
import random

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.msac.gov.au',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Safari/537.36'
}
df1 = pd.read_excel('msac_upwork_link.xlsx')
links = df1['link'].tolist()
print(len(links))
data = []
list = {}
counter = 0
with requests.Session() as s:
    for link in links:
        counter = counter + 1
        print(counter)
        print(link)
        try:
            r = s.get(link, headers=headers, timeout=60)
            soup = BeautifulSoup(r.content, 'html.parser')
        except:
            print('false request')
        # print(soup)
        datas = soup.find('div', attrs={'id': 'read'})
        try:
            if 'Status' in datas.find('h3').string:
                status = datas.find('h3').next_sibling.string
            else:
                status = 'Not Found'
        except:
            status = 'Not Found'

        strin = ''
        for string in datas.strings:
            strin = strin + string
        try:
            if 'Status' in datas.find('h3').get_text():
                description_medical_service = strin.split(str(datas.findAll('h3')[1].string))[
                    1].split(str(datas.findAll('h3')[2].string))[0]
            #     print('\n')
                description_medical_condition = strin.split(str(datas.findAll('h3')[2].string))[
                    1].split(str(datas.findAll('h3')[3].string))[0]
            #     print('\n')
                reason_for_application = strin.split(str(datas.findAll('h3')[3].string))[
                    1].split(str(datas.findAll('h3')[4].string))[0]
            else:
                description_medical_service = strin.split(str(datas.findAll('h3')[0].string))[
                    1].split(str(datas.findAll('h3')[1].string))[0]
            #     print('\n')
                description_medical_condition = strin.split(str(datas.findAll('h3')[1].string))[
                    1].split(str(datas.findAll('h3')[2].string))[0]
            #     print('\n')
                reason_for_application = strin.split(str(datas.findAll('h3')[2].string))[
                    1].split(str(datas.findAll('h3')[3].string))[0]
        except:
            description_medical_service = '-'
            description_medical_condition = '-'
            reason_for_application = '-'
        try:
            for hs in datas.findAll('h3'):
                if 'Medical Service Type' in hs.string:
                    medical_service_type = hs.next_sibling

                if 'Previous Application Number' in hs.string:
                    try:
                        previous_application_numbers = hs.next_sibling['href']
                        previous_application_number1 = hs.next_sibling.string
                        previous_application_number2 = f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{previous_application_numbers}"
                    except:
                        previous_application_number1 = hs.next_sibling.string
                        previous_application_number2 = '-'

                if 'PASC' in hs.string:
                    meetings_for_this_application_pasc = hs.next_sibling.replace(
                        'N/A', '-')

                if 'ESC' in hs.string:
                    meetings_for_this_application_esc = hs.next_sibling.replace(
                        'N/A', '-')

                if 'MSAC' in hs.string:
                    meetings_for_this_application_msac = hs.next_sibling.replace(
                        'N/A', '-')
        except:
            medical_service_type = '-'
            previous_application_number = '-'
            meetings_for_this_application_pasc = '-'
            meetings_for_this_application_esc = '-'
            meetings_for_this_application_msac = '-'

        pico_list = []
        application_form_list = []
        assesment_report_list = []
        public_summary_doc_list = []
        for hs in datas.findAll('a'):
            if 'PICO Confirmation' in hs.get_text():
                pico_list.append(
                    f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{hs['href']}")
            elif 'Final Decision Analytic Protocol (DAP)' in hs.get_text():
                pico_list.append(
                    f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{hs['href']}")

            if 'Application Form' in hs.get_text():
                application_form_list.append(
                    f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{hs['href']}")

            if 'Assessment report' in hs.get_text():
                assesment_report_list.append(
                    f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{hs['href']}")
            elif 'Assessment Report' in hs.get_text():
                assesment_report_list.append(
                    f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{hs['href']}")

            if 'One Page Summary' in hs.get_text():
                public_summary_doc_list.append(
                    f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{hs['href']}")
            elif 'Final MSAC Minutes' in hs.get_text():
                public_summary_doc_list.append(
                    f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{hs['href']}")
            elif 'One Page summary' in hs.get_text():
                public_summary_doc_list.append(
                    f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{hs['href']}")
            elif 'Public Summary Document' in hs.get_text():
                public_summary_doc_list.append(
                    f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{hs['href']}")
            elif 'One page summary' in hs.get_text():
                public_summary_doc_list.append(
                    f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{hs['href']}")
            elif 'Public Summary Document (PSD) TUNA' in hs.get_text():
                public_summary_doc_list.append(
                    f"http://www.msac.gov.au/internet/msac/publishing.nsf/Content/{hs['href']}")

        if len(pico_list) == 0:
            pico_confirmation1 = '-'
            pico_confirmation2 = '-'
        if len(pico_list) == 1:
            pico_confirmation1 = pico_list[0]
            pico_confirmation2 = '-'
        if len(pico_list) == 2:
            pico_confirmation1 = pico_list[0]
            pico_confirmation2 = pico_list[1]

        if len(application_form_list) == 0:
            application_form1 = '-'
            application_form2 = '-'
        if len(application_form_list) == 1:
            application_form1 = application_form_list[0]
            application_form2 = '-'
        if len(application_form_list) == 2:
            application_form1 = application_form_list[0]
            application_form2 = application_form_list[1]

        if len(assesment_report_list) == 0:
            assesment_report1 = '-'
            assesment_report2 = '-'
        if len(assesment_report_list) == 1:
            assesment_report1 = assesment_report_list[0]
            assesment_report2 = '-'
        if len(assesment_report_list) == 2:
            assesment_report1 = assesment_report_list[0]
            assesment_report2 = assesment_report_list[1]

        if len(public_summary_doc_list) == 0:
            public_summary_doc1 = '-'
            public_summary_doc2 = '-'
            public_summary_doc3 = '-'
            public_summary_doc4 = '-'
        if len(public_summary_doc_list) == 1:
            public_summary_doc1 = public_summary_doc_list[0]
            public_summary_doc2 = '-'
            public_summary_doc3 = '-'
            public_summary_doc4 = '-'
        if len(public_summary_doc_list) == 2:
            public_summary_doc1 = public_summary_doc_list[0]
            public_summary_doc2 = public_summary_doc_list[1]
            public_summary_doc3 = '-'
            public_summary_doc4 = '-'
        if len(public_summary_doc_list) == 3:
            public_summary_doc1 = public_summary_doc_list[0]
            public_summary_doc2 = public_summary_doc_list[1]
            public_summary_doc3 = public_summary_doc_list[2]
            public_summary_doc4 = '-'
        if len(public_summary_doc_list) == 4:
            public_summary_doc1 = public_summary_doc_list[0]
            public_summary_doc2 = public_summary_doc_list[1]
            public_summary_doc3 = public_summary_doc_list[2]
            public_summary_doc4 = public_summary_doc_list[3]

        list = {
            'Url': link,
            'Status': status,
            'Description of Medical Service': description_medical_service,
            'Description of Medical Condition': description_medical_condition,
            'Reason for Application': reason_for_application,
            'Medical Service Type': medical_service_type,
            'Previous Application Number': previous_application_number1,
            'Previous Application Link': previous_application_number2,
            'Application Form 1': application_form1,
            'Application Form 2': application_form2,
            'PICO Confirmation 1': pico_confirmation1,
            'PICO Confirmation 2': pico_confirmation2,
            'Assessment Report 1': assesment_report1,
            'Assessment Report 2': assesment_report2,
            'Public Summary Document 1': public_summary_doc1,
            'Public Summary Document 2': public_summary_doc2,
            'Public Summary Document 3': public_summary_doc3,
            'Public Summary Document 4': public_summary_doc4,
            'Meetings for this Application - PASC': meetings_for_this_application_pasc,
            'Meetings for this Application - ESC': meetings_for_this_application_esc,
            'Meetings for this Application - MSAC': meetings_for_this_application_msac
        }
        data.append(list)

# print(status)
# print(description_medical_service)
# print(description_medical_condition)
# print(reason_for_application)
# print(medical_service_type)
# print(previous_application_number)
# print(application_form)
# print(pico_confirmation)
# print(assesment_report)
# print(public_summary_doc)
# print(meetings_for_this_application_pasc)
# print(meetings_for_this_application_esc)
# print(meetings_for_this_application_msac)


df1 = pd.DataFrame(data)
df = df1.reset_index(drop=True)
df.to_csv('msac2.csv', encoding='utf-8-sig', index=False)
