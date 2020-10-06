import pandas as pd
import datacompy

base_file_location = "N:/ReportingAnalysis/Workforce/CSReporting/UAT/"

def exportDFDiffs(key,value):
    diffs = compare.intersect_rows[[key.lower(), value.lower() + '_df1'
                                      , value.lower() + '_df2'
                                      , value.lower() +'_match']]
    diffs = diffs[diffs[value.lower() +'_match'] == False].copy()
    return diffs

df1 = pd.read_excel(base_file_location +  "October 2019/October 2019_SN.xlsx" )
df2 = pd.read_excel(base_file_location +  "October 2019/October 2019_BO.xlsx" )

#make sure column names are the same
df2.columns = ['Number', 'Created', 'Originating group', 'Created by','Assignment group', 'Contact type',
       'Closed by', 'KB Number', 'KB Title [Main Ticket]', 'State', 'CDOL Unit number']

df1['Closed by'] = df1['Closed by'].str.lower()
df1['Created by'] = df1['Created by'].str.lower()

compare = datacompy.Compare(
    df1,
    df2,
    join_columns='Number',  #You can also specify a list of columns
    abs_tol=0, #Optional, defaults to 0
    rel_tol=0, #Optional, defaults to 0
    df1_name='SN', #Optional, defaults to 'df1'
    df2_name='BO' #Optional, defaults to 'df2'
    )
compare.matches(ignore_extra_columns=True)

# This method prints out a human-readable report summarizing and sampling differences
print(compare.report())

with open(base_file_location+ 'SN_BO_October_comparisonReport.txt', 'w') as file_object:
    file_object.write(compare.report())

print(compare.intersect_rows[['number','kb title [main ticket]_df1', 'kb title [main ticket]_df2', 'kb title [main ticket]_match']])

kbTitleMainTicketDiffs = exportDFDiffs('number','kb title [main ticket]')
kbTitleMainTicketDiffs.set_index('number',inplace=True)
kbNumberDiffs = exportDFDiffs('number','kb number')
kbNumberDiffs.set_index('number',inplace=True)
originGroupDiffs = exportDFDiffs('number','originating group')
originGroupDiffs.set_index('number',inplace=True)

conglob = pd.concat([kbTitleMainTicketDiffs,kbNumberDiffs,originGroupDiffs],axis=1,sort=False)
conglob.to_excel(base_file_location + 'SN_BO_October_Comparison.xlsx')


##################################
#
##################################

df1 = pd.read_csv(base_file_location +  "Ticket Segment.csv" )
df2 = pd.read_csv(base_file_location +  "Ticket Event.csv" )

df1.columns = ['Event Id', 'Channel Name', 'Current State', 'Full Subject',
       'Last Kb Attached Title', 'Created Date Time']

df2.columns = ['Event Id', 'Channel Name', 'Created Date Time',
       'Current Assignment Group', 'Current State', 'Full Subject',
       'Last Kb # Attached', 'Last Kb Attached Title']

compare = datacompy.Compare(
    df1,
    df2,
    join_columns='Event Id',  #You can also specify a list of columns
    abs_tol=0, #Optional, defaults to 0
    rel_tol=0, #Optional, defaults to 0
    df1_name='Segments', #Optional, defaults to 'df1'
    df2_name='Events' #Optional, defaults to 'df2'
    )
compare.matches(ignore_extra_columns=True)

# This method prints out a human-readable report summarizing and sampling differences
print(compare.report())


with open(base_file_location+ 'TicketSeg_TicketEvent_October_comparisonReport.txt', 'w') as file_object:
    file_object.write(compare.report())


##################################
#
##################################




df1 = pd.read_excel(base_file_location +  "October 2019/October 2019_SN.xlsx" )
df2 = pd.read_csv(base_file_location +  "Ticket Event.csv" )

df1.columns = ['Number', 'Created', 'Originating group', 'Created by',
       'Assignment group', 'Contact type', 'Closed by', 'KB Number',
       'Last Kb Attached Title', 'State', 'Tier', 'CDOL Unit number']

df2.columns = ['Number', 'Contact type', 'Created',
       'Assignment group', 'State', 'Full Subject',
       'KB Number', 'Last Kb Attached Title']

compare = datacompy.Compare(
    df1,
    df2,
    join_columns='Number',  #You can also specify a list of columns
    abs_tol=0, #Optional, defaults to 0
    rel_tol=0, #Optional, defaults to 0
    df1_name='SN', #Optional, defaults to 'df1'
    df2_name='Events' #Optional, defaults to 'df2'
    )
compare.matches(ignore_extra_columns=True)

# This method prints out a human-readable report summarizing and sampling differences
print(compare.report())


assignmentGroupDiffs = exportDFDiffs('number','assignment group')
kbNumberDiffs = exportDFDiffs('number','kb number')
lastKbTitleDiffs = exportDFDiffs('number','last kb attached title')

assignmentGroupDiffs.set_index('number',inplace=True)
kbNumberDiffs.set_index('number',inplace=True)
lastKbTitleDiffs.set_index('number',inplace=True)

conglob = pd.concat([assignmentGroupDiffs,kbNumberDiffs,lastKbTitleDiffs],axis=1,sort=False)
conglob.to_excel(base_file_location + 'SN_vs_Tableau_Comparison.xlsx')

with open(base_file_location+ 'SN_vs_Tableau_comparisonReport.txt', 'w') as file_object:
    file_object.write(compare.report())






df1 = pd.read_csv(base_file_location +  "October 2019/September2019_SN.csv" ,encoding='latin1')
df2 = pd.read_excel(base_file_location +  "October 2019/September2019_BO.xlsx" )

# df1
# ['number', 'sys_created_on', 'sys_updated_on', 'u_originating_group',
#        'assigned_to.user_name', 'assignment_group', 'contact_type',
#        'closed_by.user_name', 'KB Number',
#        'ref_x_tcoj2_gsc_main_ticket.u_kb_short_description', 'state', 'u_tier',
#        'requested_by.u_cdol_unit_number', 'Subject']

# df2
# ['Ticket Event Number', 'Created Date & Time', 'Originating Group Name',
#        'First Touched By Employee.LDS Account User Name',
#        'Assignment Group Name', 'Channel Name', 'Source State Name',
#        'First Resolved By Employee.LDS Account User Name', 'KB Number',
#        'Title', 'Unit Number', 'Full Subject']

df1.columns = ['number', 'sys_created_on', 'sys_updated_on', 'u_originating_group',
       'assigned_to.user_name', 'assignment_group', 'contact_type',
       'closed_by.user_name', 'KB Number',
       'ref_x_tcoj2_gsc_main_ticket.u_kb_short_description', 'state', 'u_tier',
       'requested_by.u_cdol_unit_number', 'Full Subject']


df2.columns = ['number', 'sys_created_on', 'u_originating_group',
       'assigned_to.user_name',
       'assignment_group', 'contact_type', 'state',
       'closed_by.user_name', 'KB Number',
       'ref_x_tcoj2_gsc_main_ticket.u_kb_short_description', 'requested_by.u_cdol_unit_number', 'Full Subject']


df2['closed_by.user_name'] = df2['closed_by.user_name'].str.lower()
df1['closed_by.user_name'] = df1['closed_by.user_name'].str.lower()

df1['requested_by.u_cdol_unit_number'] = df1['requested_by.u_cdol_unit_number'].fillna(0)
df1['requested_by.u_cdol_unit_number'] = df1['requested_by.u_cdol_unit_number'].astype('int')
df2['requested_by.u_cdol_unit_number'] = df2['requested_by.u_cdol_unit_number'].astype('int')

df2['Full Subject'] = df2['Full Subject'].replace('[\[\]]','',regex=True)
df2['Full Subject'] = df2['Full Subject'].replace('\.',' > ',regex=True)

compare = datacompy.Compare(
    df1,
    df2,
    join_columns='Number',  #You can also specify a list of columns
    abs_tol=0, #Optional, defaults to 0
    rel_tol=0, #Optional, defaults to 0
    df1_name='SN', #Optional, defaults to 'df1'
    df2_name='BO' #Optional, defaults to 'df2'
    )
compare.matches(ignore_extra_columns=True)

print(compare.report())

key = 'number'
listDfs = []
ignoreColList = [key,'requested_by.u_cdol_unit_number']
for col1 in df1.columns:
    if col1 not in ignoreColList:
        if col1 in list(df2.columns):
            dfDiffs = exportDFDiffs(key,col1)
            dfDiffs.set_index(key,inplace=True)
            listDfs.append(dfDiffs)

conglob = pd.concat(listDfs,axis=1,sort=False)
conglob.to_excel(base_file_location + 'September2019_SN_BO_Comparison.xlsx')

with open(base_file_location+ 'September2019_SN_BO_comparisonReport.txt', 'w',encoding='latin-1') as file_object:
    file_object.write(compare.report())






















df1 = pd.read_csv(base_file_location +  "October 2019/September2019_SN.csv" ,encoding='latin1')
df2 = pd.read_csv(base_file_location +  "Ticket Event - Sept.csv" )

df1.columns = ['number', 'sys_created_on', 'sys_updated_on', 'u_originating_group',
       'assigned_to.user_name', 'Current Assignment Group', 'contact_type',
       'closed_by.user_name', 'KB Number',
       'ref_x_tcoj2_gsc_main_ticket.u_kb_short_description', 'state', 'u_tier',
       'requested_by.u_cdol_unit_number', 'Subject']

df2.columns = ['contact_type', 'sys_created_on', 'Current Assignment Group',
       'state', 'Subject', 'KB Number',
       'number']

df2['Subject'] = df2['Subject'].replace('[\[\]]','',regex=True)
df2['Subject'] = df2['Subject'].replace('\.',' > ',regex=True)

compare = datacompy.Compare(
    df1,
    df2,
    join_columns='number',  #You can also specify a list of columns
    abs_tol=0, #Optional, defaults to 0
    rel_tol=0, #Optional, defaults to 0
    df1_name='SN', #Optional, defaults to 'df1'
    df2_name='Tableau' #Optional, defaults to 'df2'
    )
compare.matches(ignore_extra_columns=True)

print(compare.report())

key = 'number'
listDfs = []
ignoreColList = [key,'contact_type','sys_created_on']
for col1 in df1.columns:
    if col1 not in ignoreColList:
        if col1 in list(df2.columns):
            dfDiffs = exportDFDiffs(key,col1)
            dfDiffs.set_index(key,inplace=True)
            listDfs.append(dfDiffs)

conglob = pd.concat(listDfs,axis=1,sort=False)
conglob.to_excel(base_file_location + 'September2019_SN_Tableau.xlsx')

with open(base_file_location+ 'September2019_SN_Tableau_comparisonReport.txt', 'w',encoding='latin-1') as file_object:
    file_object.write(compare.report())








df1 = pd.read_csv(base_file_location +  "October 2019/August2019_SN.csv" ,encoding='latin1')
df2 = pd.read_csv(base_file_location +  "Ticket Event - Aug.csv" )

df1.columns = ['number', 'sys_created_on', 'u_originating_group',
       'assigned_to.user_name', 'Current Assignment Group', 'contact_type',
       'closed_by.user_name', 'KB Number',
       'ref_x_tcoj2_gsc_main_ticket.u_kb_short_description', 'state', 'u_tier',
       'requested_by.u_cdol_unit_number', 'Subject']

df2.columns = ['contact_type', 'sys_created_on', 'Current Assignment Group',
       'state', 'Subject', 'KB Number',
       'number']

df2['Subject'] = df2['Subject'].replace('[\[\]]','',regex=True)
df2['Subject'] = df2['Subject'].replace('\.',' > ',regex=True)

compare = datacompy.Compare(
    df1,
    df2,
    join_columns='number',  #You can also specify a list of columns
    abs_tol=0, #Optional, defaults to 0
    rel_tol=0, #Optional, defaults to 0
    df1_name='SN', #Optional, defaults to 'df1'
    df2_name='Tableau' #Optional, defaults to 'df2'
    )
compare.matches(ignore_extra_columns=True)

print(compare.report())

key = 'number'
listDfs = []
ignoreColList = [key,'contact_type','sys_created_on','state','contact_type']
for col1 in df1.columns:
    if col1 not in ignoreColList:
        if col1 in list(df2.columns):
            dfDiffs = exportDFDiffs(key,col1)
            dfDiffs.set_index(key,inplace=True)
            listDfs.append(dfDiffs)

conglob = pd.concat(listDfs,axis=1,sort=False)
conglob.to_excel(base_file_location + 'August2019_SN_Tableau.xlsx')

with open(base_file_location+ 'August2019_SN_Tableau_comparisonReport.txt', 'w',encoding='latin-1') as file_object:
    file_object.write(compare.report())


# df1 = pd.read_csv(base_file_location +  "October 2019/July2019_SN.csv" ,encoding='latin1')
# df2 = pd.read_csv(base_file_location +  "Ticket Event - July.csv" )

# df1.columns = ['number', 'sys_created_on', 'u_originating_group',
#        'assigned_to.user_name', 'Current Assignment Group', 'contact_type',
#        'closed_by.user_name', 'KB Number',
#        'ref_x_tcoj2_gsc_main_ticket.u_kb_short_description', 'state', 'u_tier',
#        'requested_by.u_cdol_unit_number', 'Subject']

# df2.columns = ['contact_type', 'sys_created_on', 'Current Assignment Group',
#        'state', 'Subject', 'KB Number',
#        'number']

# df2['Subject'] = df2['Subject'].replace('[\[\]]','',regex=True)
# df2['Subject'] = df2['Subject'].replace('\.',' > ',regex=True)

# compare = datacompy.Compare(
#     df1,
#     df2,
#     join_columns='number',  #You can also specify a list of columns
#     abs_tol=0, #Optional, defaults to 0
#     rel_tol=0, #Optional, defaults to 0
#     df1_name='SN', #Optional, defaults to 'df1'
#     df2_name='Tableau' #Optional, defaults to 'df2'
#     )
# compare.matches(ignore_extra_columns=True)

# print(compare.report())

# key = 'number'
# listDfs = []
# ignoreColList = [key,'contact_type','sys_created_on','state','contact_type']
# for col1 in df1.columns:
#     if col1 not in ignoreColList:
#         if col1 in list(df2.columns):
#             dfDiffs = exportDFDiffs(key,col1)
#             dfDiffs.set_index(key,inplace=True)
#             listDfs.append(dfDiffs)

# conglob = pd.concat(listDfs,axis=1,sort=False)
# conglob.to_excel(base_file_location + 'August2019_SN_Tableau.xlsx')

# with open(base_file_location+ 'August2019_SN_Tableau_comparisonReport.txt', 'w',encoding='latin-1') as file_object:
#     file_object.write(compare.report())





















