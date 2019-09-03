#Testes

``` dos
curl -X POST -i -H "Content-Type: application/json" -d "{\"id\":1,\"firstName\":\"Luis\",\"lastName\":\"Gray\",\"email\":\"john.gray@example.com\",\"phone\":\"1203123\",\"birthDate\":\"1975-05-14\",\"title\":\"Developer Manager\",\"dept\":\"IT\"}" http://127.0.0.1:8080/employees
```

``` dos
curl -X DELETE -i http://127.0.0.1:8080/employees/1
```

``` dos
curl -X GET -i http://127.0.0.1:8080/employees
```