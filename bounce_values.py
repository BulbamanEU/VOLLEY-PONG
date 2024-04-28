

def update_ball(ball, offset):
    TRAVEL_X = 0
    TRAVEL_Y = 0
    ball.y -= offset
    ball.rect.center = (ball.x, ball.y)
    center = (ball.x, ball.y)
    travelling = True
    invert = False
    pause = 0
    return ball, center, travelling, invert, TRAVEL_X, TRAVEL_Y, pause