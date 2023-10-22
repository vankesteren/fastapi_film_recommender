set DBNAME=webshop
set PGPASSWORD=postgres
set PGCLIENTENCODING=UTF8

echo "Restoring data to database %DBNAME%"

dropdb -U postgres %DBNAME%
createdb -U postgres %DBNAME%
psql -h localhost -p 5432 -U postgres -d %DBNAME% -f PostgreSQLSampleDatabase\data\create.sql
psql -h localhost -p 5432 -U postgres -d %DBNAME% -f PostgreSQLSampleDatabase\data\address.sql
psql -h localhost -p 5432 -U postgres -d %DBNAME% -f PostgreSQLSampleDatabase\data\articles.sql
psql -h localhost -p 5432 -U postgres -d %DBNAME% -f PostgreSQLSampleDatabase\data\customer.sql
psql -h localhost -p 5432 -U postgres -d %DBNAME% -f PostgreSQLSampleDatabase\data\labels.sql
psql -h localhost -p 5432 -U postgres -d %DBNAME% -f PostgreSQLSampleDatabase\data\order_positions.sql
psql -h localhost -p 5432 -U postgres -d %DBNAME% -f PostgreSQLSampleDatabase\data\order.sql
psql -h localhost -p 5432 -U postgres -d %DBNAME% -f PostgreSQLSampleDatabase\data\products.sql
psql -h localhost -p 5432 -U postgres -d %DBNAME% -f PostgreSQLSampleDatabase\data\stock.sql