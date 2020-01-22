from database import Database

def main():

    d = Database()
    
    #Example of inserting into database
    table_entries = ["EECS210", "asdad", "Hello", 5]
    d.create_entry(table_entries)
    
    #Example of reading into database
    test = d.read("EECS21")
    print(test)

if __name__ == '__main__':
    main()
