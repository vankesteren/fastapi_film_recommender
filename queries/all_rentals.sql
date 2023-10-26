select 
    rental.customer_id, 
    inventory.film_id, 
    count(*) as N
from rental 
left join inventory 
on rental.inventory_id=inventory.inventory_id
group by 
    rental.customer_id, 
    inventory.film_id
order by 1, 2

