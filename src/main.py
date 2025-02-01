from generated_data import insert_data
import time 

if __name__ == "__main__":
    count = 10_000
    for _ in range(10):
        insert_data()
        print("Inserted data: ", count)
        time.sleep(5)
        count += 10_000
