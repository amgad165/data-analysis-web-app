import pandas as pd

def clean_detail_data(data,col_names):
    new_row = []
    for i in range(len(col_names)):
            new_row.append(data[0][i])
    return new_row

def clean_fetched(data):
    return [ object[0] for object in data ]


def select_top_data(df):
    df = df.sort_values(by='deployment_date',ascending=False)
    return df.iloc[:5000]

def filter(conn,dep_set_id,is_failed,date):

    #to pass them to  the query they have to be in string
    date_as_string = "'" +str(date)+ "'"
    is_failed_as_as_string = "'" +str(is_failed)+ "'"

    if dep_set_id == None and is_failed == None and date == '' :
        query = "select top (5000) *   from [reporting].[common].[deployment_log] order by deployment_date desc;"
        df = pd.read_sql(query, conn)

        return df

    elif dep_set_id == None and is_failed != None and date != '' :

        print("df[(df['is_failed']==is_failed) & (df['deployment_date']==date)]")

        query = "select top (5000) * from [reporting].[common].[deployment_log] WHERE deployment_date >= "+date_as_string+" and is_failed = "+is_failed_as_as_string+" order by deployment_date desc;"
        df = pd.read_sql(query, conn)

        return df
    
    elif dep_set_id == None and is_failed == None and date != '' :
        print("df[df['deployment_date']==date]")
        query = "select top (5000) *  from [reporting].[common].[deployment_log] WHERE deployment_date >= " + date_as_string + " order by deployment_date desc;"
        df = pd.read_sql(query, conn)

        return df
    
    elif dep_set_id == None and is_failed != None and date == '' :

        print("df[df['is_failed']==is_failed]")

        query = "select  top (5000) * from [reporting].[common].[deployment_log] WHERE is_failed = "+is_failed_as_as_string+" order by deployment_date desc;"
        df = pd.read_sql(query, conn)

        return select_top_data(df)
  

    elif is_failed != None and date != '':
        print('1')
        query = "select * from [reporting].[common].[deployment_log] WHERE deployment_set_id = "+str(dep_set_id)+";"
        df = pd.read_sql(query, conn)

        return select_top_data(df[(df['is_failed']==is_failed) & (df['deployment_date']>=date)])
    
    elif is_failed == None and date != '':
        print('2')
        query = "select * from [reporting].[common].[deployment_log] WHERE deployment_set_id = "+str(dep_set_id)+";"
        df = pd.read_sql(query, conn)
        
        return select_top_data(df[df['deployment_date']>=date])

    elif is_failed != None and date == '':
        print('3')
        query = "select * from [reporting].[common].[deployment_log] WHERE deployment_set_id = "+str(dep_set_id)+";"

        df = pd.read_sql(query, conn)
        return select_top_data(df[df['is_failed']==is_failed])
    
    
    else:
        print('4')

        query = "select * from [reporting].[common].[deployment_log] WHERE deployment_set_id = "+str(dep_set_id)+";"

        df = pd.read_sql(query, conn)

        return select_top_data(df)

def statistics(df):
    total_count = df['deployment_set_id'].count()
    total_success= df[df['is_failed']== 0 ].count().iloc[0]
    total_failed = df[df['is_failed']== 1 ].count().iloc[0]
    return [total_count,total_success,total_failed]



