#!/bin/bash

./deployment.sh auth
./deployment.sh store
python ./tests/main.py --type all --with-authentication --authentication-address http://127.0.0.1:5000 --jwt-secret uuyfu56r67F65FUYFT78 --roles-field role --administrator-role admin --customer-role customer --warehouse-role worker --customer-address http://127.0.0.1:5001 --warehouse-address http://127.0.0.1:5002 --administrator-address http://127.0.0.1:5003
