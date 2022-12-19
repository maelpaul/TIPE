all: build

build:
	python3 create.py
	python3 create_loc.py

clean:
	rm trajectoire*

cleanall:
	rm base.txt bd1_storage.txt bd2_storage.txt coord_x.txt coord_y.txt localisation.txt trajectoire*
