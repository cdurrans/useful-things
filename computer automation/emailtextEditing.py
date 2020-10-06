

import os, shutil
emailName = "Address Unknown"
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






emailTitle = "Address Unknown"


# Sib=<p>Dear [Members Name],</p><p>We have contacted you using the e-mail address you have provided for use by The Church of Jesus Christ of Latter-day Saints.</p><p>We have been notified that your [RELATIONSHIP], [MTLS NAME], has moved, and we no longer have their current address. Please help us send their membership record to the correct ward or branch by returning their current address and telephone number in a reply email.</p><p>A residential address is preferred.</p><p>Thank you,</p><p>Member Services <br /><a href="mailto:MemberLocators@churchofjesuschrist.org">MemberLocators@churchofjesuschrist.org</a><strong><br /> </strong><small>[Sequence]_[MTLS MRN]</small></p>


p1 = """
Dear [Members Name],                                                                             
"""
p2 = """
We have contacted you using the e-mail address you have provided for use by The Church of Jesus Christ of Latter-day Saints.
"""
p3 = """
We have been notified that your place of residence has changed, and we no longer have your current address. Please help us send your membership record to your new ward or branch by replying to this email with your current residential address and phone number.
"""
p4b = """
Thank you,
"""
p5 = """
Member Services
"""
p6 = """
Member Services <br/><a href="mailto:MemberLocators@churchofjesuschrist.org">MemberLocators@churchofjesuschrist.org</a><strong><br/> </strong><small>[Sequence]_[MTLS MRN]</small>
"""

paragraphsList = [p1,p2,p3,p4b,p5,p6]

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