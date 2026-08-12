# EV3 Q-learning line follower (`python-ev3dev2`)

This is the standard Python 3/ev3dev2 version of the project. It retains the
`(mode, light_state)` state, Q-learning algorithm, bounded actions, and resumable
checkpoint used by the Pybricks version in `suma`.

Hardware ports:

- Left motor: output A
- Right motor: output D
- Color sensor: input 1
- Infrared sensor: input 4

Upload from Git Bash:

```bash
scp -r suma1 robot@169.254.18.150:/home/robot/pathFollowing/
```

Run directly with standard Python 3:

```bash
cd /home/robot/pathFollowing/suma1
python3 read_sensor.py
python3 train.py
python3 run.py
```

`training_checkpoint.pkl` is updated after every completed step. Restarting
`train.py` resumes automatically. Delete the checkpoint and Q-table only when
you deliberately want to begin fresh training.

The infrared `proximity` value is a percentage rather than centimeters; 100 is
approximately 70 cm. Tune `OBSTACLE_PROXIMITY` on the physical robot.
