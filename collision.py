def detect(obj0, obj1):
	left0   = obj0.x - obj0.hitbox.width /2
	left1   = obj1.x - obj1.hitbox.width /2
	right0  = obj0.x + obj0.hitbox.width /2
	right1  = obj1.x + obj1.hitbox.width /2
	top0    = obj0.y - obj0.hitbox.height/2
	top1    = obj1.y - obj1.hitbox.height/2
	bottom0 = obj0.y + obj0.hitbox.height/2
	bottom1 = obj1.y + obj1.hitbox.height/2
	return (left0 < right1
		and left1 < right0
		and top0  < bottom1
		and top1  < bottom0)