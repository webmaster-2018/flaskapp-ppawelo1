# -*- coding: utf-8 -*-
# quiz-orm/views.py
from datetime import datetime

from flask import Flask, flash, redirect, url_for, request
from flask import render_template
from playhouse.flask_utils import get_object_or_404

from forms import KlasaForm, UczenForm
from modele import *

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


lista_plec = [(0, 'kobieta'), (1, 'mężczyzna')]

blad_nieuzupelnione_tekst = 'Uzupełnij wymagane pola!!!!'


def nieuzupelnione_blad():
    flash(blad_nieuzupelnione_tekst, 'alert-danger')


def lata(a, b):
    rok = datetime.now().year
    lata_lista = []
    for i in range(a, b):
        lata_lista.append((rok - i, rok - i))

    return lata_lista


@app.route('/')
def index():
    """Strona główna"""
    return render_template('index.html')


@app.route("/dodaj_klase", methods=['GET', 'POST'])
def dodaj_klase():
    form = KlasaForm()

    form.rok_naboru.choices = lata(-1, 10)
    form.rok_matury.choices = lata(-4, 7)

    if form.validate_on_submit():
        print(form.data)
        klasa_obj = Klasa(nazwa=form.nazwa.data,
                      rok_naboru=form.rok_naboru.data, rok_matury=form.rok_matury.data)
        klasa_obj.save()
        flash("Dodano klasę: {}".format(form.nazwa.data), 'alert-success')
        return redirect(url_for('klasy'))

    elif request.method == 'POST':
        nieuzupelnione_blad()

    return render_template('dodaj_klase.html', form=form)


@app.route('/edytuj_klase/<int:klasa_id>', methods=['GET', 'POST'])
def edytuj_klase(klasa_id):
    klasa_obj = get_object_or_404(Klasa, Klasa.id == klasa_id)
    form = KlasaForm(nazwa=klasa_obj.nazwa, rok_naboru=klasa_obj.rok_naboru, rok_matury=klasa_obj.rok_matury)
    form.rok_naboru.choices = lata(-1, 10)
    form.rok_matury.choices = lata(-4, 7)

    if form.validate_on_submit():
        print(form.data)
        klasa_obj.nazwa = form.nazwa.data
        klasa_obj.rok_naboru = form.rok_naboru.data
        klasa_obj.rok_matury = form.rok_matury.data
        klasa_obj.save()
        flash("Zaktualizowano klasę: {}".format(
            form.nazwa.data), 'alert-success')
        return redirect(url_for('klasy'))
    elif request.method == 'POST':
        nieuzupelnione_blad()

    return render_template('edytuj_klase.html', form=form, klasa=klasa_obj)


@app.route('/usun_klase/<int:klasa_id>', methods=['GET', 'POST'])
def usun_klase(klasa_id):
    klasa_obj = get_object_or_404(Klasa, Klasa.id == klasa_id)

    if request.method == 'POST':
        message_name = klasa_obj.nazwa
        klasa_obj.delete_instance()
        flash("Usunięto klasę: {}".format(message_name), 'alert-success')
        return redirect(url_for('klasy'))
    return render_template('usun_klase.html', klasa=klasa_obj)


@app.route('/klasy')
def klasy():
    klasy_lista = Klasa.select().order_by(Klasa.rok_naboru, Klasa.nazwa)
    return render_template('klasy.html', klasy=klasy_lista)


@app.route('/klasa/<int:klasa_id>')
def klasa(klasa_id):
    klasa_obj = get_object_or_404(Klasa, Klasa.id == klasa_id)

    uczniowie_obj = Uczen.select().order_by(
        Uczen.nazwisko, Uczen.imie).where(Uczen.klasa == klasa_id)
    liczba_uczniow = uczniowie_obj.count()

    return render_template('klasa.html', klasa=klasa_obj, uczniowie=uczniowie_obj, liczba_uczniow=liczba_uczniow)


@app.route("/dodaj_ucznia", methods=['GET', 'POST'])
def dodaj_ucznia():
    form = UczenForm()

    form.plec.choices = lista_plec
    form.klasa.choices = [(kl.id, kl.nazwa) for kl in Klasa.select()]

    if form.validate_on_submit():
        print(form.data)
        k = get_object_or_404(Klasa, Klasa.id==form.klasa.data)
        uczen = Uczen(imie=form.imie.data, nazwisko=form.nazwisko.data,
                      plec=form.plec.data, klasa=k.id)
        uczen.save()

        flash("Dodano ucznia: {} {}".format(
            form.imie.data, form.nazwisko.data), 'alert-success')
        return redirect(url_for('uczniowie'))

    elif request.method == 'POST':
        nieuzupelnione_blad()
    return render_template('dodaj_ucznia.html', form=form)


@app.route('/uczniowie')
def uczniowie():
    uczniowie_lista = Uczen.select().order_by(
        Uczen.klasa, Uczen.nazwisko, Uczen.imie)
    return render_template('uczniowie.html', uczniowie=uczniowie_lista)


@app.route('/usun_ucznia/<int:uczen_id>', methods=['GET', 'POST'])
def usun_ucznia(uczen_id):
    uczen = get_object_or_404(Uczen, Uczen.id == uczen_id)

    if request.method == 'POST':
        message = (uczen.imie, uczen.nazwisko)
        uczen.delete_instance()
        flash("Usunięto ucznia: {} {}".format(
            message[0], message[1]), 'alert-success')
        return redirect(url_for('uczniowie'))
    return render_template('usun_ucznia.html', uczen=uczen)


@app.route('/edytuj_ucznia/<int:uczen_id>', methods=['GET', 'POST'])
def edytuj_ucznia(uczen_id):
    uczen = get_object_or_404(Uczen, Uczen.id == uczen_id)
    k = get_object_or_404(Klasa, Klasa.nazwa == uczen.klasa.nazwa)
    form = UczenForm(imie=uczen.imie, nazwisko=uczen.nazwisko,
                     plec=uczen.plec, klasa=k.id)

    form.plec.choices = lista_plec
    form.klasa.choices = [(kl.id, kl.nazwa) for kl in Klasa.select()]

    if form.validate_on_submit():
        uczen.imie = form.imie.data
        uczen.nazwisko = form.nazwisko.data
        uczen.plec = form.plec.data
        uczen.klasa = form.klasa.data
        uczen.save()

        flash("Zaktualizowano ucznia: {} {}".format(
            form.imie.data, form.nazwisko.data), 'alert-success')
        return redirect(url_for('uczniowie'))
    elif request.method == 'POST':
        nieuzupelnione_blad()
return render_template('edytuj_ucznia.html', form=form, uczen=uczen)