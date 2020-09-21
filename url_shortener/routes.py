from flask import Blueprint, request, redirect, jsonify
from .extensions import db
from .models import Link, LinkSchema, InvalidUsage
import re


short = Blueprint('short', __name__)

link_schema = LinkSchema()
links_schema = LinkSchema(many=True)

@short.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@short.route('/<short_url>')
def redirect_to_url(short_url):
    '''Обработчик коротких/кастомных ссылок.'''

    if Link.query.filter_by(custom_url=short_url).first() != None:
        link = Link.query.filter_by(custom_url=short_url).first()
        return redirect(link.original_url, code=302)
    else:
        link = Link.query.filter_by(short_url=short_url).first_or_404()
        return redirect(link.original_url, code=302)


@short.route('/add_link', methods=['POST'])
def add_link():

    blob = request.get_json(force=True)

    # Валидация оригинального url, если не пройдена - 400
    http_pattern = re.compile('https?://\S*\.[a-z]+')
    simple_pattern = re.compile('\S*\.[a-z]+')
    if not blob['original_url'].startswith('http'):
        if re.match(simple_pattern, blob['original_url']):
            original_url = 'https://' + blob['original_url']
        else:
            raise InvalidUsage('Not valid URL. Try again.', status_code=400)
    elif re.match(http_pattern, blob['original_url']):
        original_url = blob['original_url']
    else: 
        raise InvalidUsage('Not valid URL. Try again.', status_code=400)
    
    # Обработка кастомного url
    if 'custom_url' in blob:
        custom_url = blob['custom_url']

        # Проверяем на уникальность кастомный URL во избежание ошибок; если существует - 400
        if Link.query.filter_by(custom_url=custom_url).first() != None:
            raise InvalidUsage('Entered custom URL already existed.', status_code=400)
        new_link = Link(original_url=original_url, custom_url=custom_url)
    else:
        new_link = Link(original_url=original_url)

    db.session.add(new_link)
    db.session.commit()
    return link_schema.jsonify(new_link)


@short.route('/links', methods=['GET'])
def get_all_links():
    '''JSON со всеми ссылками.'''
    all_links = Link.query.all()
    result = links_schema.dump(all_links)
    return jsonify(result)


@short.route('/links/<id>', methods=['GET'])
def get_link_info(id):
    '''JSON с конкретной ссылкой по id'''
    link = Link.query.filter_by(id=id).first_or_404()
    result = link_schema.dump(link)
    return jsonify(result)

@short.route('/links/<id>', methods=['PUT'])
def update_link(id):
    '''Обновление информации, по id.'''
    blob = request.get_json(force=True)
    Link.query.filter_by(id=id).update(blob)
    db.session.commit()
    link = Link.query.get_or_404(id)
    return link_schema.jsonify(link)

@short.route('/links/<id>', methods=['DELETE'])
def delete_link(id):
    link = Link.query.get(id)
    db.session.delete(link)
    db.session.commit()

    return link_schema.jsonify(link)
