import pandas as pd

def sp_getserverlist(conn,region,status,ait,sql_version,group):
    region = "'" +str(region)+ "'"
    status = "'" +str(status)+ "'"  
    ait = "'" +str(ait)+ "'"    
    sql_version = "'" +str(sql_version)+ "'"
    group = "'" +str(group)+ "'"
    empty = str("\' \'")
    print("empty = ",empty)


    cursor = conn.cursor()
   
    cursor.execute("set nocount on; exec [reporting].[common].[sp_getserverlist] @server_name = '' , @region = "+region+", @server_status ="+status+",@ait ="+ait+",  @group = "+group+", @sql_version = "+sql_version+";")
    
    df2 = cursor.fetchall()
    return df2


def clean_detail_data(data,col_names):
    new_row = []
    for i in range(len(col_names)):
            new_row.append(data[0][i])
    return new_row

def clean_fetched(data):
    return [ object[0] for object in data ]


def select_top_data(df):
    df = df.sort_values(by='deployment_date',ascending=False)
    return df.iloc[:100]

def filter(df,dep_set_id,is_failed,date):

    if dep_set_id == None and is_failed == None and date == '' :
        return select_top_data(df)

    elif dep_set_id == None and is_failed != None and date != '' :

        print("df[(df['is_failed']==is_failed) & (df['deployment_date']==date)]")
        return select_top_data(df[(df['is_failed']==is_failed) & (df['deployment_date']>=date)])
    
    elif dep_set_id == None and is_failed == None and date != '' :
        print("df[df['deployment_date']==date]")
        return select_top_data(df[df['deployment_date']>=date])
    
    elif dep_set_id == None and is_failed != None and date == '' :
        print("df[df['is_failed']==is_failed]")
        return select_top_data(df[df['is_failed']==is_failed])
  

    elif is_failed != None and date != '':
        print('1')
        return select_top_data(df[(df['deployment_set_id']==dep_set_id) & (df['is_failed']==is_failed) & (df['deployment_date']>=date)])
    
    elif is_failed == None and date != '':
        print('2')
        return select_top_data(df[(df['deployment_set_id']==dep_set_id)  & (df['deployment_date']>=date)])
    elif is_failed != None and date == '':
        print('3')
        return select_top_data(df[(df['deployment_set_id']==dep_set_id)  & (df['is_failed']==is_failed)])
    
    
    else:
        print('4')
        return select_top_data(df[df['deployment_set_id']==dep_set_id])

def statistics(df,dep_set_id):
    if dep_set_id == None:
        return None

    else:
        total_count = df[df['deployment_set_id']==dep_set_id].count().iloc[0]
        total_success= df[(df['deployment_set_id']==dep_set_id) & (df['is_failed']== 0) ].count().iloc[0]
        total_failed = df[(df['deployment_set_id']==dep_set_id) & (df['is_failed']== 1) ].count().iloc[0]
        return [total_count,total_success,total_failed]



