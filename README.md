# heroku-mapviz

Original repo: https://github.com/napon/MapViz

## Changes need to deploy and run on Heroku

https://devcenter.heroku.com/articles/deploying-python  

### Pip packages
[gunicorn==19.6.0](https://github.com/dan-l/heroku-mapviz/blob/master/requirements.txt#L6)  To run the application.  
[whitenoise==2.0.6](https://github.com/dan-l/heroku-mapviz/blob/master/requirements.txt#L7)  To serve static file, since by default not supported.  
[dj_database_url](https://github.com/dan-l/heroku-mapviz/blob/master/requirements.txt#L8) To retrieve DB config on heroku, since we won't be able to create users on it (security purposes).  

### Procfile
[Procfile](https://github.com/dan-l/heroku-mapviz/blob/master/Procfile)

### Static files
[Static file settings](https://github.com/dan-l/heroku-mapviz/blob/master/polls/settings.py#L129) 
[Template](https://github.com/dan-l/heroku-mapviz/tree/master/polls/templates)  
[Static files](https://github.com/dan-l/heroku-mapviz/tree/master/polls/static)  

### Copying local db data to heroku postgres
`hg pg:push <DATABASE_NAME> <HEROKU_POSTGRES_NAME>`
