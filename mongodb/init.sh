
mongoimport --db student_db --collection students --ignoreBlanks --type csv --file /docker-entrypoint-initdb.d/student_list.csv --drop --headerline