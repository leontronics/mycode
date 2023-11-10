import requests

def get_game_status():
    try:
        response = requests.get('http://127.0.0.1:3000/status')
        response.raise_for_status() 
        data = response.json()
        print("Game Status:")
        print(data['status'])
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOPS: Something Else", err)

def main():
    while True:
        print("\n1. Get Game Status")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            get_game_status()
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
