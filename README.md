In this Documention I will write step by step of my jeourny from creating to testing of Google cloud storage 

## Python script to Upload/Download a file from a bucket

First of all we need to make sure two APIs are enabled 
    -Google Cloud Storage
    -Google Cloud Storage JSON API

Then, we need to create a new service account with the following permissions 
    -storage object creater
    -storage object admin

Afterwards,by clicking on the sevice account we created
    -Under the "key" toolbar >> "Add Key" >> "Create new key" >> key type : JSOn
    -Download and copy its path in the sctipt that we wrote for cloud storage clinet

## What is Workload Identity Federation
