# import os
# import requests
# from urllib.request import urlretrieve
# from bs4 import BeautifulSoup
# import csv
# import pandas as pd
# import datetime 
# import random
# import re 
from mysql.connector import connect, Error
from getpass import getpass

try:
        
    with connect(
        host = "localhost", 
        user =  input('User: '),
        password = getpass(), 
        database = 'wikipedia'
    )as connection:
        print("successfully connected")

        with connection.cursor() as cursor:
            # cursor.execute(
            # """
            # CREATE TABLE pages (
            # id INT NOT NULL AUTO_INCREMENT,
            # url VARCHAR(255) NOT NULL,
            # created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            # PRIMARY KEY (id) );
            # """)

            # cursor.execute(
            # """
            # CREATE TABLE `wikipedia`.`links` (
            # `id` INT NOT NULL AUTO_INCREMENT,
            # `fromPageId` INT NULL,
            # `toPageId` INT NULL,
            # `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            # PRIMARY KEY (`id`));
            # """
            # )

            # cursor.execute(
            #     """
            #     delete from pages
            #     """
            # )
            # cursor.execute(
            #     """
            #     delete from links
            #     """
            # )

            # cursor.execute(
            #     """
            #     alter table pages 
            #     drop column url ,
            #     add column path varchar(255) not null, 
            #     add column title varchar(100) not null  
            #     """
            # )
            connection.commit()

except Error as e:
    print(e)