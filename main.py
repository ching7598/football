from vpython import *
# 建立場景
scene = canvas(title="FootBall",
               width=1000, height=650,
               background=color.white)
               
from utils.game_field import *
from obj.physical_object import *               
              
               
# 在畫面上方建立按鈕
running = True  # 控制是否繼續動畫



def stop_animation(btn):
    global running
    if running:
        running = False
    else:
        running=True
        f_start()
    


def kick_ball(btn):
    ball.add_force(
        addedforce=vector(
            float(f_x_input.text),
            float(f_y_input.text),
            float(f_z_input.text)
        )        
    )
    
def player1_run(btn):
    player1.run_forward()

def player1_back(btn):
    player1.backpedal()

def player1_turn(btn):
    player1.turn_right(degree=30)

def player1_shuffle(btn):
    player1.right_shuffle()
    
def player1_kick(btn):
    get=player1.kick_ball(ball)
    

    

button(text="❌ 結束動畫", bind=stop_animation)
button(text="kick", bind=kick_ball)
scene.append_to_caption('X：')
f_x_input = winput(bind=None)
scene.append_to_caption('Y：')
f_y_input = winput(bind=None)
scene.append_to_caption('Z：')
f_z_input = winput(bind=None)
button(text="player1_forward", bind=player1_run)
button(text="player1_back", bind=player1_back)
button(text="player1_turn30", bind=player1_turn)
button(text="player1_shuffle", bind=player1_shuffle)
button(text="player1_kick", bind=player1_kick)




my_field=FieldManager();
blueTeam=Team(name="blueTeam",color=color.blue)
my_field.add_team(blueTeam);
blueTeam.add_defendGoal(my_field.rightGoal);
blueTeam.add_targetGoal(my_field.leftGoal);



# 建立足球
ball=Ball();
player1=Player(pos_center=vector(0,6,10))
blueTeam.add_player(player1,10)

my_field.push_into_field(ball);
my_field.push_into_field(player1);




##label_ball=label(pos=vector(0, 20, 30),text="",height=40, color=color.yellow, box=False)

 # 動畫主迴圈
def f_start():
    global running;
    if not running:
        running=True;
        
    while running:
        rate(Physis.fps)
        ##label_ball.text=str(player1.velocity)+"\n"+str(player1.acceleration)+"\n"+str(player1.force);
        my_field.next_state()

           
    

f_start()

