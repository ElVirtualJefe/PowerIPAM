
import main.app.main



engine = create_engine(SQLALCHEMY_DATABASE_URI)
db.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine))

s = Session()


def add_new_row(n):
    # Insert a new number into the 'numbers' table.
    print(f'n = {n}')
    s.execute(text("INSERT INTO numbers (number,timestamp) VALUES ("+str(n) + "," + str(int(round(time.time() * 1000))) + ");"))
    s.commit()

def get_last_row():
    # Retrieve the last number inserted inside the 'numbers'
    query = text("" + \
            "SELECT number " + \
            "FROM numbers " + \
            "WHERE timestamp >= (SELECT max(timestamp) FROM numbers)" +\
            "LIMIT 1")
    result_set = s.execute(query)  
    for (r) in result_set:  
        return r[0]


while True:
    add_new_row(random.randint(1,100000))
    print('The last value insterted is: {}'.format(get_last_row()))
    time.sleep(5)
