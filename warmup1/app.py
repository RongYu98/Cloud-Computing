# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04

from flask import Flask, render_template, request, jsonify
# import datetime
import random
import emailserver

from datetime import datetime
# datetime.now().strftime('%Y-%m-%d %H:%M:%S')

app = Flask(__name__)

# dict of users to their passwords
unverified_emails = {}
verified_users = {}

current_id = 0
id_to_game = {} # grid=id_to_game["grid"], winner=id_to_game["winner"]), each element being a dict of the grid and the winner
list_of_games = {} # first username, then each game being a set of: # each game being a starting time and an id

# scores = {"human":0, "wopr":0, "tie":0}
scores = {} # user:{"human":0, "wopr":0, "tie":0}
@app.route('/adduser', methods=['GET'])
def adduser_getter():
    return render_template("adduser.html")

@app.route('/adduser', methods=['POST'])
def make_unverified_user():

    name = request.form.get('username:')
    password = request.form.get('password:')
    email = request.form.get('email:')

    info = request.json
    if (name == None and password == None and email==None):
        name = info['username']
        password = info['password']
        email = info['email']
    
    # print(request.json)

    # add user to list of unverified users, with key
    key = randomString()
    unverified_emails[email] = [name, password, email, key]

    print(name, password, email, key)
    # send email with key
    emailserver.sendEmail(key, email)

    return {'status':'OK'}
    #return render_template("adduser.html")
def randomString():
    s = 'abcdefghijklnmopqrstuvwxyz'
    r_string = ''
    for x in range(0, 10):
        r_string += s[random.randint(0, 25)]
    return r_string

@app.route('/verify', methods=['GET'])
def verify_getter():
    return render_template('verify.html')

@app.route('/verify', methods=["POST"])
def verifier():
    info = request.json
    email = request.form.get('email')
    key = request.form.get('key')
    if (email==None and key==None):
        email = info['email']
        key = info['key']
    
    if email not in unverified_emails:
        return {"status":"ERROR"}
    if key=='abracadabra' or key==unverified_emails[email][3]:

        v = unverified_emails[email]
        del unverified_emails[email]
        
        verified_users[v[0]] = [v[1], v[2]] # passwrod, email
        return {"status":"OK"}
    return {"status":"ERROR"}


@app.route("/login", methods=['GET'])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    info = request.json
    username = request.form.get('username')
    password = request.form.get('password')
    if username==None and password==None:
        username = info['username']
        password = info['password']

    
    if (username not in verified_users):
        return {"status":"ERROR"}
    print(verified_users[username][0])
    if (verified_users[username][0] != password):
        return {"status":"ERROR"}

    if username not in list_of_games:
        list_of_games[username] = []
    if username not in scores:
        scores[username] = {"human":0, "wopr":0, "tie":0}
    resp = jsonify(status="OK")
    # resp = make_response({"status":"OK"})
    resp.set_cookie('username', username)
    return resp
#{"status":"OK"}
    

@app.route("/logout", methods=["POST"])
def logout_post():
    resp = jsonify(status="OK")
    resp.set_cookie('username', '', expires=0)
    return {"status":"OK"}

@app.route("/listgames", methods=["GET", "POST"])
def listGames():
    username = request.cookies['username']
    if username not in list_of_games:
        return jsonify(status="OK", games=[])
    resp = jsonify(status="OK", games=list_of_games[username])
    return resp

@app.route("/getscore", methods=["GET"])
def getScoresGetter():
    return render_template("getScores.html")
@app.route("/getscore", methods=["POST"])
def returnScore():
    # username = request.cookies['username']
    if "username" not in request.cookies:
        return {'status':"ERROR"}
    username = request.cookies['username']
    s = scores[username]
    s['status'] = "OK"
    resp = jsonify(s)
    return resp

@app.route("/getgame", methods=["GET"])
def getgameGET():
    return render_template("getGameID.html")
@app.route("/getgame", methods=["POST"])
def getgamePOST():
    info = request.json
    i = request.form.get('id')
    if (i==None):
        i = info['id']
    if i not in id_to_game:
        return {"status":"ERROR"}
    resp = jsonify(status="OK", grid=id_to_game[i]["grid"], winner=id_to_game[i]["winner"])
    return resp

    

@app.route("/ttt/", methods=['GET'])
def page_getter():
    return render_template("index.html")

@app.route("/ttt/", methods=['POST'])
def page_poster():
    
    name = request.form.get('name')
    return render_template("post_page.html", name=name,
                           date='{:%Y-%m-%d}'.format(datetime.now()))

@app.route("/ttt/play", methods=['POST'])
def player():
    global current_id
    
    info = request.json
    if ('username' not in request.cookies):
        return {'status':"ERROR"}
        return redirect(url_for('login'))
    username = request.cookies['username']

    if info == None:
        jsonStuff = request.get_json(force=True)
        print(jsonStuff)
        move = jsonStuff['move']
        info = {'move':move}
    # for null moves..
    if (  (request.get_json(force=True)==None or "grid" not in request.get_json(force=True)) and
          info["move"]==None):
        if ('id' not in request.cookies):
            with open("TESTING", 'w+') as f:
                f.write("HOLY SHOOT")
            grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            id_of_game = str(current_id)
            current_id += 1
            list_of_games[username].append({"id":id_of_game, "start_date":datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            id_to_game[id_of_game] = {"grid":grid, "winner":"undetermined"}
            
        else:
            # grid = request.cookies['grid']
            id_of_game = request.cookies['id']
            grid = id_to_game[id_of_game]['grid']
        resp = jsonify(status="OK", grid=grid)
        resp.set_cookie("id", str(id_of_game))
        # resp.set_cookie("grid", grid)
        return resp
    
    if (info["move"]!=None):
        # we're using this then bois
        username = request.cookies['username']
        if ('id' not in request.cookies):
            # 'grid' not in request.cookies): # we need to start a new game
            grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            id_of_game = str(current_id)
            current_id += 1
            list_of_games[username].append({"id":id_of_game, "start_date":datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            id_to_game[id_of_game] = {"grid":grid, "winner":"undetermined"}
        else:
            # grid = request.cookies['grid']
            id_of_game = request.cookies['id']
            grid = id_to_game[id_of_game]['grid']

        print(info["move"])
        print(grid)
        print("THE ABOVE IS WHAT WE GOT..")
        if (info["move"] !="null" ): # probably different
            if ( grid[info["move"]]==' '): # we're not overwritting non-empty space
                grid[info["move"]] = 'X'
            winner = hasWinner(grid)
            if (winner==' '):
                grid[randomPlace(grid)] = 'O'
            winner = hasWinner(grid)
            
            id_to_game[id_of_game]['grid'] = grid
            # change of plans, None == tie, else, ' ' if game going on
            id_to_game[id_of_game]['winner'] = winner if winner in ["X", "O", "", None] else ' '
            
            # record the game
            if (winner=='X'):
                scores[username]['human']+=1
            elif (winner=='O'):
                scores[username]['wopr']+=1
            elif (winner==None):
                scores[username]['tie']+=1
            else:          
                resp = jsonify(status="OK", grid=grid)
                resp.set_cookie("id", str(id_of_game))
                return resp

            resp = jsonify(status="OK", grid=grid, winner=winner)
            resp.set_cookie("id", '', expires=0)
            return resp
            
            # MY CPU WINS, don't reset, gameover, no more
            if (winner=='O'):
                resp = jsonify(status="OK", grid=grid)
                resp.set_cookie("id", '', expires=0)
                return resp
            
            # You win, or you tied don't show off, let's reset
            # resp = jsonify(status="OK", grid=[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
            # WTF? Part: "user '0GamMEPx3w' play games" failed, with error: Error: client bot reports: non one move has been made, received [" "," "," "," "," "," "," "," "," "], last bot move: ["X"," "," "," ","X"," ","O","O","X"]
            # YOU WON, THAT"S WHY IT'S EMPTY
            
            resp.set_cookie("id", '', expires=0)
            return resp

    '''
    print(request.get_json(force=True))
    jsonStuff = request.get_json(force=True)
    grid = jsonStuff['grid']
    winner = hasWinner(grid)
    if (winner==' '): # there is still an empty spot
        grid[randomPlace(grid)] = 'O' # O is the AI?
    winner = hasWinner(grid)
    print(jsonify(grid=grid, winner=winner))
    return jsonify(grid=grid, winner=winner)
    '''
    
def hasWinner(grid):
    winningSets = [
        [0,1,2], [3,4,5], [6,7,8], # 3 across
        [0,3,6], [1,4,7], [2,5,8], # 3 downwards
        [0,4,8], [2,4,6] ]

    # for winning_set in winningSets:
    #     a
    for a,b,c in winningSets:
        if (grid[a]==grid[b] and grid[b]==grid[c] and grid[c]!=' '):
            return grid[a] # a winner

    if ' ' not in grid:
        return None
    return ' '

def randomPlace(grid):
    emptySpots = []
    for i in range(0, 9):
        cell = grid[i]
        if cell==' ':
            emptySpots.append(i)
    return emptySpots[random.randint(0, len(emptySpots)-1)] # returns inclusive,
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
    
