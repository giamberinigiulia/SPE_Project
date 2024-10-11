import Load_generator as lg

lg = lg.LoadGenerator(10, 0.2, 20, "http://localhost")
lg.generate_load()
print("End")
