from read_values import SCREEN_HEIGHT
def net_touch(ball, NET, TRAVEL_Y):
    if ball.rect.colliderect(NET.rect) or ball.y - TRAVEL_Y > SCREEN_HEIGHT:
        return False
    else:
        return True

def wall_touch(ball, invert, TRAVEL_X, SCREEN_WIDTH, travel=0):
    if not invert:
        if ball.x+TRAVEL_X < 0 or ball.x+TRAVEL_X > SCREEN_WIDTH:
            invert = True
            ball.x += TRAVEL_X
            travel = TRAVEL_X
    return invert, travel