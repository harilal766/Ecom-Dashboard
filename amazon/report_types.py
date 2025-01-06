

selected_types = {
    "Shipment Report" : "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
    "Return Report" : "GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE",
    "Settlement Report" : ""
}


order_report_types = {
    "actionable shipping flatfile" : "GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_SHIPPING",
    "invoicing" : "GET_ORDER_REPORT_DATA_INVOICING",
    "tax data" : "GET_ORDER_REPORT_DATA_TAX",
    "shipping report" : "GET_ORDER_REPORT_DATA_SHIPPING",
    "invoicing flatfile" : "GET_FLAT_FILE_ORDER_REPORT_DATA_INVOICING",
    "shipping flatfile" : "GET_FLAT_FILE_ORDER_REPORT_DATA_SHIPPING",
    "" : "GET_FLAT_FILE_ORDER_REPORT_DATA_TAX",
    "" : "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL",
    "datewise orders data flatfile" : "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
    "datewise archived orders data flatfile" : "GET_FLAT_FILE_ARCHIVED_ORDERS_DATA_BY_ORDER_DATE",
    "" : "GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL",
    "datewise order data xml" : "GET_XML_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
    "pending orders flatfile" : "GET_FLAT_FILE_PENDING_ORDERS_DATA",
    "pending orders" : "GET_PENDING_ORDERS_DATA",
    "" : "GET_CONVERGED_FLAT_FILE_PENDING_ORDERS_DATA",
}


return_report_types = {
   "datewise returns xml" : "GET_XML_RETURNS_DATA_BY_RETURN_DATE",
   "datewise returns flatfile" : "GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE",
   "prime returns xml" : "GET_XML_MFN_PRIME_RETURNS_REPORT",
   "prime returns csv" : "GET_CSV_MFN_PRIME_RETURNS_REPORT",
   "" : "GET_XML_MFN_SKU_RETURN_ATTRIBUTES_REPORT",
   "" : "GET_FLAT_FILE_MFN_SKU_RETURN_ATTRIBUTES_REPORT"
}
 

def type_menus(dictionary):
    menu_count = 0
    for choice in dictionary:
        print(f"{menu_count} : {choice}")

