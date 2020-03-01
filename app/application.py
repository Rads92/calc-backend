#!flask/bin/python
from flask import Flask, jsonify, request, abort, send_from_directory
from config import Config
from app import app, db
from models import Cukier, Syrop, Ziola, Ciasto
import json
import os
import math as m

### TODO LIST:
    # obsluga bledow

@app.route('/')
def render_react():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def static_proxy(path):
    """static folder serve"""
    file_name = path.split("/")[-1]
    dir_name = os.path.join(app.static_folder, "/".join(path.split("/")[:-1]))
    return send_from_directory(dir_name, file_name)
# Serve React App
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def serve(path):
#     if path != "" and os.path.exists(app.static_folder + '/' + path):
#         return send_from_directory(app.static_folder, path)
#     else:
#         return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/v1/stan', methods=['GET'])
def index():
    cukier = Cukier.query.all()
    syrop = Syrop.query.all()
    ziola = Ziola.query.all()

    return jsonify({
            'cukier': [c.as_dict() for c in cukier],
            'syrop': [c.as_dict() for c in syrop],
            'ziola': [c.as_dict() for c in ziola],
        })

### CIASTO
@app.route('/api/v1/ciasto', methods=['POST'])
def post_ciasto():
    # data = {
    #   cukier: [ {id, zuzyte}, {id, zuzyte}]
    #   syrop: [ {id, zuzyte}, {id, zuzyte}]
    #   ziola: [ {id, zuzyte}, {id, zuzyte}]
    # }
    data = json.loads(request.data)
    ciasto_dane = {
        "cena_sumaryczna": 0,
        "waga": 0,
        "cukier": [
            # { cala instancja cukru + pole 'zuzyte'}
        ],
        "syrop": [
            # { cala instancja syrop + pole 'zuzyte'}
        ],
        "ziola": [
            # { cala instancja ziola + pole 'zuzyte'}
        ],
    }
    ## Walidacja
    cukier = data['cukier']
    for c in cukier:
        c_db = Cukier.query.get(c.get('id'))

        if c_db is None or c_db.stan < c.get('zuzyte'):
            abort(400, description="Nie ma takiej ilosci na stanie")

        ciasto_dane['cukier'].append({'db': c_db, 'zuzyte': c.get('zuzyte')})

    syrop = data['syrop']
    for c in syrop:
        c_db = Syrop.query.get(c.get('id'))

        if c_db is None or c_db.stan < c.get('zuzyte'):
            abort(400, description="Nie ma takiej ilosci na stanie")

        ciasto_dane['syrop'].append({'db': c_db, 'zuzyte': c.get('zuzyte')})

    ziola = data['ziola']
    for c in ziola:
        c_db = Ziola.query.get(c.get('id'))

        if c_db is None or c_db.stan < c.get('zuzyte'):
            abort(400, description="Nie ma takiej ilosci na stanie")

        ciasto_dane['ziola'].append({'db': c_db, 'zuzyte': c.get('zuzyte')})
    ## Walidacja Koniec

    for cukier in ciasto_dane['cukier']:
        cukier_db = cukier.get('db')
        zuzyte = cukier.get('zuzyte')
        stan_obecny = cukier_db.stan - zuzyte
        cukier_db.stan = stan_obecny
        cukier_db.zuzyte = zuzyte
        ciasto_dane['waga'] += zuzyte
        ciasto_dane['cena_sumaryczna'] += zuzyte*cukier_db.cena
        ciasto_dane['cukier'] = [{'id': x.get('db').id, 'zuzyte': x.get('zuzyte')} for x in ciasto_dane['cukier']]
    # edytowanie ciasta, powinno byc :
    # revertem dodawania
    # tworzeniem nowego
    for syrop in ciasto_dane['syrop']:
        syrop_db = syrop.get('db')
        zuzyte = syrop.get('zuzyte')
        stan_obecny = syrop_db.stan - zuzyte
        syrop_db.stan = stan_obecny
        syrop_db.zuzyte = zuzyte
        ciasto_dane['waga'] += zuzyte
        ciasto_dane['cena_sumaryczna'] += zuzyte*syrop_db.cena
        ciasto_dane['syrop'] = [{'id': x.get('db').id, 'zuzyte': x.get('zuzyte')} for x in ciasto_dane['syrop']]

    for ziola in ciasto_dane['ziola']:
        ziola_db = ziola.get('db')
        zuzyte = ziola.get('zuzyte')
        stan_obecny = ziola_db.stan - zuzyte
        ziola_db.stan = stan_obecny
        ziola_db.zuzyte = zuzyte
        ciasto_dane['waga'] += zuzyte
        ciasto_dane['cena_sumaryczna'] += zuzyte*ziola_db.cena
        ciasto_dane['ziola'] = [{'id': x.get('db').id, 'zuzyte': x.get('zuzyte')} for x in ciasto_dane['ziola']]

    ciasto = Ciasto(
        partia = data['partia'],
        ilosc = ciasto_dane['waga'],
        stan = ciasto_dane['waga'],
        cukier = json.dumps(ciasto_dane['cukier']),
        syrop = json.dumps(ciasto_dane['syrop']),
        ziola = json.dumps(ciasto_dane['ziola']),
        cena = m.floor(ciasto_dane['cena_sumaryczna']/ciasto_dane['waga'] * 100)/ 100.0,
    )
    db.session.add(ciasto)
    db.session.commit()
    ciasto = Ciasto.query.all()
    return jsonify({
            'ciasto': [c.as_dict() for c in ciasto],
        })

@app.route('/api/v1/ciasto', methods=['GET'])
def get_ciasto():
    ciasto = Ciasto.query.all()

    return jsonify({
            'ciasto': [c.as_dict() for c in ciasto],
        })

# odwrotnosc dodania - przywrocenie cukru/syropu/ziol
@app.route('/api/v1/ciasto/<int:ciasto_id>', methods=['DELETE'])
def delete_ciasto(ciasto_id):
    ciasto = Ciasto.query.get(ciasto_id)
    # import pdb; pdb.set_trace()
    for cukier in json.loads(ciasto.cukier):
        _db.zuzyte -= cukier.get('zuzyte')
        _db.stan += cukier.get('zuzyte')
    for syrop in json.loads(ciasto.syrop):
        _db = Syrop.query.get(syrop.get('id'))
        _db.zuzyte -= syrop.get('zuzyte')
        _db.stan += syrop.get('zuzyte')
    for ziola in json.loads(ciasto.ziola):
        _db = Ziola.query.get(ziola.get('id'))
        _db.zuzyte -= ziola.get('zuzyte')
        _db.stan += ziola.get('zuzyte')
    db.session.delete(ciasto)
    db.session.commit()
    # (Pdb) ciasto.cukier
    # '[{"id": 1, "zuzyte": 10}]'
    # (Pdb) ciasto.ziola
    # '[{"id": 1, "zuzyte": 10}]'
    # (Pdb) ciasto.syrop
    # '[{"id": 1, "zuzyte": 10}]'
    ciasto = Ciasto.query.all();
    return jsonify({
            'ciasto': [c.as_dict() for c in ciasto],
        })

### CUKIER
@app.route('/api/v1/cukier', methods=['GET'])
def get_cukier():
    cukier = Cukier.query.all()

    return jsonify({
            'cukier': [c.as_dict() for c in cukier],
        })

@app.route('/api/v1/cukier/<int:cukier_id>', methods=['DELETE'])
def delete_cukier(cukier_id):
    cukier = Cukier.query.get(cukier_id)
    db.session.delete(cukier)
    db.session.commit()

    cukier = Cukier.query.all();
    return jsonify({
            'cukier': [c.as_dict() for c in cukier],
        })

@app.route('/api/v1/cukier', methods=['POST'])
def post_cukier():
    data = json.loads(request.data)
    cukier = Cukier(
        dostawa=data['dostawa'],
        ilosc=data['ilosc'],
        stan=data['ilosc'],
        cena=data['cena']
    )
    db.session.add(cukier)
    db.session.commit()

    cukier = Cukier.query.all()

    return jsonify({
            'cukier': [c.as_dict() for c in cukier],
        })

### SYROP
@app.route('/api/v1/syrop', methods=['GET'])
def get_syrop():
    syrop = Syrop.query.all()

    return jsonify({
            'syrop': [c.as_dict() for c in syrop],
        })

@app.route('/api/v1/syrop', methods=['POST'])
def post_syrop():
    data = json.loads(request.data)
    syrop = Syrop(
        dostawa=data['dostawa'],
        ilosc=data['ilosc'],
        stan=data['ilosc'],
        cena=data['cena']
    )
    db.session.add(syrop)
    db.session.commit()

    syrop = Syrop.query.all()

    return jsonify({
            'syrop': [c.as_dict() for c in syrop],
        })

@app.route('/api/v1/syrop/<int:syrop_id>', methods=['DELETE'])
def delete_syrop(syrop_id):
    syrop = Syrop.query.get(syrop_id)
    db.session.delete(syrop)
    db.session.commit()

    syrop = Syrop.query.all();
    return jsonify({
            'syrop': [c.as_dict() for c in syrop],
        })

### ZIOLA
@app.route('/api/v1/ziola', methods=['GET'])
def get_ziola():
    ziola = Ziola.query.all()

    return jsonify({
            'ziola': [c.as_dict() for c in ziola],
        })

@app.route('/api/v1/ziola', methods=['POST'])
def post_ziola():
    data = json.loads(request.data)
    ziola = Ziola(
        dostawa=data['dostawa'],
        ilosc=data['ilosc'],
        stan=data['ilosc'],
        cena=data['cena']
    )
    db.session.add(ziola)
    db.session.commit()

    ziola = Ziola.query.all()

    return jsonify({
            'ziola': [c.as_dict() for c in ziola],
        })


@app.route('/api/v1/ziola/<int:ziola_id>', methods=['DELETE'])
def delete_ziola(ziola_id):
    ziola = Ziola.query.get(ziola_id)
    db.session.delete(ziola)
    db.session.commit()

    ziola = Ziola.query.all();
    return jsonify({
            'ziola': [c.as_dict() for c in ziola],
        })


if __name__ == '__main__':
    app.run(debug=Config.DEV_MODE)
