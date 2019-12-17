#Testes

## Insert
``` dos
curl -X POST -i -H "Content-Type: application/json" -d "{\"id\":1,\"firstName\":\"Luis\",\"lastName\":\"Gray\",\"email\":\"john.gray@example.com\",\"phone\":\"1203123\",\"birthDate\":\"1975-05-14\",\"title\":\"Developer Manager\",\"dept\":\"IT\"}" http://127.0.0.1:8080/employees
```

## Delete
``` dos
curl -X DELETE -i http://127.0.0.1:8080/employees/1
```

## List
``` dos
curl -X GET -i http://127.0.0.1:8080/employees
```

## JDE 
``` dos
python "exemplo api.py"

curl -u giovani_mesquita:5s253m8UV$ -X GET -i http://127.0.0.1:8080/cic/99988488068
curl -u giovani_mesquita:5s253m8UV$ -X GET -i http://127.0.0.1:8080/cic/62256092020
curl -u giovani_mesquita:5s253m8UV$ -X GET -i http://127.0.0.1:8080/cic/82951328000158
curl -u giovani_mesquita:5s253m8UV$ -X GET -i http://127.0.0.1:8080/cic/27704912020
curl -u giovani_mesquita:5s253m8UV$ -X GET -i http://127.0.0.1:8080/oc/00610/2819/OM
```

``` dos
curl -u miguel:python -i http://localhost:5000/todo/api/v1.0/tasks
```