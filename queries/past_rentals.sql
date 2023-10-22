select rental.customer_id, inventory.film_id from rental 
left join inventory on rental.inventory_id=inventory.inventory_id