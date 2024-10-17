from generator import LoadGenerator

lg = LoadGenerator(clients_number=5, enter_rate=0.2, max_time=5, target_url="https://example.com/")
lg.generate_load()
print("End")
