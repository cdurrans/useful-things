

import os, shutil
emailName = "Gift Aid UK v2"
base_file_location = "C:/Users/cdurrans/Downloads/EmailDocuments/"
templateFileLocation = base_file_location + "gsdTestTemplate.html"
destination = base_file_location + emailName +".html"

shutil.copy(templateFileLocation, destination)


def insertBoldText(textToBold):
    message = """ <strong><span style='font-family:"Arial",sans-serif'> """
    message += textToBold
    message += """</span></strong>"""
    return message

def insertParagraph(paragraph_text):
    paragraphText = """<span style='font-size:13.5pt;font-family:"Arial",sans-serif;
    mso-fareast-font-family:"Times New Roman";color:#222325'>"""
    paragraphText += paragraph_text
    paragraphText += """</span><span style='mso-fareast-font-family:"Times New Roman"; color:black;mso-color-alt:windowtext'>
    <br>
    <img border=0 width=2 height=20 id="_x0000_i1032"
    src="http://image.email.ldschurch.org/lib/fe8a1372756d06747d/m/2/LDS_Spacer.gif"
    class=tableRebrand><br>
    </span>"""
    return paragraphText

emailTitle = "Gift Aid (GA) Individual Statement/s of Contribution/s Tax Year April 2019 – April 2020"

p1 = """
Dear Bishops and Branch Presidents,                                                                             
"""
p2 = """
The “Gift Aid Donation Details” individual statements were posted to you on the 23rd April 2020 for the GA donors in your unit. Please can you distribute these to your members when possible, with the utmost care to ensure the confidentiality of these statements. If a member requires their statement before the lockdown is lifted, please ask them to contact us on the email below to request a second copy.
"""
p3 = """
Note : If you have not received these Statements, please ignore this message, as you may not have donors from your Ward paying their donations through GA. Some GA donors have already received their Statements via email. If there were only less than 3 statements per unit, we have directly sent them by post to their respective addresses.
"""
p4b = """
Please stress the importance of the safe keeping of the statement if required for self- assessments, so the Gift Team are not continuously asked for further copies.
"""
p5 = """
If members have any questions or concerns regarding the contents of their statements, please direct them to contact the Gift Aid Department. 
"""
p6 = """
E-mail:- giftaid@churchofjesuschrist.org 
"""
p7 = """
If you are aware of any changes to a member’s address or any incomplete addresses, please can you instruct your ward/branch clerk to correct them in LCR.
"""
p8 = """
New rules from the HMRC require that we have to include a postcode on all UK addresses being submitted for Gift Aid claims, failure to do so will result in a delay of the claim. <br>
"""

p9a = """Thank you for your assistance in this matter. """

p9 = """
Kind regards,
"""
p10 = """Luis B Silva"""
p11 = """Gift Aid Manager"""

paragraphsList = [p1,p2,p3,insertBoldText(p4b),p5,p6,insertBoldText(p7),p8,p9,p9a,p10,p11]


message = ""
for pa in paragraphsList:
    message += insertParagraph(pa)



f= open(destination, 'r')
ftxt = f.read()
f.close()

callingsStr = "Bishops and Branch Presidents"


ftxt = ftxt.replace("__Title_Email__",emailTitle)
ftxt = ftxt.replace("__paragraph_text__",message)
ftxt = ftxt.replace("__Callings_Included__",callingsStr)


f= open(destination, 'w')
f.write(ftxt)
f.close()