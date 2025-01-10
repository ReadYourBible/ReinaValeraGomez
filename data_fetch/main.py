#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Victor V. R. Matos (@vvrmatos)
# Description: This script creates a directory structure for books of the Bible,
# fetches chapter content from eBible.org, and saves verses as text files.
# License: CC0 1.0 Universal

import os
import re
import sys
from time import sleep
from pathlib import Path
from collections import namedtuple
from reina_valera_gomez import SessionManager, VerseExtractor


file_path = Path(__file__)
root_path = file_path.parent.parent


Book = namedtuple("Book", ["name", "chapters", "code", "site_code"])


books_data = [
    ("Génesis", 50, "genesis", "GEN"),
    ("Éxodo", 40, "exodo", "EXO"),
    ("Levítico", 27, "levitico", "LEV"),
    ("Números", 36, "numeros", "NUM"),
    ("Deuteronomio", 34, "deuteronomio", "DEU"),
    ("Josué", 24, "josue", "JOS"),
    ("Jueces", 21, "jueces", "JDG"),
    ("Rut", 4, "rut", "RUT"),
    ("I Samuel", 31, "i-samuel", "1SA"),
    ("II Samuel", 24, "ii-samuel", "2SA"),
    ("I Reyes", 22, "i-reyes", "1KI"),
    ("II Reyes", 25, "ii-reyes", "2KI"),
    ("I Crónicas", 29, "i-cronicas", "1CH"),
    ("II Crónicas", 36, "ii-cronicas", "2CH"),
    ("Esdras", 10, "esdras", "EZR"),
    ("Nehemías", 13, "nehemias", "NEH"),
    ("Ester", 10, "ester", "EST"),
    ("Job", 42, "job", "JOB"),
    ("Salmos", 150, "salmos", "PSA"),
    ("Proverbios", 31, "proverbios", "PRO"),
    ("Eclesiastés", 12, "eclesiastes", "ECC"),
    ("Cantares", 8, "cantares", "SNG"),
    ("Isaías", 66, "isaias", "ISA"),
    ("Jeremías", 52, "jeremias", "JER"),
    ("Lamentaciones", 5, "lamentaciones", "LAM"),
    ("Ezequiel", 48, "ezequiel", "EZK"),
    ("Daniel", 12, "daniel", "DAN"),
    ("Oseas", 14, "oseas", "HOS"),
    ("Joel", 3, "joel", "JOL"),
    ("Amós", 9, "amos", "AMO"),
    ("Abdías", 1, "obdias", "OBA"),
    ("Jonás", 4, "jonas", "JON"),
    ("Miqueas", 7, "miqueas", "MIC"),
    ("Nahúm", 3, "nahum", "NAM"),
    ("Habacuc", 3, "habacuc", "HAB"),
    ("Sofonías", 3, "sofonias", "ZEP"),
    ("Hageo", 2, "hageo", "HAG"),
    ("Zacarías", 14, "zacarias", "ZEC"),
    ("Malaquías", 4, "malaquias", "MAL"),
    ("Mateo", 28, "mateo", "MAT"),
    ("Marcos", 16, "marcos", "MRK"),
    ("Lucas", 24, "lucas", "LUK"),
    ("Juan", 21, "juan", "JHN"),
    ("Hechos", 28, "hechos", "ACT"),
    ("Romanos", 16, "romanos", "ROM"),
    ("I Corintios", 16, "i-corintios", "1CO"),
    ("II Corintios", 13, "ii-corintios", "2CO"),
    ("Gálatas", 6, "galatas", "GAL"),
    ("Efesios", 6, "efesios", "EPH"),
    ("Filipenses", 4, "filipenses", "PHP"),
    ("Colosenses", 4, "colosenses", "COL"),
    ("I Tesalonicenses", 5, "i-tesalonicenses", "1TH"),
    ("II Tesalonicenses", 3, "ii-tesalonicenses", "2TH"),
    ("I Timoteo", 6, "i-timoteo", "1TI"),
    ("II Timoteo", 4, "ii-timoteo", "2TI"),
    ("Tito", 3, "tito", "TIT"),
    ("Filemón", 1, "filemon", "PHM"),
    ("Hebreos", 13, "hebreos", "HEB"),
    ("Santiago", 5, "santiago", "JAS"),
    ("I Pedro", 5, "i-pedro", "1PE"),
    ("II Pedro", 3, "ii-pedro", "2PE"),
    ("I Juan", 5, "i-juan", "1JN"),
    ("II Juan", 1, "ii-juan", "2JN"),
    ("III Juan", 1, "iii-juan", "3JN"),
    ("Judas", 1, "judas", "JUD"),
    ("Apocalipsis", 22, "apocalipsis", "REV")
]


books = [Book(name, chapters, code, site_code) for name, chapters, code, site_code in books_data]

def create_book_dir(books: Book):
    for book in books:
        book_number = books.index(book) + 1
        book_number = str(book_number) if book_number >= 10 else "0" + str(book_number)        
        book_dir_name = f"{book_number}-{book.code}"
        os.makedirs(root_path / book_dir_name, exist_ok=True)

def main():    
    base_url = "https://ebible.org"
    session_manager = SessionManager(base_url)

    create_book_dir(books)

    for book in books:
        book_number = books.index(book) + 1
        book_number = f"0{book_number}" if book_number < 10 else str(book_number)
        book_dir_name = f"{book_number}-{book.code}"

        for chapter in range(1, book.chapters + 1):
            if book.site_code == "PSA":
                chapter_number = f"00{chapter}" if chapter < 10 else f"0{chapter}" if chapter <= 99 else str(chapter)
            else:
                chapter_number = f"0{chapter}" if chapter < 10 else str(chapter)
            file_name = f"{book.code}-{chapter_number}.txt"
            print(file_name)
    
            page_path = f"/sparvg/{book.site_code}{chapter_number}.htm"
            
            page_content = session_manager.fetch_page(page_path)

            # Extract verses
            extractor = VerseExtractor(page_content)
            container = extractor.get_text_container()

            if container:                
                verses = extractor.extract_all_text(container)
                print(f"Extracted {len(verses)} verses for {book.name} Chapter {chapter}")

                # Save verses to file
                file_path = root_path / book_dir_name / file_name
                if not file_path.exists() or file_path.stat().st_size == 0:
                    with open(file_path, "a") as file:
                        print(verses)
                        for verse in verses:
                            if verse == verses[-1]:
                                file.write(f"{verse}")
                            else:
                                file.write(f"{verse}\n")
                else:
                    print(f"File {file_name} already exists and is not empty. Skipping.")
            else:
                print(f"No verses found for {book.name} Chapter {chapter}!")

if __name__ == "__main__":
    main()
