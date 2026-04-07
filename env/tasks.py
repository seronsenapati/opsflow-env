def load_tasks():
    return [
        {
            "type": "address_fix",
            "observation": {
                "task_type": "address_fix",
                "data": {
                    "address": "kolkata sectr 5 near tcs gitanjli park"
                }
            },
            "expected": "kolkata sector 5 near tcs gitanjali park",
            "keywords": ["kolkata", "sector", "5", "tcs", "gitanjali", "park"]
        },
        {
            "type": "prioritization",
            "observation": {
                "task_type": "prioritization",
                "data": [
                    {"order": "A", "deadline": 3, "distance": 4},
                    {"order": "B", "deadline": 1, "distance": 8},
                    {"order": "C", "deadline": 2, "distance": 2}
                ]
            },
            "expected": ["B", "C", "A"]
        },
        {
            "type": "driver_assignment",
            "observation": {
                "task_type": "driver_assignment",
                "data": {
                    "drivers": 2,
                    "orders": 3,
                    "urgent": 1
                }
            },
            "expected": "maximize_delivery"
        }
    ]
