import bottle
import os
import random

SNAKE = 1
WALL = 2
FOOD = 3

def init(data):
    grid = [[0 for col in range(data['height'])] for row in range(data['width'])]
    mysnake = data['you']

    for p in data['you']['body']['data']:
        grid[p['x']][p['y']] = SNAKE

    for x in range(data['width']):
        grid[x][0] = WALL
    for x in range(data['width']):
        grid[x][data['height']-1] = WALL
    for y in range(data['height']):
        grid[0][y] = WALL
    for y in range(data['height']):
        grid[data['width']-1][y] = WALL

    for f in data['food']['data']:
        grid[f['x']][f['y']] = FOOD

    return mysnake, grid


@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    mysnake, grid = init(data)
    x = mysnake['body']['data']['x']
    y = mysnake['body']['data']['y']

    # TODO: Do things with data
    # for s in data['snakes']:
    #     if s['data']['length'] > 0:
    #         for p in s['data']['body']:
    #             grid[p['object']['point']['x']][p['object']['point']['y']] = SNAKE

    # if (grid[x+1][y] == 2):
    #     direction = 'up'
    # else:
    #     direction = 'right'

    direction = 'right'
    return {
        'move': direction,
        'taunt': 'blast off!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
