# To perform performance testing, check for useCases (tasks).
# forexample, user browsing products

from locust import HttpUser, task, between
from random import randint


class WebUser(HttpUser):
    wait_time = between(1, 5)

    
    # Task can be view products, view particular product
    @task(2)
    def view_products(self):
        collection_id = randint(2, 6)
        print("Viewing products")
        self.client.get(f"/products/?collection_id={collection_id}", name="/products/")

    @task(4)
    def view_product(self):
        print("Viewing product details")
        product_id = randint(1, 1000)
        self.client.get(f"/products/{product_id}", name="/product/:id/")

    @task(1)
    def view_product_images(self):
        product_id = randint(1, 1000)
        self.client.get(f"/products/{product_id}/images/", name="/product/:id/images/")
