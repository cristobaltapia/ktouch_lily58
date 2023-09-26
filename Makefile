.PHONY: all ktgen layout

all: ktlg ktgen

layout: layout/generate_layout.py
	cd layout && python generate_layout.py \
		--keyboard-config=lily58_config.json \
		--layout=noted_layout.json \
		--name=noted

# Use ktouch-lesson-generator
ktlg: layout/Lily58_noted.xml
	ktouch-lesson-generator -o ktlg_course_en.xml \
		lessons/lily58_noted.ktgen dictionaries/dict-en_uk.txt
	ktouch-lesson-generator -o ktlg_course_de.xml \
		lessons/lily58_noted.ktgen dictionaries/dict-de_de.txt

# Use ktgen
ktgen: layout/Lily58_noted.xml
	ktgen --output-file ktgen_course_en.xml \
		--text-file dictionaries/dict-en_uk.txt \
		--word-diversity 30 \
		--lesson-length 500 \
		lessons/lily58_noted.ktgen
	ktgen --output-file ktgen_course_de.xml \
		--text-file dictionaries/dict-de_de.txt \
		--word-diversity 30 \
		--text-distance 0.9 \
		--lesson-length 500 \
		lessons/lily58_noted.ktgen

