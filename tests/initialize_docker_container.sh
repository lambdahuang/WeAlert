echo "Initialize docker database..."
docker run --name wealert_database -p 33433:3306 -e MYSQL_ROOT_PASSWORD=TEMPASSWORD -d mysql:5.7
echo "Database is initialized."
