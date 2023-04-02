from sqlite3 import Cursor
from xmlrpc.client import Boolean
from django.shortcuts import render
import pyodbc
import pandas as pd
from . utilities import clean_fetched,filter,clean_detail_data,statistics
# Create your views here.

def stat(request, id):
    dep_set_id = int(id)
    conn =pyodbc.connect('Driver={sql server};'
        'Server=WIN-ESVIOLS6ROB;'
        'Database=reporting;'
        'Trusted_Connection=yes;')

    cursor = conn.cursor()

    cursor.execute("exec [reporting].[common].[sp_get_deployment_set_id_analysis] @deployment_set_id  = ?",(dep_set_id))
    failure_break = cursor.fetchall()

    cursor.cancel()
    # get the table data to get statistics from it
    query = "select * from [reporting].[common].[deployment_log] WHERE deployment_set_id = "+str(dep_set_id)+";"

    df = pd.read_sql(query, conn)
    # convert the table to pandas(python Library) dataframe

    ## Statistics data 
    stat_data = statistics(df)

    return render(request, "statistics.html",{'failure_break':failure_break,'stat_data':stat_data})

def detail(request, id):
    dep_id = int(id)
    conn =pyodbc.connect('Driver={sql server};'
        'Server=WIN-ESVIOLS6ROB;'
        'Database=reporting;'
        'Trusted_Connection=yes;')

    cursor = conn.cursor()

    
    #getting Columns names

    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'deployment_log'")
    col_names = cursor.fetchall()
    col_names = clean_fetched(col_names)

    #getting the row which equal to the passed deployment_id
    cursor.execute("SELECT  * FROM [reporting].[common].[deployment_log] WHERE [deployment_id] = ?",(dep_id))
    row = cursor.fetchall()
    row = clean_detail_data(row,col_names)


  
    return render(request, "detail_view.html",{'row':row,'col_names':col_names})

def home(request):
    
    # connecting to the database
    conn =pyodbc.connect('Driver={sql server};'
        'Server=WIN-ESVIOLS6ROB;'
        'Database=reporting;'
        'Trusted_Connection=yes;')

    cursor = conn.cursor()
    #getting the ids' from vwlast_deployment_sets view
    cursor.execute("SELECT  [deployment_set_id] FROM [reporting].[common].[vwlast_deployment_sets];")
    recent_deployment_set_id = cursor.fetchall()

    #cleaning the data to get functional format
    recent_deployment_set_id = clean_fetched(recent_deployment_set_id)



    if request.method == "POST":
        # get the data from the html

        
        is_failed = None
        dep_set_id = None
        sql_name = None

        try:
            dep_set_id = int(request.POST["dep_set_id"])
        except:
            print('no dep_set_id applied')
        try :
            is_failed  = bool(int(request.POST["is_failed"]))
        except:
            print('no check box applied')

        #getting Date from html and check if user provided date or not
        if request.POST["date"] == "":
            posted_date = request.POST["date"]
        else :
            posted_date = request.POST["date"]
            #convert date to pandas datetime format
            posted_date = pd.to_datetime(posted_date)
        print(posted_date)
        # getting Sql name if provided
        try:
            sql_name = request.POST["sql_name"]
        except:
            print('No SQL Name applied')

                
        # # get the table data to filter it
        # query = "select * from [reporting].[common].[deployment_log];"

        # # convert the table to pandas(python Library) dataframe
        # df = pd.read_sql(query,conn)
        # # convert the database date to pandas datetime 
        # df['deployment_date'] = pd.to_datetime(df['deployment_date'])

        filtered_df = filter(conn,dep_set_id,is_failed,posted_date)

        #check if user provided sql_name and apply another filter 
        if sql_name:
            print("sql_name","chosed")
            filtered_df = filtered_df[filtered_df['deployment_sql_instance']==sql_name]
        
   
        
        return render(request,'home.html',{'recent_deployment_set_id':recent_deployment_set_id,'filtered_df':filtered_df})

    return render(request,'home.html',{'recent_deployment_set_id':recent_deployment_set_id})