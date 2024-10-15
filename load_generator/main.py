from generator import LoadGenerator

lg = LoadGenerator(10, 0.2, 20, "http://localhost")
lg.generate_load()
print("End")
