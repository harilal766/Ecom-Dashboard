#$import psycopg2
import pandas as pd
import os
from .messages import better_error_handling,success_status_msg,color_text
from .file_ops import *
import calendar,time
from datetime import datetime
import  calendar 
import pg8000,sqlite3
from sqlalchemy import create_engine
import pandas as pd

def db_connection(dbname,db_system):
    function_boundary(title="DB CONNECTION")
    try:
        if db_system == "postgres":
            connection = pg8000.connect(
                user='postgres',
                password='1234',
                host='localhost',      
                port=5432,            
                database=dbname
                )
        elif db_system == "sqlite":
            connection = sqlite3.connect(f"{dbname}.db")

        if connection:
            success_status_msg(f"Connected to the databse : {dbname}.")
            return connection
        else:
            better_error_handling(f"Connection failed to the database : {dbname}.")
            
    except Exception as e:
        better_error_handling(e)
    
def query_backup(filename,query):
    try:
        with open(f"{filename}.sql",'w') as query_backup:
            query_backup.write(query)
    except Exception as e:
        better_error_handling(e)
    finally:
        success_status_msg("Query Backed Up.")

def line_limit_checker(word_count,line_limit):
    if word_count % line_limit == 0:
        return True
    return False
    
def sql_to_excel(sql_cursor,query_result,out_excel_path,excel_filename=None):
    try: 
        #  PSEUDOCODE
        # replace underscore with space
        # convert to excel only if excel file name is not none
        success_status_msg("Excel conversion Started.")
        # excel conversion
        # replacing underscores with empty spaces in columns
        column_list = [desc[0].replace("_"," ") for desc in sql_cursor.description]
        if column_list:
            color_text(message="_ replaced with empty space")
        excel_sheet = pd.DataFrame(query_result,columns=column_list)
        # if the excel file already exists, a sheet should be created inside the file and the output should be stored there.
        if excel_filename == None:
            excel_filename = file_input_checker(display_message="Enter the filename.")
        if excel_filename:
            # re initialization of the file path after getting the filename
            out_directory = out_excel_path
            out_excel_path = os.path.join(out_directory,excel_filename+".xlsx")
            excel_sheet.to_excel(out_excel_path,index="False",engine='openpyxl')
            if excel_filename in os.listdir(out_directory):
                success_status_msg(f"Excel output file : {out_directory} created.")
        else:
            print("Please enter the filename..")
    except Exception as e:
        better_error_handling(e)

def db_closer(connection,cursor):
    try:
        if connection and cursor:
            # closing the db
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and connection:
                connection.close()
            color_text(message="Connection closed.",color='green')
        else:
            color_text(message="Error with db closilng",color="red")
    except Exception as e:
        better_error_handling(e)

def query_execution(dbname,db_system,tablename,filter_rows):
    try:
        fields = """amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax"""

        order_by_clause="amazon_order_id asc, product_name asc, quantity asc"
        query = f"""SELECT {fields}
        FROM {tablename} 
        WHERE 
            amazon_order_id in {tuple(filter_rows)} 
        ORDER BY {order_by_clause};"""
        print(query)
        # connecting to the db
        connection = db_connection(dbname=dbname,db_system=db_system)
        if connection:
            success_status_msg("Connection Succeeded.")
            cursor = connection.cursor()
            cursor = cursor.execute(query)
            # converting the sql result into excel file
            return {"connection":connection,"cursor":cursor}
# Error Areas -----------------------------------------------------------------------------------
        else:
            color_text(message="Connection Failed",color="red")
    except Exception as e:
        better_error_handling(e)

def sql_table_CR(dbname,tablename,replace_or_append,input_file_dir,filename=None):
    try:
        connection = db_connection(dbname=dbname,db_system="sqlite")
        if filename != None:
            filename = file_input_checker(display_message="Enter the input filename with extension :- ",filepath=input_file_dir)
        extension = str(filename.split(".")[-1]).lower()
        df = ""
        filepath = os.path.join(input_file_dir,filename)
        
        if extension == "xlsx":
            sheet_name = input("Enter the name of the sheet : ")
            df = pd.read_excel(filepath, sheet_name=sheet_name)
        elif extension == "txt":
            df = pd.read_csv(filepath,delimiter='\t',on_bad_lines='skip')
        elif extension == "csv":
            df = pd.read_csv(filepath,delimiter=',',on_bad_lines='skip')
        elif extension == "tsv":
            df = pd.read_csv(filepath,sep='\t')
        else:
            print("UNSUPPORTED EXTENSION")
        
        # replacing " " with "-"
        df.columns = df.columns.str.replace(' ', '_').str.replace("-","_")
        
        engine = create_engine(f'sqlite:///{dbname}.db')
        df.to_sql(tablename,con=engine, if_exists=str(replace_or_append), index=False)
    except FileNotFoundError:
        color_text(message=f"{filename} not found, if the name is correct, please check the spaces....",color='red')
    except Exception as e:
        better_error_handling(e)
    finally:
        connection.close()
        color_text(message="Connection closed.",color="green")