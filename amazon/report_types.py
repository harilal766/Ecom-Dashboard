

spapi_report_types = {
    "Fulfilled Report" : "GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL",
    "Order Report" : "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
    "Return Report" : "GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE",
    "Settlement Report" : "GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE"
}


def type_menus(dictionary):
    menu_count = 0
    for choice in dictionary:
        print(f"{menu_count} : {choice}")

