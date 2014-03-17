#!/bin/bash

KEY='toto'
USERS=`curl -s http://localhost:8080/Plone/@@notification_get_users`

for USER in $USERS
do
    curl -s "http://localhost:8080/Plone/@@notification_email?user=$USER&key=$KEY"
done
