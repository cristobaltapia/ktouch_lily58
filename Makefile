.PHONY: all ktgen

all: ktlg ktgen

# Use ktouch-lesson-generator
ktlg: layout/noted.xml
	ktouch-lesson-generator -o ktlg_course_en.xml \
		lessons/lily58_noted.ktgen dictionaries/dict-en_uk.txt
	ktouch-lesson-generator -o ktlg_course_de.xml \
		lessons/lily58_noted.ktgen dictionaries/dict-de_de.txt

# Use ktgen
ktgen: layout/noted.xml
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

