from generator import LoadGenerator

if __name__ == '__main__':
    lg = LoadGenerator(number_clients=3, enter_rate=0.2, max_time=5, target_url="https://example.com/")
    lg.generate_load()
    print("End")
