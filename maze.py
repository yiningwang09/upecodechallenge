import sys
import requests
import json

def getToken():
	UID={"uid":"504983099"}
	r=request.post(" http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session",data=UID)
	tokengot=r.json()
	token=tokengot['token']
	return token
	
def getStatus(token):
    return requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token).json()
	
def out_of_bound (coordinate, chang, kuan):
    if coordinate[0] < 0 or coordinate[0] >= chang or coordinate[1] < 0 or coordinate[1] >= kuan:
        return True
    return False

	
def reverse_dir (dir):
    if dir == "UP":
        return "DOWN"
    elif dir == "LEFT":
        return "RIGHT"
    elif dir == "RIGHT":
        return "LEFT"
    else:
        return "UP"
		

def helpmaze(current,token,takenorblocked):

    dict={
    "UP" : [current[0],current[1]-1] ,
    "DOWN": [current[0], current[1]+1],
    "LEFT": [current[0]-1 , current[1]],
    "RIGHT":[current[0]+1, current[1]]
    }

    for dir,coordinate in dict.items():
        print(dir)
		print(coordinate)
        
        if (not out_of_bound(coordinate,chang,kuan)) and (coordinate not in takenorblocked):
            result = requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token, {"action":dir}).json()
            print(result)
            if result["result"] == "WALL":
                takenorblocked.append(coordinate)
            elif result["result"] == "END":
                return True
            elif result["result"] == "SUCCESS":
                takenorblocked.append(coordinate)
                if helpmaze(coordinate, token, takenorblocked):
                    return True
                else:
                    r=requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token, {"action":reverse_dir(dir)}).json()
    return False

def main():
	token=getToken()
	
	i=0
	while i<5:
		game_states = requests.get("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token).json()
		global chang
		global kuan
		chang=game_states['maze_size'][0]
		kuan=game_states['maze_size'][1]
		x = game_states["current_location"][0]
		y = game_states["current_location"][1]
		current=[x,y]
		takenorblocked = []
		takenorblocked.append(current)
		helpmaze(current, token, takenorblocked)
		
	
	
		i+=1



if __name__ == '__main__':
    main()