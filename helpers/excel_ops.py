import pandas as pd

from helpers.messages import *

def excel_appending(dataframes,out_path):
    try:
        if isinstance(dataframes,list):
            # append the dataframes
            for dataframe in dataframes:
                space = 0
                print(dataframe)
                with pd.ExcelWriter(out_path,engine='openpyxl') as writer:
                    dataframe.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=space,index=False)
                    space += len(dataframe)+2

            # save the output 
        else:
            color_text(message="The dataframes are not specified in list format",color="red")
    except Exception as e:
        better_error_handling(e)
        

def shipment_report_pivot_table(df,grouping_column,pivot_columns):
    try:
        if not df.empty:
            pivot = pd.pivot_table(data=df,index=grouping_column,
                                values= pivot_columns,aggfunc="sum")
            """
                Select the column you want to group : Product name
                Selct the operation you want on the pivot table : sum
                select the 
            """
        
            # SORTING the pivot table 
            pivot = pivot[pivot_columns] # column sorting

            # Creating the sum row and adding to the pivot
            sum_row = pivot.sum(axis=0).to_frame().T
            sum_row.index = ["Total"]
            pivot = pd.concat(objs=[pivot,sum_row])

            # Final out
            pivot.to_excel(excel_writer=r"D:\Ecom-Dashboard\Test documents\pivot\pivot.xlsx")
            color_text(message=pivot)
            
        else:
            color_text(message="The excel file is empty",color="red")

    except Exception as e:
        better_error_handling(e)

def excel_styling():
    pass

