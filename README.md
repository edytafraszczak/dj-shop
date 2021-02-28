# dj-shop
Django based shop application. It provides following features
- `grappelli` based admin
- i18n support utilizing `parler` for categories and products
- coupon codes
- user cart
- `bootsrap4` design
- `bootsrap4` forms with `crispy`
- user registration and authentication
- pdf invoice generation
- email based authentication
- docker config

You can see more screens of the app in [showcase](showcase) catalog.

<p float="left">
  
<img src="https://github.com/edytafraszczak/dj-shop/blob/main/showcase/1.PNG" width="250" height="117" style="padding:10px">
<img src="https://github.com/edytafraszczak/dj-shop/blob/main/showcase/3.PNG" width="250" height="117" style="padding:10px">
<img src="https://github.com/edytafraszczak/dj-shop/blob/main/showcase/4.PNG" width="250" height="117" style="padding:10px">
<img src="https://github.com/edytafraszczak/dj-shop/blob/main/showcase/6.PNG" width="250" height="117" style="padding:10px">
<img src="https://github.com/edytafraszczak/dj-shop/blob/main/showcase/9.PNG" width="250" height="117" style="padding:10px">
<img src="https://github.com/edytafraszczak/dj-shop/blob/main/showcase/13.PNG" width="250" height="117" style="padding:10px">
</p>




## How to instructions
- Run app
```
docker-compose up
```
- Generate migrations
```
docker-compose run web python manage.py makemigrations
```
- Create super user
```
docker-compose run web python manage.py createsuperuser
```
- Migrate migrations
```
docker-compose run web python manage.py migrate
```
- Generate messages
```
docker-compose run web python manage.py makemessages -all
```
- Compile messages
```
docker-compose run web python manage.py compilemessages
```
