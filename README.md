
Домашнє завдання

Реалізуйте LRU кеш для Python коду, який використовує Redis.

---->>folder 10_1

Реалізуйте сховище інформації для "Персонального помічника" за допомогою Mongo DB.

---->>folder 10_2   Run docker-->mongodb_container, port 27017.   Start main.py


Address book commands:

    Commands format - Command meaning
    Command: "help" - returns a list of available commands with formatting   
    Command: "hello" - returns a greeting 
    Command: "add" Enter: name phone (birthday) - adds a phone to a contact, adds a birthday (optional)    
    Command: "new phone" Enter: name phone new phone - changes a phone number to a new one    
    Command: "show all" - displays all contacts   
    Command: "birthday" Enter: name - finds a birthday for name   
    Command: "soon birthday" Enter: {days} - gives a list of users who have birthday within the next {days}, where days = number of your choosing   
    Command: "find" Enter: [any strings} - finds matches in the address book and returns the findings  
    Command: "email" Enter: name email - adds an email for a user  
    Command: "new email" Enter: name old email new email - changes old email to new email  
    Command: "new address" Enter: name old address new address - changes old address to the new address  
    Command: "address" Enter: name address - adds and address for a user, address format city,street,number  
    Command: "remove contact" Enter:  name - deletes the user and all his data from the contact book  
    Command: "back" - returns to the selection of work branches
    


Notate book commands:

    Commands format - Command meaning
    Command: "help" - returns a list of available commands with formatting
    Command: "hello" - returns a greeting
    Command: "add" Enter: note - adds a note to a NotateBook
    Command: "tag" Enter: number of note and tags in format 'tag1, tag2, ...'
    Command: "del notate" Enter: the number of the note you want to delete
    Command: "del tag" Enter: the number of the note whose tags you want to delete
    Command: "change" Enter: the number of the note you want to change and new note
    Command: "find notate" Enter: the text that the notes should contain
    Command: "find tag" Enter: the tag(s) that the note's tags should contain
    Command: "show"  print a book of notes
    Command: "clear"  delete a book of notes
    Command: "back" returns to the selection of work branches
