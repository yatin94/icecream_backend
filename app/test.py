from models.sales import SalesBilling
a = {'customer_name': 'Ice Cream Shop', 'bill_id': 22, 'purchases': [{'count': 1, 'flavor': {'id': 1, 'flavor': 'Mango'}, 'type': {'id': 2, 'type': 'Sundae'}, 'size': {'id': 2, 'name': 'Medium', 'price': 13}, 'toppings': [{'id': 3, 'name': 'Gems', 'price_per_scoop': 11, 'scoops': 1}], 'basePrice': 13, 'totalPrice': 24}], 'payment_type': 'gcash', 'total_amount': '24.00', 'amount_given': '24.00', 'amount_returned': 0}
a = {'customer_name': 'Ice Cream Shop', 'bill_id': 22, 'purchases': [{'count': 1, 'flavor': {'id': 1, 'flavor': 'Mango'}, 'type': {'id': 2, 'type': 'Sundae'}, 'size': {'id': 1, 'name': 'Small', 'price': 12}, 'toppings': [], 'basePrice': 12, 'totalPrice': 12}, {'count': 2, 'flavor': {'id': 1, 'flavor': 'Mango'}, 'type': {'id': 1, 'type': 'Cone'}, 'size': {'id': 3, 'name': 'Large', 'price': 14}, 'toppings': [], 'basePrice': 14, 'totalPrice': 14}], 'payment_type': 'gcash', 'total_amount': '26.00', 'amount_given': '26.00', 'amount_returned': '0'}
a =  {
    "customer_name": "Ice Cream Shop",
    "purchases": [
        {
            "count": 1,
            "flavor": {
                "flavor_name": "Mango",
                "id": 2,
                "is_deleted": 0
            },
            "type": {
                "id": 2,
                "type": "Cone",
                "flavor_id": 2,
                "is_deleted": 0
            },
            "size": {
                "id": 4,
                "name": "Small",
                "price": 10,
                "ice_cream_type_id": 2,
                "flavor_id": 2,
                "is_deleted": 0
            },
            "toppings": [],
            "basePrice": 10,
            "totalPrice": 10
        },
        {
            "count": 2,
            "flavor": {
                "flavor_name": "Choclate",
                "id": 3,
                "is_deleted": 0
            },
            "type": {
                "id": 3,
                "type": "Sundae",
                "flavor_id": 3,
                "is_deleted": 0
            },
            "size": {
                "id": 9,
                "name": "Small",
                "price": 12,
                "ice_cream_type_id": 3,
                "flavor_id": 3,
                "is_deleted": 0
            },
            "toppings": [
                {
                    "id": 3,
                    "name": "Choco chip",
                    "price_per_scoop": 12,
                    "is_deleted": 0,
                    "scoops": 2
                }
            ],
            "basePrice": 12,
            "totalPrice": 36
        }
    ],
    "payment_type": "card",
    "total_amount": "46.00",
    "amount_given": "46.00",
    "amount_returned": "0"
}
SalesBilling.model_validate(a)
