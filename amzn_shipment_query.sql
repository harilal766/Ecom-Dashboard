
            SELECT DISTINCT
            amazon_order_id, purchase_date, last_updated_date, order_status, product_name,item_status, quantity, item_price, item_tax, shipping_price, shipping_tax 
            FROM Orders 
            WHERE amazon_order_id IN (
                	'404-6411994-7187539','403-1987618-0004345','405-0403666-8806766',
'406-8746685-8793949','171-5398275-0929901','407-5321697-9503511',
'403-3821936-5823552','408-3292509-1429132','171-2115168-9433959',
'408-9852933-7557931','171-0797127-5144300','408-9685509-5233142',
'171-9330049-8758707','404-7775473-6553953','403-8579082-7514758',
'405-1597226-9461900','405-5937402-0520333','171-4378195-4527568',
'405-7847944-4349945','402-4431666-4938716','171-0992849-8383529',
'408-3191750-2089966','402-9698775-1860301','402-9241472-2546746',
'405-5901769-2583538','402-1288412-1552301','171-5283221-3543563',
'171-3294913-4630748','403-0677741-7514757','407-5804416-8208366',
'402-3421391-4077121','407-6296569-1783516','408-4203956-7552368',
'402-3394322-1045151','408-4110070-8085936','405-1580223-8201151',
'402-4462188-3018749','171-0768807-8536303','403-7043736-5045951',
'171-9908429-4370705','404-5168830-5909967','403-4566701-5378722',
'402-1794188-6604363','404-3962824-2696312','403-6677856-9284316',
'171-4066264-4870720','407-3673114-7733960','408-6783325-8217900'
            )
            ORDER BY product_name asc,quantity asc;
        