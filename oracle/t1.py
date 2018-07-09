import cx_Oracle as oracle
import time

fo = open('stockName')
line = fo.readline().strip()
zz500 = line.split(',')
zz = []
for z in zz500:
    zz.append( "'"+z+"'")
s = ','.join(l for l in zz)
#print(zz)
fo.close()
print(len(zz500))
a = '20170102'
b = '20180427'
#s = "'000006.SZ','000012.SZ'"
day = time.strftime("%Y%m%d", time.localtime())
print(day)
fo = open('stock_data_price_qfq_n1.csv', 'w')
fo.write('STOCK,TRADE_DT,S_DQ_ADJOPEN,S_DQ_ADJHIGH,S_DQ_ADJLOW,S_DQ_ADJCLOSE\n')
conn = 'wind/wind@10.0.116.198:1521/wind'
db = oracle.connect(conn)
cursor=db.cursor()
#strsql = "select TRADE_DT, S_DQ_ADJOPEN, S_DQ_ADJHIGH, S_DQ_ADJLOW, S_DQ_ADJCLOSE from ASHAREEODPRICES where
#    S_INFO_WINDCODE = '%s' and TRADE_DT in  order by TRADE_DT "%(a, b, c) ;
strsql = "select S_INFO_WINDCODE, TRADE_DT, S_DQ_ADJOPEN, S_DQ_ADJHIGH, S_DQ_ADJLOW, S_DQ_ADJCLOSE from ASHAREEODPRICES where TRADE_DT >= '%s' and TRADE_DT <= '%s' and S_INFO_WINDCODE in (%s) order by S_INFO_WINDCODE, TRADE_DT" % (a,b,s) ;
print(strsql)
try:
    cursor.execute(strsql)
    row = cursor.fetchall()
    for rw in row:
        fo.write(','.join(str(l) for l in rw)+'\n')
    #print(row)
except Exception as err:
    print(err)
    print('hehe')
fo.close()
