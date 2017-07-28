# Vue & Django Boilerplate

This is a simple boilerplate to use for projects that use Django for the backend and VueJs for the frontend.

## Installation

Clone Project

1. Create Virtual env
2. Install dependencies
```
pip install -r requirements.txt
```

3. Setup your database (in this example a Postgres Database is already setup)
4. Create a ```.env``` file in the root directory. This will handle your config variables.
Example:
```
SECRET_KEY=N0t_A_S3Cr3T
DEBUG=True
DATABASE_NAME=db_name
DATABASE_USER=db_user
DATABASE_PASSWORD=db_password
LANGUAGE_CODE=en-us
TIME_ZONE=Europe/Berlin
```
5. Run migrations
```
python manage.py migrate
```

6. Create Superuser
```
python manage.py createsuperuser
```

7. Setup Frontend
```
cd web/vueapp && npm install
```

You're done

## Development

For development we will spin up 2 servers. The first one is our django instance which will provide the api endpoints. The second one will be our frontend development server, which eases hot-reloading etc. So if you point your browser to the site served by Django (localhost:8000) you'll see either an error or an outdated frontend, because this is used only for production.

1. Run Django server (you may have to go back to root dir first)
```
python manage.py runserver
```

2. Run Frontend Development server
(You may have to go to your frontend dir first by using ``` cd web/vueapp ```)
```
npm run dev
```

If you now visit ```localhost:8080``` you should see the frontend and when you go to the account page, you should see the superuser you just created.

## Build for Production

1. Build Frontend
(You may have to go to your frontend dir first again by using ``` cd web/vueapp ```)
```
npm run build
```

2. Collect statics
(You may have to go back to your root dir first)
```
python manage.py collectstatic
```
(You probably have to confirm)

3. Test it
Start the server
```
python manage.py runserver
```
This time go to ```localhost:8000``` and check if Django serves the frontend correctly

## Thanks

Huge Thanks to [petervmeijgaard](https://github.com/petervmeijgaard/vue-2.0-boilerplate), whose frontend boilerplate is used throughout this project.
The Readme for the frontend is located in [```web/vueapp```](/web/vueapp/README.md).


## Got questions or improvements?

Feel free to hit me up on:

[GitHub](https://github.com/berniwittmann)

Or create an [issue](https://github.com/BerniWittmann/vue-django-boilerplate/issues/new)

## Fork It And Make Your Own

What are you waiting for?! Make something awesome!

## License

The MIT License (MIT)

Copyright (c) 2017 Bernhard Wittmann

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.