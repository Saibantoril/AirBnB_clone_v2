from sqlalchemy.orm import sessionmaker, scoped_session

class DBStorage:
    """ Database storage engine """
    
    __engine = None
    __session = None
    
    def __init__(self):
        """ Constructor method """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                       .format(user, pwd, host, db),
                                       pool_pre_ping=True)
        
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Returns a dictionary of all objects """
        objs_dict = {}
        
        if cls:
            objects = self.__session.query(cls).all()
            for obj in objects:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objs_dict[key] = obj
                
        else:
            for cls in classes:
                objects = self.__session.query(cls).all()
                for obj in objects:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objs_dict[key] = obj
                    
        return objs_dict
    
    def new(self, obj):
        """ Adds a new object to the database """
        self.__session.add(obj)
    
    def save(self):
        """ Commits changes to the database """
        self.__session.commit()
        
    def delete(self, obj=None):
        """ Deletes an object from the database """
        if obj:
            self.__session.delete(obj)
            
    def reload(self):
        """ Creates all tables in the database """
        Base.metadata.create_all(self.__engine)
        
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        
        self.__session = Session()
        
    def close(self):
        """ Closes the session """
        self.__session.close()
