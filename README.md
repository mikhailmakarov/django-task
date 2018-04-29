# Test django task

## Some remarks
There were two not fully clear moments in category adding process:

1. What to do for a category which name exists in database? If parent is same, I do nothing. Otherwise I made keeping an old one through renaming exist category and marking it as removed.
2. What to do if a category have some children and in database exist extra ones. I made moving these extra categories to root parent(Null). And Category structure in database will match with given json.


## Installation Guide
For installation you need virtualenv and python3, please follow the steps below
```
    $ git clone git@github.com:mikhailmakarov/django-task.git
    $ cd django-task
    $ virtualenv venv --python python3
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt
    $ python3 manage.py migrate
    $ python3 manage.py runserver
```

Thanks for watching and have a good day :)




--

Best Regards,

Mikhail Makarov
