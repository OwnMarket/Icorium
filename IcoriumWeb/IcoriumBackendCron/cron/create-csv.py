import csv
import pymssql
import boto3

MSSQL_SERVER = 'icoriummasterdb.cqc4c8d1cdmf.us-west-2.rds.amazonaws.com'
MSSQL_USER = 'icouser'
MSSQL_PWD = 'D6zqZ6UXfd'
MSSQL_DB = 'Icorium'
AWS_BUCKET_NAME = 'exp.icorium.io'
ICO_MASTER = '/home/icorium/csv/IcoMasterJCsraQ5Km5.csv'
ICO_SOCIAL = '/home/icorium/csv/IcoSocialJCsraQ5Km5.csv'
ICO_MASTER_KEY = 'IcoMasterJCsraQ5Km5.csv'
ICO_SOCIAL_KEY = 'IcoSocialJCsraQ5Km5.csv'


conn = pymssql.connect(MSSQL_SERVER, MSSQL_USER, MSSQL_PWD, MSSQL_DB)        
cursor = conn.cursor()

cursor.execute("SELECT IcoID, IcoSymbol, CompanyName, CONCAT('http://images.icorium.io/full/', Logo) AS Logo, Category, YearofOrigin, CountryofOrigin, UnderlayingTechno, AcceptedCurrency, IcoPhase, IcoStart, IcoEnd, IcoScale, ScaleCurrency, IcoTotalExpected, TotalCurrency, IcoTotalRaised, RaisedCurrency, TokenDistribution, TokenSales, InvestmentPotential, HypeScore, RiskScore, OverallRating FROM IcoMaster  ORDER BY IcoID")
with open(ICO_MASTER, "w", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(cursor)

cursor.execute("SELECT IcoId, Type, Link FROM SocialLinks ORDER BY IcoId")
with open(ICO_SOCIAL, "w", newline='') as csv_file:
    csv_writer = csv.writer(csv_file) 
    csv_writer.writerows(cursor)

s3 = boto3.client('s3')

with open(ICO_MASTER, 'rb') as data:
    s3.upload_fileobj(data, AWS_BUCKET_NAME, ICO_MASTER_KEY)

with open(ICO_SOCIAL, 'rb') as data:
    s3.upload_fileobj(data, AWS_BUCKET_NAME, ICO_SOCIAL_KEY)
