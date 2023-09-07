#Postgresql data analysis for a video rental store based on Sakila Sample Database
#Info about the database: http://dev.mysql.com/doc/sakila/en/index.html


#Schema of the database: Actor ( actor id, first name, last name, last update)
Address ( address id, address, address2◦, district, city id→City, postal code◦, phone, last update)
Category ( category id, name, last update)
City ( city id, city, country id→Country, last update)
Country ( country id, country, last update)
Customer ( customer id, store id→Store, first name, last name, email◦, address id→Address, active◦, create date, last update◦)
Film ( film id, title, description◦, release year◦, language id→Language, original language id◦ →language, rental duration, rental rate, length◦, replacement cost, rating◦, special features◦, last update)
Film Actor ( actor id→Actor, film id→Film, last update)
Film Category ( film id→Film, category id→Category, last update)
Film Text ( film id, title, description)
Inventory ( inventory id, film id→Film, store id→Store, last update)
Language ( language id, name, last update)
Payment ( payment id, customer id→Customer, staff id→Staff, rental id→Rental, amount, payment date, last update)
Rental ( rental id, rental date, inventory id→Inventory, customer id→Customer, return date◦, staff id→Staff, last update)
Staff ( staff id, first name, last name, address id→Address, picture◦, email◦, store id→Store, active, username, password◦, last update)
Store ( store id, manager staff id→Staff, address id→Address, last update)


#As an example, I wrote 3 queries to analyze this database. 
#They are aimed at identifying the preferences of the clients of this store. 
#Based on these kind of data, it is possible to choose a vector for further business development.


#1)how much money did the salon earn from each of the films?

SELECT f.film_id, f.title, SUM (p.amount) as ertrag
FROM film f, payment p, rental r, inventory i
WHERE f.film_id=i.film_id
AND i.inventory_id=r.inventory_id
AND p.rental_id=r.rental_id
--"film" and "payment" are now connected
GROUP BY f.film_id
ORDER BY ertrag desc, f.film_id


#2)what are the favorite film categories of the regular customers? 
(a regular customer is one who has rented films more than 10 times)

WITH cat_rentals AS
--create a new table
(SELECT c.customer_id, c.first_name, c.last_name, k.name, COUNT(*) as number_rentals
FROM customer c, film_category fk, inventory i, rental r, category k
WHERE k.category_id=fk.category_id
AND fk.film_id=i.film_id
AND i.inventory_id=r.inventory_id
AND r.customer_id=c.customer_id
-- connection between category, rentals and customer
GROUP BY k.name, c.customer_id, c.first_name, c.last_name)
-- ->we´ve got a table of all clients with number of their rentals in each category
SELECT *
FROM cat_rentals
WHERE number_rentals>10
-- > clients who has rented more than 10 times
ORDER BY number_rentals desc, last_name, first_name


#3)films with which actor/actress are most often rented by сlients? determine for each customer his favorite actor/actress

WITH actor_film_rent as
--create a new table
(SELECT c.customer_id, c.first_name, c.last_name, a.actor_id, a.first_name, a.last_name, COUNT(*) as number_rentals
FROM customer c, film_actor fa, inventory i, rental r, actor a
WHERE a.actor_id=fa.actor_id
AND fa.film_id=i.film_id
AND i.inventory_id=r.inventory_id
AND r.customer_id=c.customer_id
-- connection between actors, rentals and customers
GROUP BY a.actor_id, a.first_name, a.last_name, c.customer_id, c.first_name, c.last_name)
-- ->we´ve got a table of all clients with number of their rentals of films with every actor
SELECT *
FROM actor_film_rent afr1 
WHERE not exists
(SELECT * 
FROM actor_film_rent afr2
WHERE afr1.customer_id=afr2.customer_id
AND afr1.number_rentals<afr2.number_rentals)
-- -> filter only 1 line of "actor_film_rent" for each customer with the max number of rentals
ORDER BY actor_id

