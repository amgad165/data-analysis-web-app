from ntpath import join
from django.shortcuts import render
import pyodbc
import pandas as pd
from . utilities import clean_fetched,filter,clean_detail_data,statistics,sp_getserverlist
# Create your views here.

def home(request):

    
    # connecting to the database
    conn =pyodbc.connect('Driver={sql server};'
        'Server=WIN-ESVIOLS6ROB;'
        'Database=reporting;'
        'Trusted_Connection=yes;')
    
  
    
    if request.method == "POST":
        sql_version = request.POST.get('sqlversion','')
        # getting rid from the last comma
        print("before",sql_version)
        sql_version = sql_version[:-1]
        print("after",sql_version)

        region = request.POST.get('region','')
        
        if request.POST.getlist('status'):
            status = request.POST.getlist('status','')
            status = ','.join(status)
        else :
            status = ''
        
        
        ait = request.POST.get('ait','')
        group = request.POST.get('group','')
        group = group[:-1]

        cursor = conn.cursor()

        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'tbl_server_list'")
        col_names = cursor.fetchall()
        col_names = clean_fetched(col_names)
        col_names = list(col_names)
        
        cursor.execute("SELECT  [status_name] FROM [reporting].[common].[vm_status]")
     
        status_names = cursor.fetchall()

        cursor.execute("SELECT [region_name] FROM [reporting].[common].[vw_region]")
        
        regions = cursor.fetchall()

        cursor.execute("SELECT DISTINCT [sql_version] FROM [reporting].[common].[tbl_server_list]")
        
        sql_versions = cursor.fetchall()

        

        cursor.execute("SELECT DISTINCT [support_group] FROM [reporting].[common].[tbl_server_list]")
        
        groups = cursor.fetchall()



        #applying the stored procedures with the posted data
        df = sp_getserverlist(conn,region,status,ait,sql_version,group)
        context = {'df':df,'col_names':col_names,'status_names':status_names,'regions':regions,"sql_versions":sql_versions,"groups":groups}
        return render(request,'home.html',context)

        
    
   
    cursor = conn.cursor()

    cursor.execute("SELECT  [status_name] FROM [reporting].[common].[vm_status]")
     
    status_names = cursor.fetchall()

    cursor.execute("SELECT [region_name] FROM [reporting].[common].[vw_region]")
     
    regions = cursor.fetchall()

    cursor.execute("SELECT DISTINCT [sql_version] FROM [reporting].[common].[tbl_server_list]")
     
    sql_versions = cursor.fetchall()

      

    cursor.execute("SELECT DISTINCT [support_group] FROM [reporting].[common].[tbl_server_list]")
     
    groups = cursor.fetchall()


    
    unwanted_filters_index = [1,2,7,8]

    context = {'unwanted_filters_index':unwanted_filters_index,'status_names':status_names,'regions':regions,"sql_versions":sql_versions,"groups":groups}

    
    
  
    return render(request,'home.html',context)

