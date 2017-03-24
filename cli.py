"""
Command line interface tool for exectuing PostgreSQL commands
To-do:
	structure query returns to be more readable
"""
import configparser
import psycopg2
import sys
import os

def cli():
	#read the database configuration file and store the relevant connection values
	try:
		print("\nReading database configuration..")
		#initialise the config.ini file
		config = configparser.ConfigParser()
		config.read('config.ini')

		#set the database connection parameters based on the config.ini file
		host = config['PostgreSQL_DB']['host']
		port = config['PostgreSQL_DB']['port']
		dbname = config['PostgreSQL_DB']['dbname']
		user  = config['PostgreSQL_DB']['user']
		password = config['PostgreSQL_DB']['password']
		print("Database configuration generated")
	except:
		print("Unable to read config.ini file")
		print(sys.exc_info())
		return

	#attempt psycopg2 connection to the database
	try:
		print("\nConnecting to database..")
		#establish psycopg2 connection and cursor based on the above inputs
		conn = psycopg2.connect(host = host,port = port,dbname = dbname,user = user,password = password)
		cursor = conn.cursor()

		#select all tables in the connected database and print the results
		print("Connection established. Current table list:\n")
		cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
		results = cursor.fetchall()
		print(results)

	except:
		print("Connection failed")
		print(sys.exc_info())
		return

	#execute PostgreSQL commands until user enters 'exit'
	while True:
		print("\nEnter valid PostgreSQL command, 'tables' to list all database tables or 'exit' to exit.")
		user_input= input().lower()
		

		if user_input == 'exit':
			#if 'exit' commit all changes, close DB connection and exit the app
			print("Closed PostgreSQL CLI")
			conn.close()
			return
		
		elif user_input == 'tables':
			#if 'tables' then print a listing of all public tables
			cursor = conn.cursor()
			cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
			print("Current table list:\n")
			results = cursor.fetchall()
			print(results)
			cursor.close()
		
		else:
			try:
				#execute user command, retrieve and print results, commit DB changes
				cursor = conn.cursor()
				cursor.execute(user_input+";")
				#results fetching is tried separately as it fails for 'delete' commands
				try:
					results = cursor.fetchall()
					print(results)
				except:
					pass
				conn.commit()
				cursor.close()
				print("Command successful")

			except:
				#on failure, rollback the last command and provide feedback
				print("Command invalid")
				print(sys.exc_info())
				conn.rollback()

if __name__ == '__main__':
    cli()