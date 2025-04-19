from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data setup
product_centers = {
    "C1": {"A", "B", "C"},
    "C2": {"D", "E", "F"},
    "C3": {"G", "H", "I"},
}

center_distances = {
    "C1": 10,
    "C2": 15,
    "C3": 20,
}

cost_per_trip = 2  # cost per km

def get_centers_for_product(product):
    centers = []
    for center, products in product_centers.items():
        if product in products:
            centers.append(center)
    return centers

def calculate_cost(order):
    min_cost = float('inf')
    for start_center in center_distances:
        visited = set()
        total_cost = 0
        current_location = start_center

        remaining = dict(order)

        while remaining:
            # find next pickup center with available products
            for center in center_distances:
                center_products = product_centers[center]
                to_pick = {p for p in remaining if p in center_products}
                if to_pick:
                    trip_cost = abs(center_distances[center] - center_distances[current_location]) * cost_per_trip
                    total_cost += trip_cost + center_distances[center] * cost_per_trip  # to L1
                    current_location = center
                    for product in to_pick:
                        del remaining[product]
            break

        min_cost = min(min_cost, total_cost)

    return min_cost

@app.route('/calculate-cost', methods=['POST'])
def calculate_delivery_cost():
    order = request.get_json()
    cost = calculate_cost(order)
    return jsonify({"cost": cost})

if __name__ == '__main__':
    app.run()
