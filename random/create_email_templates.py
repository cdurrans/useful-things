import os 
import sys 
sys.path.insert(0,'//w17568/Shared Folders/Python Scripts/')
import pandas as pd 
from shutil import copyfile
import pyodbc
import shutil
import time
from dbTools import DBTools
import easygui
from datetime import datetime



mydb = DBTools('w13107','MLU')

df = mydb.query_data("""
select *
from atr_temp
where [Type] = 'Reminder'

""")



def populate_language_content(emailBuilt, inf_dict):
    emailBuilt = emailBuilt.replace("__email_type_category__", inf_dict.get("__email_type_category__", "Error"))
    emailBuilt = emailBuilt.replace("__email_includes__", inf_dict.get("__email_includes__", "Error"))
    emailBuilt = emailBuilt.replace("__email_address_header__", inf_dict.get("__email_address_header__", "Error"))
    emailBuilt = emailBuilt.replace("__intellectual__reserve__", inf_dict.get("__intellectual__reserve__", "Error"))
    emailBuilt = emailBuilt.replace("__terms_of_use_header__", inf_dict.get("__terms_of_use_header__", "Error"))
    emailBuilt = emailBuilt.replace("__privacy_notice_header__", inf_dict.get("__privacy_notice_header__", "Error"))
    emailBuilt = emailBuilt.replace("[__3digit_lang_code__]", inf_dict.get("[__3digit_lang_code__]", "Error"))
    return emailBuilt


def populate_content(content, emailBuilt):
    emailBuilt = emailBuilt.replace("__pre_header_start__", "")
    emailBuilt = emailBuilt.replace("__email_title__", "")
    content = content.replace("<p>","")
    content = content.replace("</p>","\n")
    paragraphs = content.split('\n')
    newEmailBody = ""
    paragraphSpacer = '<tr><td height="20" style="height: 20px;"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" width="1" height="1" border="0" style="display:block;"/></td> </tr> '
    for par in paragraphs:
        newEmailBody += '<tr> <td class="em_blue_M" align="left" valign="top" style="font-family:Arial, sans-serif; font-size:16px; line-height:22px; color:#222325;">'
        newEmailBody += par + "</td></tr>" + paragraphSpacer;
    emailBuilt = emailBuilt.replace("__EMAIL_BODY__", newEmailBody);
    return emailBuilt;


new_template = open("//w13107/GSC-Reporting/Visual Studio 2015/EmailAppWPF/EmailAppWPF/Language_INFs/new_template.html", "r", encoding="utf8")
new_template_txt = new_template.read()
new_template.close()

for indx, row in df.iterrows():
    lan_inf_file_location = "//w13107/GSC-Reporting/Visual Studio 2015/EmailAppWPF/EmailAppWPF/Language_INFs/" + row["Language"] + ".inf"
    if not os.path.exists(lan_inf_file_location):
        lan_inf_file_location = "//w13107/GSC-Reporting/Visual Studio 2015/EmailAppWPF/EmailAppWPF/Language_INFs/" + "English.inf"
    inf_dict = dict()
    file_raw = open(lan_inf_file_location, "r", encoding="utf8")
    email_content = new_template_txt
    for line in file_raw:
        print(line)
        pieces = str(line).split("=")
        if len(pieces) == 2:
            inf_dict[pieces[0]] = pieces[1].replace("\n","")
    file_raw.close()
    email_content = populate_language_content(email_content, inf_dict)
    email_content = populate_content(row["Body"], email_content)
    f = open(f'Y:/testSite/EmailDocuments/ATR/ATR_draft_{row["Language"]}.html', 'w', encoding='utf8')
    f.write(email_content)
    f.close()

    

print(inf_dict)



sql = "select Email_From_Address,email,email_subject, email_body, status from MLU.dbo.SNSend where isnull(status,0) <> 1 order by [Unit_Number]";