# Project 0: Da Art of Storytellin' by Team once upon a time

## Instructions to Run

This project runs on Python 2.7.

1. Clone into your desired repo with:

   `$ git clone https://github.com/kwang7/once_upon_a_time.git once_upon_a_time`
2. You may want to create and activate a virtual environment:
   ```
   $ virtualenv <env_name>
   $ . <env_name>/bin/activate
   ```
3. Dependencies:
    * Flask

    Install dependency using `pip`:

    `$ pip install flask`
4. Run:
   ```
   $ cd once_upon_a_time
   $ python app.py
   ```

The site can be reached at `localhost:5000`.

To deactivate your virtual environment:

`$ deactivate`

A database has been provided with the following users:
| Username    | Password       |
|-------------|----------------|
| test_user   | test_pass      |
| cool_person | cool_pass      |
| mr_brown    | brown mykolyk  |
| mr_dw       | dyrland weaver |

as well as several stories.

If you want to restore to the database provided, you can:
```
$ rm once_upon_a_time.db
$ python
>>> import db_builder
>>> db_builder.create_tables()
>>> db_builder.seed_db()
```
