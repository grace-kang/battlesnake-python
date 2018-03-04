import bottle
import os
import random

SNAKE = 1
ENEMY = 4
WALL = 2
FOOD = 3

def init(data):
    grid = [[-1 for col in range(data['height']+1)] for row in range(data['width']+1)]
    mysnake = data['you']

    for p in data['you']['body']['data']:
        grid[p['x']][p['y']] = SNAKE

    for x in range(data['width']):
        grid[x][-1] = WALL
    for x in range(data['width']):
        grid[x][data['height']] = WALL
    for y in range(data['height']):
        grid[-1][y] = WALL
    for y in range(data['height']):
        grid[data['width']][y] = WALL

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

    head_url = '%s://%s/static/rocket.png' % (
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

    for coors in mysnake['body']['data']:
        x = coors['x']
        y = coors['y']
        break

    # get coordinates of enemy snakes
    for s in data['snakes']['data']:
        if not (s['id'] == mysnake['id']):
            if (s['length'] > 0):
                for p in s['body']['data']:
                    grid[p['x']][p['y']] = ENEMY

    b = False
    direction = 'up'
    if (grid[x+1][y] == ENEMY):
        b = True
        if (grid[x][y-1] == ENEMY):
            direction = 'left'
        else:
            direction = 'up'
    elif (grid[x][y-1] == ENEMY):
        b = True
        if (grid[x-1][y] == ENEMY):
            direction = 'down'
        else:
            direction = 'left'
    elif (grid[x-1][y] == ENEMY):
        b = True
        if (grid[x][y+1] == ENEMY):
            direction = 'right'
        else:
            direction = 'down'
    elif (grid[x][y+1] == ENEMY):
        b = True
        if (grid[x+1][y] == ENEMY):
            direction = 'up'
        else:
            direction = 'right'

    if (b == True):
        return {
            'move': direction,
            'taunt': 'blast off!'
        }

    b = False
    if (mysnake['health'] <= 75):
        for i in range(-5,5):
            if ((x+i > 0) & (x+i < data['width'])):
                if (grid[x+i][y] == FOOD):
                    b = True
                    if (i < 0):
                        direction = 'left'
                    else:
                        direction = 'right'

            if ((y+i > 0) & (y+i < data['height'])):
                if (grid[x][y+i] == FOOD):
                    b = True
                    if (i < 0):
                        direction = 'up'
                    else:
                        direction = 'down'

            if (b == True):
                return {
                    'move': direction,
                    'taunt': 'blast off!'
                }     

    direction = 'up'
    if (grid[x+1][y] == WALL):
        if (grid[x][y-1] == WALL):
            direction = 'left'
        else:
            direction = 'up'
    elif (grid[x][y-1] == WALL):
        if (grid[x-1][y] == WALL):
            direction = 'down'
        else:
            direction = 'left'
    elif (grid[x-1][y] == WALL):
        if (grid[x][y+1] == WALL):
            direction = 'right'
        else:
            direction = 'down'
    elif (grid[x][y+1] == WALL):
        if (grid[x+1][y] == WALL):
            direction = 'up'
        else:
            direction = 'right'
    else:
        if (grid[x+1][y] == SNAKE):
            direction = 'left'
        elif (grid[x][y-1] == SNAKE):
            direction = 'down'
        elif (grid[x-1][y] == SNAKE):
            direction = 'right'
        elif (grid[x][y+1] == SNAKE):
            direction = 'up'
        else:
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
