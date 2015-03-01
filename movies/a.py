import mysql.connector

db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="",db="movies")
cursor = db.cursor()
cursor1 = db.cursor()

def fformat (text) :
    rez = ''
    lungime = len(text)
    for i in range(lungime):
        if text[i]!='(' and text[i]!=',' and text[i]!=')':
            rez+=text[i]
    return rez
    
class Film(object):
    def __init__(self, id):
        self.id = id
        cursor.execute(("SELECT title, release_year, length FROM film WHERE film_id = {};").format(self.id))
        self.film_details = cursor.fetchone()
        self.actor_list = []
        cursor.execute(("SELECT actor.actor_id, actor.first_name, actor.last_name FROM film JOIN film_actor ON film.film_id = film_actor.film_id JOIN actor ON film_actor.actor_id = actor.actor_id WHERE film.film_id = {};").format(self.id) ) 
        list = cursor.fetchall()
        for item in list:
            new = Actor(item[0])
            self.actor_list.append(new)
        cursor.execute (("SELECT film_text.description FROM film JOIN film_text ON film.film_id = film_text.film_id WHERE film.film_id = {};").format(self.id))
        self.text = cursor.fetchone()
        cursor.execute (("SELECT category.name FROM film JOIN film_category ON film.film_id = film_category.film_id JOIN category ON film_category.category_id = category.category_id WHERE film.film_id = {};").format(self.id)) 
        self.cat = cursor.fetchone()
    def __str__ (self):
        rez = ''
        rez +=fformat(str(self.film_details)) + '\n'
        rez +=fformat(str(self.cat)) + '\n'
        for item in self.actor_list:
            rez+=str(item) + ' '
        rez += '\n'
        rez +=fformat(str(self.text))
        return rez
        
class Actor (object):
    def __init__(self, id):
        self.id = id
        cursor.execute (("SELECT first_name, last_name FROM actor WHERE actor_id = {} ").format(self.id))
        self.name = cursor.fetchone()
    def __str__(self):
        return fformat(str(self.name[0]+' '+self.name[1]+' '))
    
    
class Category (object):
    def __init__(self, id):
        self.id = id
        cursor.execute (("SELECT name FROM category WHERE category_id = {} ").format(self.id))
        self.name = cursor.fetchone()
        self.movie_list = []
        cursor.execute (("SELECT film.film_id, film.title FROM category JOIN film_category ON category.category_id=film_category.category_id JOIN film ON film_category.film_id = film.film_id WHERE category.category_id = {} ").format(self.id))
        list = cursor.fetchall()
        for item in list:
            new = Film(item[0])
            self.movie_list.append(new)
    def __str__ (self):
        rez = ''
        for item in self.movie_list:
            rez+=str(item)+'\n' + '\n'
        return rez
   
mov_id = input("ID movie = ") 
mov = Film(mov_id)
print (mov) 
cat_id = input("ID category = ")
cat = Category(cat_id)
print (cat)




