from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Tea:
    db_name = 'teas'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.location = db_data['location']
        self.tea_color = db_data['tea_color'] 
        self.date_made = db_data['date_made'] 
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.founder = None
        self.set_founder();
        self.vistors = []
        self.likes = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO teas (name, location, tea_color, date_made, user_id, created_at, updated_at) VALUES (%(name)s,%(location)s,%(tea_color)s,%(date_made)s,%(user_id)s,NOW(),NOW());"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM teas LEFT JOIN users on users.id = teas.user_id;" 
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_teas = [] 
        for row in results:
            print(row['location'])
            all_teas.append( cls(row) )
        return all_teas

    @classmethod
    def get_tea_founder(cls):
        query = "SELECT * FROM teas" 
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_teas = [] 
        for row in results:
            tea = cls(row)
            all_teas.append(tea)
        return all_teas

    def set_founder(self):
        query = "SELECT * FROM teas LEFT JOIN users on users.id = teas.user_id;" 
        results =  connectToMySQL(self.db_name).query_db(query)
        for row in results:
            if row['id'] == self.id:
                print(row)
                founder_data = {
                    'id' : row['users.id'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name'],
                    'email' : row['email'],
                    'password' : row['password'],
                    'created_at' : row['users.created_at'],
                    'updated_at' :row['users.updated_at']
                }
                self.founder = user.User(founder_data)
                

    @classmethod
    def get_my_teas(cls):
        query = "SELECT * FROM teas LEFT JOIN users on users.id = teas.user_id;" 
        results =  connectToMySQL(cls.db_name).query_db(query)
        my_teas = [] 
        for row in results:
            print(row['location'])
            my_teas.append( cls(row) )
        return my_teas

    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM teas WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(type(results[0]))
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE teas SET name=%(name)s, location=%(location)s, date_made=%(date_made)s, tea_color=%(tea_color)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)    

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM teas WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_tea(tea):
        is_valid = True
        print(tea)
        if len(tea['name']) < 5:
            is_valid = False
            flash("Tea name must be greater then 5 characters, Consider using an adjective if tea name is less then 5 ","tea")
        if len(tea['location']) < 2:
            is_valid = False
            flash("A Location name must be greater then 2 characters","tea")
        if len(tea['tea_color']) >= 50:
            is_valid = False
            flash("tea_color Character has to be 50 characters or less, It's like Twitter but Not","tea")
        if tea['date_made'] == "":
            is_valid = False
            flash("Please enter a date","tea")
        return is_valid

    # @classmethod
    # def get_visitors_from_teas( cls , data ):
    #     query = "SELECT * FROM teas LEFT JOIN visitors ON visitors.tea_id = teas.id LEFT JOIN users ON visitors.user_id = users.id WHERE teas.id = %(id)s;"
    #     results = connectToMySQL('teas').query_db( query , data )
    #     # results will be a list of objects with the vistor attached to each row. 
    #     tea = cls( results[0] )
    #     for row in results:
    #         vistor_data = {
    #                 'id' : row['users.id'],
    #                 'first_name' : row['first_name'],
    #                 'last_name' : row['last_name'],
    #                 'email' : row['email'],
    #                 'password' : row['password'],
    #                 'created_at' : row['users.created_at'],
    #                 'updated_at' :row['users.updated_at']
    #             }
    #         tea.vistors.append( user.User( vistor_data ) )
    #     return tea 
    # Note Refer to bottom Class Method for table gathering 


    @classmethod
    def get_one_tea( cls , data ):
        query = "SELECT * FROM teas JOIN users ON user_id = users.id LEFT JOIN visitors ON visitors.tea_id = teas.id LEFT JOIN users AS visiting_users ON visitors.user_id = visiting_users.id LEFT JOIN likes ON likes.tea_id = teas.id LEFT JOIN users AS liking_users ON liking_users.id = likes.user_id WHERE teas.id = %(id)s;"
        results = connectToMySQL('teas').query_db( query , data )
        print(results)
        # results will be a list of objects with the vistor attached to each row. 
        tea = cls( results[0] )
        for row in results:
            tea.founder = user.User.get_by_id({'id':'users.id'})
            tea.vistors.append(user.User.get_by_id({'id':'visiting_users.id'}))
            tea.likes.append(user.User.get_by_id({'id':'liking_users.id'}))
        return tea