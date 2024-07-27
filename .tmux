###### VENV ####### 
# Check if virtual environment is activated
if [ -z "VIRTUAL_ENV" ]
then
    printf "Virtual environment is not activated Use `BYellowpipenv BIWhiteshellNC` command. Exiting..."
    exit 1
fi

###### Docker ####### 
# Check if Docker is running
if ! docker info &> /dev/null
then
   printf "Docker( ) is not running."
   sudo systemctl start docker   
fi

SESSIONNAME="$(pwd)"

echo $SESSIONNAME

# check for session 
tmux has-session -t $SESSIONNAME &> /dev/null
if [ $? != 0 ] 
 then
  # start the new session 
  tmux new-session -d -s $SESSIONNAME

  # Window 1: Open nvim on the current project root
  tmux new-window -t $SESSIONNAME:1 -n 'nvim'
  tmux send-keys -t $SESSIONNAME:1 'nvim' C-m

  # Window 2: Command line window
  tmux new-window -t $SESSIONNAME:2 -n 'cmd'

  # Window 3: Run docker compose 
  tmux new-window -t $SESSIONNAME:3 -n 'docker'
  tmux send-keys -t $SESSIONNAME:3 'docker-compose up' C-m

  # Window 4: Run lazy docker 
  tmux new-window -t $SESSIONNAME:4 -n 'lazydocker'
  tmux send-keys -t $SESSIONNAME:4 'lazydocker' C-m

fi

tmux attach -t $SESSIONNAME
