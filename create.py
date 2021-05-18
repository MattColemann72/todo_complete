from app import db, TodoList

db.drop_all
db.create_all()

todotask = TodoList(task = "New ToDo")
# todo2 = TodoList(task = "Get to work for 4", True)
# todo3 = TodoList(task = "Work till 8", True)
# todo4 = TodoList(task = "Start second work at 9", True)
# todo5 = TodoList(task = "Finsih second work at 5.30", False)
# todo6 = TodoList(task = "Get dinner ready for around 7", False)
# todo7 = TodoList(task = "Get in bed by 9", False)

db.session.add(todotask)
db.session.commit()

# testuser = Users(first_name='Grooty',last_name='Toot') # Extra: this section populates the table with an example entry
# db.session.add(todo)
# db.session.commit()