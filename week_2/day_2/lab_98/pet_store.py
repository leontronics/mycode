#!/usr/bin/python3

import requests

# Base URL of the Petstore API
url = "https://petstore.swagger.io/v2/pet"

# CREATE a new pet (POST)
def create_pet(pet_data):
    response = requests.post(url, json=pet_data)
    if response.status_code == 200:
        print("Pet created successfully!")
        return response.json()
    else:
        print("Failed to create pet.")
        return response.json()

# READ pet details (GET)
def get_pet(pet_id):
    response = requests.get(f"{url}/{pet_id}")
    if response.status_code == 200:
        print("Pet details retrieved successfully!")
        return response.json()
    else:
        print("Failed to retrieve pet details.")
        return response.json()

# UPDATE pet details (PUT)
def update_pet(pet_id, updated_data):
    response = requests.put(f"{url}/{pet_id}", json=updated_data)
    if response.status_code == 200:
        print("Pet updated successfully!")
        return response.json()
    else:
        print("Failed to update pet.")
        return response.json()

# DELETE a pet (DELETE)
def delete_pet(pet_id):
    response = requests.delete(f"{url}/{pet_id}")
    if response.status_code == 200:
        print("Pet deleted successfully!")
    else:
        print("Failed to delete pet.")
        return response.json()

def main():

    new_pet = {
        "id": 42,  
        "category": {
            "id": 1,
            "name": "Dogs"
        },
        "name": "Fido",
        "photoUrls": [
            "http://example.com/photo1.jpg",
            "http://example.com/photo2.jpg"
        ],
        "tags": [
            {
                "id": 0,
                "name": "Tag1"
            },
            {
                "id": 1,
                "name": "Tag2"
            }
        ],
        "status": "available"
    }

    print("Creating a pet...")
    create_response = create_pet(new_pet)
    print(create_response)

    if 'id' in create_response:
        pet_id = create_response['id']
        print("\nGetting pet details...")
        get_response = get_pet(pet_id)
        print(get_response)
        
        print("\nUpdating pet details...")
        new_pet['name'] = 'Gabby Updated'
        update_response = update_pet(pet_id, new_pet)
        print(update_response)

        '''
        print("\nDeleting pet...")
        delete_response = delete_pet(pet_id)
        print(delete_response)'''

    else:
        print("Could not create pet, skipping other operations.")

if __name__ == "__main__":
    main()


'''
Pet Schema = {
    "id": int,
    "category": {
        "id": int,
        "name": "string"
    },
    "name": "string",
    "photoUrls": ["string"],
    "tags": [
        {
            "id": int,
            "name": "string"
        }
    ],
    "status": "string"
}

Notes:
    - The id of the pet is mandatory
    - The status of the pets are: available, pending or sold
'''