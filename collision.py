def collision(axis):
    if check_collision_recs(player.rec, ground_tile.rec):
        if axis == "x":
            if direction.x > 0:
                player.x = block.x - player.width
            if direction.x < 0:
                player.x = block.x + block.width
        else:
            if direction.y > 0:
                player.y = block.y - player.height
            if direction.y < 0:
                player.y = block.y + block.height

