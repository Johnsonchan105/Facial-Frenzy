# CS190B-F23-Facial-Frenzy
Facial Frenzy is a game built by the **expresso** team (Gretchen Lam, Johnson Chan, and Cappillen Lee)

## Introduction
Our vision for our Raspberry Pi expression game project is to create an engaging and interactive experience in which players' emotions shape the gameplay. We are using several devices to create a facial recognition game where the player has to make the expression specified by the computer. Utilizing OpenCV, a facial expression detection library, and a laptop and webcam, our game will enable players to communicate, connect, and express themselves in a fun way. Our design implementation will seamlessly integrate the Raspberry Pi, providing an endpoint and accessible platform for players to share their emotions through expressive play. Future features we plan to include are utilizing an Amazon Echo dot to interact with the raspberry pi and share the results of the gameplay.

## Features
- Main game that tests players ability to make facial expressions
- Stores players progress in the cloud
- Players can view their past expressions
- Leaderboard system to encourage social and friendly competition 

## System requirements
Install all python libraries in requirements.txt. Systems that are supported and software tools required for this project are listed below
- System
  - Windows 10 +
  - Any Linux-based system
  - Ubuntu 20+/ CentOS 7+
  - Any system
  - Docker container
- Software tools
  - python 3.10+
  - tensorflow 2.0+
  - Postgres SQL
  - Firebase Storage

## Installation
Clone repo.
```bash
git clone git@github.com:ucsb/CS190B-F23-expresso-cappillen.git
```
Then run
```bash
cd CS190B-F23-expresso-cappillen
pip install -r requirements.txt
```
If you are working on a M1 Apple Silicon machine then you should uninstall tensorflow and reinstall:
```
pip install tensorflow-macos
```
### Build programs
To run the game, enter the commands:
```
cd game
python main.py
```
To run the web app alongside, enter the commands:
```
cd rasp-api
python app.py
```
### Environment Variables and Secrets
Make sure to pass in the correct environment variables.
- PostgresSQL Database URI (string)
- Firebase service account credientials (in a json file)

## Contributors
- Cappillen Lee (cappillen@ucsb.edu)
- Gretchen Lam (gretchenlam@ucsb.edu)
- Johnson Chan (c_chan@ucsb.edu)

## Acknowledgments
We would like to thank UCSB, Professor Krintz, and our TAs.