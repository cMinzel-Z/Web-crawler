# -*- coding: utf-8 -*-

from peewee import *

db = MySQLDatabase("spider_project", host="localhost", port=3306, user="root", password="#")

class Person(Model):
    name = CharField(max_length=20)
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.
        table_name = "users"
  
# 数据的增删改查
      
if __name__ == "__main__":
#    db.create_tables([Person])
    from datetime import date
    
    # 生成数据
#    uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
#    uncle_bob.save() # bob is now stored in the database
#    
#    uncle_bob = Person(name='Mick', birthday=date(1988, 1, 15))
#    uncle_bob.save() # bob is now stored in the database
#    
    # 查询数据 (只获取一条记录)
    # get方法在取不到数据的时候会报异常
#    grandma = Person.select().where(Person.name == 'Grandma L.').get()
    bob = Person.get(Person.name == 'Bob')
    print(bob.name)
    
    # 查询数据 (获取多条记录)
    query = Person.select()
    for person in query:
        print(person.name, person.birthday)
        
#    query = Person.select()[1:]
#    for person in query:
#        print(person.name, person.birthday)
        
    # 修改数据
    mod_query = Person.select().where(Person.name == 'Bob').get()
    mod_query.birthday = date(2020, 1, 17)
    # 在数据存在的时候新增数据
    # 存在的时候更新数据
    mod_query.save()
    
    # 删除数据
    del_query = Person.select().where(Person.name == 'Bob').get()
    del_query.delete_instance()