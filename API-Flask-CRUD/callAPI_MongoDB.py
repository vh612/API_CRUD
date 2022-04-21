#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# callAPI_MongoDB.py
#######################

import os

import requests
import json

def postapi(port):
    api_url = "http://fit-lab.vlu.edu.vn:" + port + "/add_one"
    todo = {'_id': 17, 'title': "todo title call api 12", 'body': "todo body api "}
    headers =  {"Content-Type":"application/json"}
    response = requests.post(api_url, data=json.dumps(todo), headers=headers)
    print (response.json())
    print(response.status_code)

def getapi(port):
    api_url = "http://fit-lab.vlu.edu.vn:" + port + "/get_todo/17"
    response = requests.get(api_url)
    result = response.json()
    statuscode = response.status_code
    headers = response.headers["Content-Type"]
    print(result)
    print('status code: ', statuscode)
    print('headers: ', headers)

if __name__ == "__main__":

    homeDir = os.environ['HOME']
    userID = homeDir.split("/")[-1]

    if userID[2] == "6":
        port = "2" + userID[3:7]
    if userID[2] == "7":
        port = "3" + userID[3:7]

    print("Personal API Port: %s" %(port))

    getapi(port)
    #postapi(port)
