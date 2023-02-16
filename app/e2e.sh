#!/bin/bash

# Test the home page
home=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/)
if [ $home -ne 200 ]; then
  echo "Error: home page returned HTTP status code $home"
  exit 1
fi

# Test the party page
party=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/party_1)
if [ $party -ne 200 ]; then
  echo "Error: party page returned HTTP status code $party"
  exit 1
fi

# Test the vote route with valid ID and party name
vote=$(curl -s -o /dev/null -w "%{http_code}" -d "id=964501563&party_name=מרצ" -X POST http://127.0.0.1:5000/vote)
if [ $vote -ne 200 ]; then
  echo "Error: vote route returned HTTP status code $vote"
  exit 1
fi


# Test the login page
login=$(curl -s -o /dev/null -w "%{http_code}" -d "username=admin&password=admin" -X POST http://127.0.0.1:5000/login)
if [ $login -ne 200 ]; then
  echo "Error: login page returned HTTP status code $login"
  exit 1
fi

# Test the add party route
add_party=$(curl -s -o /dev/null -w "%{http_code}" -d "party_name=TestParty&party_platform=TestPlatform" -X POST http://127.0.0.1:5000/add-party)
if [ $add_party -ne 200 ]; then
  echo "Error: add party route returned HTTP status code $add_party"
  exit 1
fi

# Test the delete party route
delete_party=$(curl -s -o /dev/null -w "%{http_code}" -d "party_name=TestParty" -X POST http://127.0.0.1:5000/delete-party)
if [ $delete_party -ne 200 ]; then
  echo "Error: delete party route returned HTTP status code $delete_party"
  exit 1
fi

echo "All 6/6 tests passed successfully"
exit 0