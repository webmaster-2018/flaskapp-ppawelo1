#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  modele.py

from peewee import *

baza_plik = 'uczniowie.db'
# MODEL
baza = SqliteDatabase(baza_plik, pragmas={
  'foreign_keys': 1
})


class BazaModel(Model):
    class Meta:
        database = baza


class Klasa(BazaModel):
  nazwa = CharField(null=False)
  rok_naboru = IntegerField(default=0)
  rok_matury = IntegerField(default=0)


class Uczen(BazaModel):
  imie = CharField(null=False)
  nazwisko = CharField(null=False)
  plec = IntegerField()
  klasa = ForeignKeyField(Klasa, related_name='uczniowie', on_delete='CASCADE')


def main(args):
  baza.connect()
  baza.create_tables([Klasa, Uczen])


if __name__ == '__main__':
  import sys

  sys.exit(main(sys.argv))

