import bottle
import os
import random

SNAKE = 1
WALL = 2
FOOD = 3

def init(data):
    grid = [[0 for col in xrange(data['height'])] for row in xrange(data['width'])]
    for snek in data['snakes']:
        if snek['id']== data['you']['id']:
            mysnake = snek

    for p in data['you']['object']['point']:
        grid[coord[0]][coord[1]] = SNAKE


    for x in range(data['width']):
        grid[x][0] = WALL
    for x in range(data['width']):
        grid[x][data['height']-1] = WALL
    for y in range(data['height']):
        grid[0][y] = WALL
    for y in range(data['height']):
        grid[data['width'][0]] = WALL

    for f in data['food']:
        grid[f[0]][f[1]] = FOOD

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
    snake, grid = init(data)

    # TODO: Do things with data
    # for s in data['snakes']:
    #     if s['data']['length'] > 0:
    #         for p in s['data']['body']:
    #             grid[p['object']['point']['x']][p['object']['point']['y']] = SNAKE


    
    directions = ['up', 'down', 'left', 'right']
    direction = 'down'
    print direction
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
