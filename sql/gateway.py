#%%
import mysql.connector
import json
import sql.config as config

class gateway():

    def __init__(self):
        self.db = mysql.connector.connect(
            host=config.HOST,
            user=config.USER,
            passwd=config.PASS,
            database=config.DB
        )
        self.cur = self.db.cursor()
    

    # GET - return dict full of property data in order
    def get_properties(self):
        try:
            self.cur.execute("SELECT * FROM Property")
        except:
            return 404
        table = []
        for (property_id, address, city, state, _zip) in self.cur:
            table.append({"id":property_id,"adddress":address, "city":city, "state":state,"zip":_zip})
        return json.dumps(table)


    # POST - adds a property Address must be between 1 and 255 chars. City must be between 1 and
    # 50 chars. State must be exactly 2 chars. Zip must be between 5 and 10 chars. All fields
    # are required. The system will auto-assign a unique id to the new property
    def post_property(self,address,city,state,_zip):
        if address:
            if not (1 <= len(address) <= 255):
                return json.dumps([{"message":"address is not between 1 and 255 characters"}])
            
        if city:
            if not (1 <= len(city) <= 50):
                return json.dumps([{"message":"city is not between 1 and 50 characters"}])
            
        if state:
            if not (len(state) == 2):
                return json.dumps([{"message":"state is not 2 characters"}])

        if _zip:
            if not (5 <= len(str(_zip)) <= 10):
                return json.dumps([{"message":"zip is not between 5 and 10 characters: "+str(_zip)}])

        try:
            self.cur.execute(f"INSERT INTO Property (address, city, state, zip) VALUES ('{address}','{city}','{state}','{_zip}')")
            self.db.commit()
            self.cur.execute(f"SELECT property_id FROM Property WHERE address = '{address}'")
            for prop_id in self.cur:
                return prop_id, 200
                
        except:
            return 404



    # GET - return detailed info for property with input id
    def get_property(self,id):
        try:
            self.cur.execute(f"SELECT * FROM Property WHERE property_id = '{id}'")
            for (property_id, address, city, state, _zip) in self.cur:
                prop = {"id":property_id,"adddress":address, "city":city, "state":state,"zip":_zip}
            return prop
        except:
            return 404


    # DELETE - delete the property w the input id
    def delete_property(self,id):
        self.cur.execute(f"SELECT 1 FROM Property WHERE property_id = '{id}'")
        for x in self.cur:
            if len(x) > 0:
                self.cur.execute(f"DELETE FROM Property WHERE property_id = '{id}'")
                self.db.commit()
                return 200
        else:
            return 404


    # PUT - Updates the property with an id value of <id>. Only the fields to be modified need be present in the response data.
    def put_property(self,id,address,city,state,_zip):

        if address:
            if (1 <= len(address) <= 255):
                self.cur.execute(f"UPDATE Property SET address = '{address}' WHERE property_id = '{id}'")
                self.db.commit()
            else:
                return json.dumps([{"message":"address is not between 1 and 255 characters"}])

        if city:
            if (1 <= len(city) <= 50):
                self.cur.execute(f"UPDATE Property SET city = '{city}' WHERE property_id = '{id}'")
                self.db.commit()
            else:
                return json.dumps([{"message":"city is not between 1 and 50 characters"}])

        if state:
            if (len(state) == 2):
                self.cur.execute(f"UPDATE Property SET state = '{state}' WHERE property_id = '{id}'")
                self.db.commit()
            else:
                return json.dumps([{"message":"state is not 2 characters"}])

        if _zip != None:
            if (5 <= len(str(_zip)) <= 10):
                self.cur.execute(f"UPDATE Property SET zip = '{_zip}' WHERE property_id = '{id}'")
                self.db.commit()
            else:
                return json.dumps([{"message":"zip is not between 5 and 10 characters"}])
        
        return 200

# %%
