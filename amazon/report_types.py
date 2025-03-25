

selected_report_types = {
    #"Shipment Report" : "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
    "Shipment Report" : "GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL",
    "Return Report" : "GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE",
    "Settlement Report" : ""
}


def type_menus(dictionary):
    menu_count = 0
    for choice in dictionary:
        print(f"{menu_count} : {choice}")

