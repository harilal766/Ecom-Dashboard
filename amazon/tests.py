from django.test import TestCase
import pandas as pd

# Create your tests here.
class SPAPITesting(TestCase):
    pass
class SPAPIReportTest(SPAPITesting):
    def report_generator_test():
        pass
    
    def test_is_report_being_filtered(self,report,selected_columns):
        """
        make sure the filter columns is in the report df
        make sure selected columns are a sequence of list of tuple
        filter it and make sure the filtered column headers are same to filter_columns
        """
        report_df = pd.read_csv(report,delimiter='\t')
        filtered_df = report_df.filter(selected_columns)
        