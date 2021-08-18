

import os, shutil
import docx
base_file_location = "Y:/testSite/EmailDocuments/MSR/06252021_cde_mission_pilot/Translated Message (Organized)/Translated Message/"
templateFileLocation = "Y:/Visual Studio 2015/EmailAppWPF/EmailAppWPF/MyCallingEmailTemplate.html"

# shutil.copy(templateFileLocation, destination)


def insertBoldText(textToBold):
    message = """ <strong><span style='font-family:"Arial",sans-serif'> """
    message += textToBold
    message += """</span></strong>"""
    return message

def insertParagraph(paragraph_text):
    newEmailBody = ""
    paragraph_spacer = """ <tr><td height="20" style="height: 20px;"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" width="1" height="1" border="0" style="display:block;"/></td> </tr> """
    newEmailBody += """ <tr> <td class="em_blue_M" align="left" valign="top" style="font-family:Arial, sans-serif; font-size:16px; line-height:22px; color:#222325;"> """
    newEmailBody += paragraph_text + "</td></tr>" + paragraph_spacer
    return newEmailBody


header_template = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
xmlns:v="urn:schemas-microsoft-com:vml"
xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<!--[if gte mso 9]><xml>
<o:OfficeDocumentSettings>
<o:AllowPNG/>
<o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings>
</xml><![endif]-->
<title>The Church of Jesus Christ of Latter-day Saints</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta name="viewport" content="width=device-width, initial-scale=1.0 " />
<meta name="format-detection" content="telephone=no"/>
<style type="text/css">
body {
	margin: 0;
	padding: 0;
	-webkit-text-size-adjust: 100% !important;
	-ms-text-size-adjust: 100% !important;
	-webkit-font-smoothing: antialiased !important;
}
img {
	border: 0 !important;
	outline: none !important;
}
p {
	Margin: 0px !important;
	Padding: 0px !important;
}
table {
	border-collapse: collapse;
	mso-table-lspace: 0px;
	mso-table-rspace: 0px;
}
td, a, span {
	border-collapse: collapse;
	mso-line-height-rule: exactly;
}
.ExternalClass * {
	line-height: 100%;
}
.em_defaultlink a {
	color: inherit;
	text-decoration: none;
}
.em_g_img + div {
	display: none;
}
a[x-apple-data-detectors], u + .em_body a, #MessageViewBody a {
	color: inherit;
	text-decoration: none;
	font-size: inherit !important;
	font-family: inherit !important;
	font-weight: inherit !important;
	line-height: inherit !important;
}
table {
	table-layout: fixed;
}
.em_gray_M a {
	color: #535559;
	text-decoration: underline;
}
.em_blue_M a {
	color: #177C9C;
	text-decoration: underline;
}
.em_gray1 a {
	color: #535559;
	text-decoration: none;
}
center table {
	width: 100% !important;
}
@media only screen and (max-width:599px) {
.em_main_table {
	width: 100%!important;
}
.em_wrapper {
	width: 100%!important;
}
.em_hide {
	display: none!important;
}
.em_full_img img {
	width: 100%!important;
	height: auto!important;
	max-width: none!important;
}
.em_side15 {
	width: 15px!important;
}
.em_ptop {
	padding-top: 20px!important;
}
.em_pbottom {
	padding-bottom: 15px!important;
}
.em_h20 {
	height: 20px!important;
	font-size: 1px!important;
	line-height: 1px!important;
}
.em_h30 {
	height: 30px!important;
}
.em_mob_block {
	display: block!important;
}
.em_img1 {
	width: 81px!important;
	height: auto!important;
}
.em_pbottom1 {
	padding-bottom: 40px!important;
}
.em_padding {
	padding-top: 50px!important;
	padding-bottom: 50px!important;
}
.em_ptop1 {
	padding-top: 40px!important;
}
.em_gap {
	padding-top: 28px!important;
	padding-bottom: 28px!important;
}
.em_border_none {
	border: none!important;
}
.em_ptop35 {
	padding-top: 35px!important;
}
.em_side25 {
	width: 25px!important;
}
u+.em_body .em_full_wrap {
	width: 100%!important;
	width: 100vw!important;
}
}

ul { margin: 0!important; padding-left: 27px!important; }
ol { margin: 0!important; padding-left: 27px!important; }
li { padding-left: 10px!important; display: list-item!important;}
li ul { list-style-type: circle!important; }
li ol { list-style-type: lower-alpha!important; }

.darkmodefilter {

    background-image: url("http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/4/FFFFFF-1.png");

}
font {display: none}
ul li { margin-bottom: 10px; }
</style>

<!--POST
%%[
Var @cid Set @cid = "MC_MRA20_051520"
]%%
POST-->


</head>

<body class="em_body" style="margin:0px auto; padding:0px;" bgcolor="#eff0f0">
<table width="100%" border="0" cellspacing="0" cellpadding="20" class="em_full_wrap" bgcolor="#eff0f0" style="table-layout:fixed;">
  <tr>
    <td align="center" valign="top">
        <table align="center" width="600" border="0" cellspacing="0" cellpadding="0" class="em_main_table" style="width:600px;">
        <!--Header Section-->
        <tr>
          <td valign="top">
          <!--- PREHEADER start --->
              <table class="em_hide" width="600" border="0" cellpadding="0" cellspacing="0">
              <tr>
                <td class="em_hide" style="border-collapse: collapse;" width="300" height="0" bgcolor="#eff0f0" align="left" valign="middle"><font style="text-decoration:none; color:#eff0f0; font-size:0px; font-family:helvetica, arial, sans-serif;">__pre_header_start__</font></td>
                    <td style="border-collapse: collapse;" width="300" height="0" bgcolor="#eff0f0" align="right" valign="middle">&nbsp;</td>
              </tr>
              </table>
		      <!--- PREHEADER end --->

          <!--- Subject start --->
              <table class="em_hide" width="600" border="0" cellpadding="0" cellspacing="0">
              <tr>
                <td class="em_hide" style="border-collapse: collapse;" width="300" height="0" bgcolor="#eff0f0" align="left" valign="middle"><font style="text-decoration:none; color:#eff0f0; font-size:0px; font-family:helvetica, arial, sans-serif;">__email_subject__</font></td>

                <td style="border-collapse: collapse;" width="300" height="0" bgcolor="#eff0f0" align="right" valign="middle">&nbsp;</td>
              </tr>
              </table>
          <!--- Subject end --->
              <table width="600" border="0" cellspacing="0" cellpadding="0" style="width:600px;" class="em_wrapper" bgcolor="#ffffff">
              <tr>
                <td align="center" valign="top" class="darkmodefilter">
                <!--[if gte mso 9]>
                  <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px; height:100px;">
                    <v:fill type="tile" src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/4/FFFFFF-1.png" color="#ffffff" />
                    <v:textbox inset="0,0,0,0">
                <![endif]-->
                  <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">
                    <tr>
                      <td align="center" valign="top" width="92" style="width:92px;" class="em_img1"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/4/image_12.jpg" width="92" height="100" alt="" border="0" style="display:block; max-width:92px;" class="em_img1" /></td>
                      <td align="center" valign="middle" ><a alias="Logo" href="https://www.churchofjesuschrist.org/?lang=__three_digit_code__&cid=email-%%=v(@cid)=%%_Logo" target="_blank" style="text-decoration:none;"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/4/ChurchLogoGVSG-0420___three_digit_code__.png" width="135" alt="The Church of Jesus Christ of Latter-day Saints" border="0" style="display:block; max-width:135px; font-family:Arial, sans-serif; font-size:16px; line-height:22px; color:#000000; padding: 10px" /></a></td>
                      <td width="92" style="width:92px;" class="em_img1"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" width="1" height="1" border="0" style="display:block;" /></td>
                    </tr>
                  </table>
                <!--[if gte mso 9]>
                    </v:textbox>
                  </v:rect>
                <![endif]-->
                </td>
              </tr>
              <tr>
                <td height="1" style="height:1px; font-size:0px; line-height:0px;" bgcolor="#EFF0F0"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" width="1" height="1" border="0" style="display:block;" /></td>
              </tr>
              <tr>
                <td class="em_defaultlink" align="center" valign="top" style="font-family:Arial, sans-serif; font-size:14px; line-height:20px; color:#878A8C; padding:10px 15px 8px;" bgcolor="#ffffff">__email_type_category__</td>
              </tr>
              <tr>
                <td height="1" style="height:1px; font-size:0px; line-height:0px;" bgcolor="#EFF0F0"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" width="1" height="1" border="0" style="display:block;" /></td>
              </tr>
            </table>
            </td>
        </tr>
        <!--//Header Section--> 
        <!--Title, Text and CTA Section-->
        <tr>
          <td valign="top">
              <table width="600" border="0" cellspacing="0" cellpadding="0" style="width:600px;" class="em_wrapper" bgcolor="#ffffff">
              <tr>
                <td align="center" valign="top" style="padding:0px 25px;">
                    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">
                        <tr>
                            <td height="35" style="height:35px;"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" width="1" height="1" border="0" style="display:block;" /></td>
                        </tr>
                        <tr>
                            <td height="20" style="height:20px;"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" width="1" height="1" border="0" style="display:block;" /></td>
                        </tr>
"""


footer_template = """
                    </table>
                  </td>
              </tr>
            </table>
            </td>
        </tr>
        <!--//Title, Text and CTA Section--> 
        <!-- Footer Section -->
        <tr>
          <td valign="top" align="center">
              <table width="600" border="0" cellspacing="0" cellpadding="0" style="width:600px;" class="em_wrapper">
              <tr>
                <td align="center" valign="top">
                    <table width="600" border="0" cellspacing="0" cellpadding="0" align="center" style="width:600px;" class="em_wrapper">
                    <tr>
                      <td width="20" style="width:20px;"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" width="1" height="1" border="0" style="display:block;" /></td>
                      <td align="center" valign="top">
                          <table width="560" border="0" cellspacing="0" cellpadding="0" align="center" style="width:560px;" class="em_wrapper">
                          <tr>
                            <td height="65" style="height:65px;"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" width="1" height="1" border="0" style="display:block;" /></td>
                          </tr>
                          <tr>
                            <td align="center" class="em_gray_M" style="color:#535559;font-family:Arial, sans-serif;font-size:11px;line-height:17px;padding-bottom:25px;"><span style="font-weight:bold;">Email Recipients Include:</span>__email_recipients_include__</td>
                          </tr>
                        
                          <tr>
                            <td align="center" style="color:#535559;font-family:Arial, sans-serif;font-size:11px;line-height:17px;padding-bottom:12px;">
                                <span style="font-weight:bold;">Email Address: %%email address%%</span> 
                                &nbsp;|&nbsp; 
                                <a alias="Edit" href="https://account.churchofjesuschrist.org/email?cid=email-%%=v(@cid)=%%_Edit" target="_blank" style="color:#3A3D40;text-decoration:underline;">Edit</a>
                            </td>
                          </tr>
                          <tr>
                            <td align="center" valign="top" style="padding:0px 25px"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/5/ChurchSymbolGVSG-1120___three_digit_code__.png" width="100" alt="" border="0" style="display:block;max-width:100px" class="CToWUd"></td>
                          </tr>
                          <tr>
                            <td align="center" class="em_defaultlink" style="color:#535559;font-family:Arial, sans-serif;font-size:11px;line-height:17px;">&copy; 2021 by Intellectual Reserve, Inc. All rights reserved.</td>
                          </tr>
                          <tr>
                            <td align="center" class="em_gray_M" style="color:#535559;font-family:Arial, sans-serif;font-size:11px;line-height:17px;"><span class="em_gray1">50 E. North Temple St. Salt Lake City, Utah 84150</span><br />
                              <a alias="Terms" href="https://www.churchofjesuschrist.org/legal/terms-of-use?lang=__three_digit_code__&country=go&cid=email-%%=v(@cid)=%%_Terms" target="_blank" style="color:#535559;text-decoration:underline;">Terms of Use</a> (Updated 2021-04-13)<br />
                              <a alias="Privacy" href="https://www.churchofjesuschrist.org/legal/privacy-notice?lang=__three_digit_code__&country=go&cid=email-%%=v(@cid)=%%_Privacy" target="_blank" style="color:#535559;text-decoration:underline;">Privacy Notice</a> (Updated 2021-04-06)</td>
                          </tr>
                          <tr>
                            <td height="40" style="height:40px;" class="em_h20"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" width="1" height="1" border="0" style="display:block;" /></td>
                          </tr>
                        </table>
                        <img src="https://pixel.app.returnpath.net/pixel.gif?r=4cffc4daac7f9906b8e5f21e8766bff5e0bcda83&c=%%=v(@cid)=%%&s=%%LDSKey%%" width="1" height="1" />
                        <img src="https://pixel.inbox.exacttarget.com/pixel.gif?r=4cffc4daac7f9906b8e5f21e8766bff5e0bcda83&c=%%=v(@cid)=%%&s=%%email address%%" width="1" height="1" />
                        </td>
                      <td width="20" style="width:20px;"><img src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" width="1" height="1" border="0" style="display:block;" /></td>
                    </tr>
                  </table>
                  </td>
              </tr>
              <tr>
                <td class="em_hide" style="line-height:1px;min-width:600px;background-color:#eff0f0;"><img alt="" src="http://image.email.churchofjesuschrist.org/lib/fe8a1372756d06747d/m/2/spacer.gif" height="1"  width="600" style="max-height:1px; min-height:1px; display:block; width:600px; min-width:600px;" border="0" /></td>
              </tr>
            </table>
            </td>
        </tr>
        <!-- //Footer Section -->
      </table>
      </td>
  </tr>
</table>
</body>
</html>
"""


three_digit_code_list = ['alb','arm','bul','CAMBODIAN','ceb','zho','hrv','cze','dan','dut','est','fin','fra','ger','hun','ind','ita','jpn','kor','lav','lit','mon','nor','pol','por','rum','rus','smo','spa','swe','tgl','tha','tog','ukr','vie']
language_list = ['Albanian', 'Armenian', 'Bulgarian', 'Cambodian', 'Cebuano', 'Chinese', 'Croatian', 'Czech', 'Danish', 'Dutch', 'Estonian', 'Finnish', 'French', 'German', 'Hurgarian', 'Indonesian', 'Italian', 'Japanese', 'Korean', 'Latvian', 'Lithuanian', 'Mongolian', 'Norwegian', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Samoan', 'Spanish', 'Swedish', 'Tagalog', 'Thai', 'Tongan', 'Ukrainian', 'Vietnamese']

assert len(three_digit_code_list) == len(language_list)

# f_subject = open()


for fname in os.listdir(base_file_location):
    if fname.endswith(".docx"):
        subject = ""
        message = ""
        full_path = os.path.join(base_file_location,fname)
        # open connection to Word Document
        doc = docx.Document(full_path)
        fname_parts = fname.split()
        language = fname_parts[0]
        lang_not_found = True 
        for indx, lang in enumerate(language_list):
            if lang_not_found:
                if lang == language:
                    three_digit_code = three_digit_code_list[indx]
                    lang_not_found = False
                else:
                    continue
        if lang_not_found:
            three_digit_code = "eng"
        header = header_template.replace("__three_digit_code__", three_digit_code)
        footer = footer_template.replace("__three_digit_code__", three_digit_code)
        # read in each paragraph in file
        result = [p.text for p in doc.paragraphs]
        for par_indx in range(len(result)):
            if par_indx == 1:
                subject = result[par_indx]
            elif par_indx >= 3:
                message += insertParagraph(result[par_indx])
            else:
                pass
        f = open(os.path.join(base_file_location,language+"_email_test.html"), 'w', encoding="utf16")
        f.write(header + message + footer)
        f.close()


print(result)





# ftxt = ftxt.replace("__Title_Email__",emailTitle)
# ftxt = ftxt.replace("__paragraph_text__",message)
# ftxt = ftxt.replace("__Callings_Included__",callingsStr)

# f= open(destination, 'w')
# f.write(ftxt)
# f.close()