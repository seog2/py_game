# -*- coding: utf-8 -*-
"""
    FileName : PyShootin_A07.py
    Description : 
        원본 새로 정리
        gameOver() 붙이기 성공
        GameOverSound 추가
        GameOverSound 화면에 깜박거림 추가
        global 정리
        
        맞을때 마다 속도 빨라지도록
        ENDING() 추가
        
        배경화면 추가 성공
        
        필살기 추가 성공
        
"""

import pygame
import random
import sys
import time
from pygame.rect import *

# 스테이지 배경화면 구현
def back() :
    global BLACK, gamePad, clock, background1, background2, isGameOver, background1_x, background2_x
    
    if not isGameOver : #충돌 예외처리
        
        background1_x -= 3
        background2_x -= 3
        
        if background1_x == -1080 :
            background1_x = 1080
            
        if background2_x == -1080 :
            background2_x = 1080
            
        gamePad.blit( background1, (background1_x, 0))
        gamePad.blit( background2, (background2_x, 0))
        
def back2() :
    global BLACK, gamePad, clock, background3, background4, isGameOver, background1_x, background2_x
    
    if not isGameOver : #충돌 예외처리
        
        background1_x -= 3
        background2_x -= 3
        
        if background1_x == -1080 :
            background1_x = 1080
            
        if background2_x == -1080 :
            background2_x = 1080
            
        gamePad.blit( background3, (background1_x, 0))
        gamePad.blit( background4, (background2_x, 0))
        
def back3() :
    global BLACK, gamePad, clock, background5, background6, isGameOver, background1_x, background2_x
    
    if not isGameOver : #충돌 예외처리
        
        background1_x -= 3
        background2_x -= 3
        
        if background1_x == -1080 :
            background1_x = 1080
            
        if background2_x == -1080 :
            background2_x = 1080
            
        gamePad.blit( background5, (background1_x, 0))
        gamePad.blit( background6, (background2_x, 0))      

# 키 event
def eventProcess():
    global move, missileSound, boomSound, boom, isBoom
    
    for event in pygame.event.get(): # 리스트형태로 event 전달
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                pygame.quit()
                
            if event.key == pygame.K_LEFT :
                move.x = -5
            if event.key == pygame.K_RIGHT :
                move.x = 5
            if event.key == pygame.K_UP :
                move.y = -5
            if event.key == pygame.K_DOWN :
                move.y = 5
            if event.key == pygame.K_SPACE  :
                missileSound.play()
                makeMissile()
                
            # 필살기 구현
            while isBoom :
                if event.key == pygame.K_q :
                    boom()
                    boomSound.play()
                break

                
        if event.type == pygame.KEYUP :     # 방향키를 떼면 전투기 멈
            if ( event.key == pygame.K_UP or event.key == pygame.K_DOWN ) :
                    move.y = 0
            if ( event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT ) :
                    move.x = 0

# Player, Monster, Missile, 충돌실험
def movePlayer() : # player 출력
    global padWidth, padHeight, playerWidth, playerHeight, move, isGameOver, recPlayer, player, gamePad

    if not isGameOver : #충돌 예외처리
    
        recPlayer.x += move.x
        recPlayer.y += move.y    
    
    if recPlayer.x < 0 :
        recPlayer.x = 0
    if recPlayer.x > padWidth - playerWidth :
        recPlayer.x = padWidth - playerWidth
    if recPlayer.y < 0 :
        recPlayer.y = 0
    if recPlayer.y > padHeight - playerHeight :
        recPlayer.y = padHeight - playerHeight    
    
    gamePad.blit( player, recPlayer )

def makeMonster( monster ) :
    global padWidth, padHeight, isGameOver, recMonster, monsterHeight
        
    if isGameOver :
        return
    if timeDelay500ms() :
    
        index = random.randint( 0, len( monster ) - 1 ) # 인덱스 값을 0~ len(monster)-1 까지 가져오겠다
        if recMonster[ index ].x == padWidth + 1 :
            recMonster[ index ].y = random.randint( 0 , padHeight-monsterHeight )
            recMonster[ index ].x = padWidth
    
def moveMonster( monster ) : # monster 출력
    global gamePad, padWidth, passed, isGameOver, recMonster, monsterSpeed
                  
    makeMonster( monster )
    
    
    for k in range( len ( monster ) ) :
        if recMonster[ k ].x == padWidth + 1 :
            continue
        if not isGameOver :
            recMonster[ k ].x -= monsterSpeed
            
        if recMonster[ k ].x < 0 :
            recMonster[ k ].x = padWidth + 1
            passed += 1
            
        
        gamePad.blit( monster[ k ], recMonster[ k ] )
        
      
        
        if ( passed == 3 ) : # 운석 3개 놓치면 게임오버
            gameOver()

def makeMissile():
    global isGameOver, recPlayer, playerWidth, playerHeight, missile, recMissile
    
    if isGameOver:
        return
    
    for k in range( len( missile ) ) :
        if recMissile[k].x == -1 :
            recMissile[k].x = recPlayer.x + playerWidth
            recMissile[k].y = recPlayer.y + playerHeight/4
            break

def moveMissile():
    global padWidth, missile, recMissile
    
    for k in range( len( missile ) ) :
        if recMissile[k].x == -1 :
            continue

        if not isGameOver:
            recMissile[k].x += 10
            
        if recMissile[k].x > padWidth  :
            recMissile[k].y = -1 
            
                 
            
        gamePad.blit( missile[k], recMissile[k] )
        
def CheckCollision() :
    global padWidth, isGameOver, recPlayer, recMonster
    
    if isGameOver :
        return
    
    for rec in recMonster :
        if rec.x == padWidth + 1 :
             continue
         
        if ( rec.top < recPlayer.bottom \
            and recPlayer.top < rec.bottom \
            and rec.left < recPlayer.right \
            and recPlayer.left < rec. right ) :
                
            gameOver()
    
def CheckCollisionMissile():
    global BLACK, explosionSound, gamePad, explosion, padWidth, score, score2, score3, isGameOver, recMonster, recMissile, monsterSpeed

    if isGameOver:
        return

    for rec in recMonster :
        if rec.x == padWidth + 1 :
            continue
        for recM in recMissile :
            if rec.top < recM.bottom \
                and recM.top < rec.bottom \
                and rec.left < recM.right \
                and recM.left < rec.right:
                
                gamePad.blit( explosion, (rec) )
                explosionSound.play()
                
                rec.x = padWidth + 1
                recM.x = -1
                score += 1
                
                monsterSpeed += 0.2
                if monsterSpeed > 9 :
                    monsterSpeed = 8
                
                nextStage()

# 스테이지 전환
def nextStage() :
    global score, monsterSpeed

    if score == 6 :
        runGame2()
        
    if score == 15 :
        runGame3()
        
    if score == 25 :
        showEnding()

# 필살기( 커맨드 입력시 )
def boom():
    global isGameOver, score, isBoom, monseterWidth, monsterHeight
    isGameOver = False

    
    for k in range( len( monster ) ) :
        recMonster[k].x = padWidth + 1
        for k in range( len( monster ) ) :
            recMonster[ k ] = monster[ k ].get_rect()
            monsterSize[ k ] = recMonster[ k ].size
            monseterWidth = monsterSize[ k ][ 0 ]
            monsterHeight = monsterSize[ k ][ 1 ]
            recMonster[ k ].x = padWidth + 1
            isBoom = False

# 오프닝 화면 구현
def showOpening():
    global gamePad, clock
                  
    pygame.mixer.music.load( 'opening.wav' )
    pygame.mixer.music.play( -1 ) # 배경음악재생
    openingImage = pygame.image.load('opening1.png')
    openingImage2 = pygame.image.load('opening2.png')
    openingImage3 = pygame.image.load('opening3.png')
    openingImage4 = pygame.image.load('opening4.png')
    textfont = pygame.font.Font('NanumGothic.ttf', 40)
    text1 = textfont.render("아주 먼 과거에... 지구에 운석이 떨어졌다", True, (255, 255, 255))
    text2 = textfont.render("쥐들이 운석을 발견했고 운석에서 나오는 에너지때문에", True, (255, 255, 255))
    text3 = textfont.render("쥐들의 힘이 강해졌고 쥐들은 지구를 침공하기 시작했다", True, (255, 255, 255))
    text4 = textfont.render("이를 두고 볼 수 없는 고양이가 지구를 지키려 한다!!!", True, (255, 255, 255))

    elapsed_time = 0
    gamePad.fill((0, 0, 0))
    
    while elapsed_time < 3000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gamePad.blit(openingImage, (0, 0))
        gamePad.blit(text1, (170 , 578))
        pygame.display.update()

        elapsed_time += clock.tick(60)
        
    elapsed_time = 0
    
    while elapsed_time < 3000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gamePad.blit(openingImage2, (0, 0))
        gamePad.blit(text2, (75 , 583))
        pygame.display.update()

        elapsed_time += clock.tick(60)

    elapsed_time = 0
    
    while elapsed_time < 3000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gamePad.blit(openingImage3, (0, 0))
        gamePad.blit(text3, (70 , 583))
        pygame.display.update()

        elapsed_time += clock.tick(60)

    elapsed_time = 0
    
    while elapsed_time < 3000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gamePad.blit(openingImage4, (0, 0))
        gamePad.blit(text4, (80 , 583))
        pygame.display.update()

        elapsed_time += clock.tick(60)

    elapsed_time = 0
    
    main()

# 엔딩 화면 구현
def showEnding():
    global gamePad, clock 
    
    endingImage01 = pygame.image.load('ending.png')
    endingImage02 = pygame.image.load('name.png')
    textfont1 = pygame.font.Font('NanumGothic.ttf', 100)
    textfont2 = pygame.font.Font('NanumGothic.ttf', 140)
    textfont3 = pygame.font.Font('NanumGothic.ttf', 35)
    text1 = textfont1.render("지구지켜라 ~", True, (255, 0, 0))
    text2 = textfont2.render("냥냥", True, (255, 0, 0))
    text3 = textfont3.render("저희 게임을 플레이 해 주셔서 감사합니다~", True, (255, 255, 0))
    endingImage_x = 900
    endingImage_y = 800
    start_ticks = pygame.time.get_ticks()
    
    elapsed_time = 0
    gamePad.fill((0, 0, 0))
    
    while elapsed_time < 8000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
              
    
        if endingImage_y > 0:
            endingImage_y -= 2
        
        if endingImage_y <= 10:
            endingImage_y = -500
        
        gamePad.blit(endingImage01, (0,0))
        gamePad.blit(endingImage02, ( endingImage_x - endingImage02.get_width()/2, endingImage_y - endingImage02.get_height()/2 ) )
        
        #텍스트 출력
        if endingImage_y == -500:
            gamePad.blit(text1, (300, 150))
            gamePad.blit(text2, (300, 300))
        if pygame.time.get_ticks() - start_ticks >= 7500 and pygame.time.get_ticks() % 1500 < 750:
            gamePad.blit(text3, (200, 550))
         
        pygame.display.update()
        elapsed_time += clock.tick(60)

    elapsed_time = 0
        
    while elapsed_time < 10000:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    __init__()
                    showOpening()    

# 게임 오버 화면 구현
def gameOver() :
    global gamePad, gameOverSound, clock, score
    pygame.mixer.music.stop()
    gameOverSound.play()
    start_ticks = pygame.time.get_ticks()
    textfont = pygame.font.Font( 'NanumGothic.ttf', 80 )
    textfont2 = pygame.font.Font( 'NanumGothic.ttf', 40 )
    textfont3 = pygame.font.Font( 'NanumGothic.ttf', 20 )
    text1 = textfont.render("게임 오버!", True, (255, 0, 0))
    text2 = textfont2.render("처음부터", True, (255, 255, 0))
    text3 = textfont2.render("다시하기", True, (255, 255, 0))
    text4 = textfont2.render("현재스테이지", True, (255, 255, 0))
    text5 = textfont2.render("다시하기", True, (255, 255, 0))
    text6 = textfont3.render("아래방향키를 누르세요", True, (0, 255, 255))
    text7 = textfont3.render("SPACE키를 누르세요", True, (255, 0, 255))
    gameoverImage = pygame.image.load( 'gameover.png' )
    
    elapsed_time = 0
    gamePad.fill((0, 0, 0))
    
    textpos = text1.get_rect()
    textpos.center = ( padWidth / 2, padHeight / 2 )
    text_y = padHeight / 2
    
    while elapsed_time < 2000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        gamePad.blit(text1, textpos )
        
        pygame.display.update()

        elapsed_time += clock.tick(60)

    elapsed_time = 0
    
    gamePad.fill((0, 0, 0))
    while elapsed_time < 700:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        gamePad.fill((0, 0, 0))
        text_y -= 5
        textpos.center = ( padWidth / 2, text_y)
        
        if text_y <= 100:
          text_y = 100
          
        gamePad.blit(text1, textpos )
          
          
        pygame.display.update()

        elapsed_time += clock.tick(60)

    elapsed_time = 0
    
    while elapsed_time < 1000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        gamePad.fill((0, 0, 0))
        textpos.center = ( padWidth / 2, 95)

        gamePad.blit(text1, textpos )
        gamePad.blit(gameoverImage, (355, 160))
        
          
        pygame.display.update()

        elapsed_time += clock.tick(60)

    elapsed_time = 0
    
    while elapsed_time < 30000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if ( event.type in [ pygame.KEYDOWN ] ) :
              
                if ( event.key == pygame.K_SPACE ) :
                    if score < 6 :
                        __init__()
                        runGame()
                    elif score >= 6 and score < 11 :
                        __init__()
                        score = 6
                        runGame2()
                    elif score >= 11 and score < 20 :
                        __init__()
                        score = 11
                        runGame3()
                elif ( event.key == pygame.K_DOWN ) :
                    __init__()
                    pygame.mixer.music.load( 'opening.wav' )
                    pygame.mixer.music.play( -1 ) # 배경음악재생
                    main()
                elif event.key == pygame.K_ESCAPE :
                    pygame.quit()
                    
        gamePad.fill((0, 0, 0))
        textpos.center = ( padWidth / 2, 95)

        gamePad.blit( text1, textpos )
        gamePad.blit(gameoverImage, (355, 160))
        
        if gamePad.blit(gameoverImage, (355, 160)):
            gamePad.blit( text2, (100,250) )
            gamePad.blit( text3, (100,300) )
            gamePad.blit( text4, (780,250) )
            gamePad.blit( text5, (820,300) )
            
            if pygame.time.get_ticks() - start_ticks >= 4000 and pygame.time.get_ticks() % 1500 < 750:
                gamePad.blit( text6, (80, 400) )
                gamePad.blit( text7, (800, 400) )

        pygame.display.update()
        elapsed_time += clock.tick(60)

# 오프닝 후 메인 화면 구현
def main():
    
    global gamePad, clock, BLACK
                  
    mainImage = pygame.image.load('space.png')
    earthImage = pygame.image.load('earth.png')
    textfont1 = pygame.font.Font('NanumGothic.ttf', 60)
    textfont2 = pygame.font.Font('NanumGothic.ttf', 80)
    textfont3 = pygame.font.Font('NanumGothic.ttf', 35)
    text1 = textfont1.render("지구를 지켜라", True, (255, 0, 0))
    text2 = textfont2.render("냥냥", True, (255, 0, 0))
    text3 = textfont3.render("아무키나 누르면 게임이 시작됩니다", True, (255, 255, 0))
    text4 = textfont3.render("SPACE : 미사일", True, (255, 255, 255))
    text5 = textfont3.render("Q : 필살기", True, (255, 255, 255))
    text6 = textfont3.render("방향키 : 이동", True, (255, 255, 255))

    earthImage_x = 540
    earthImage_y = 640
    
    start_ticks = pygame.time.get_ticks()
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if earthImage_y > 0:
            earthImage_y -= 3
            
        if earthImage_y <= 320:
            earthImage_y = 320
        
        gamePad.blit(mainImage, (0,0))
        gamePad.blit(earthImage, (earthImage_x - earthImage.get_width()/2, earthImage_y - earthImage.get_height()/2))
        
        #텍스트 출력
        if earthImage_y == 320:
            gamePad.blit(text1, (370, 200))
            gamePad.blit(text2, (465, 350))
        if pygame.time.get_ticks() - start_ticks >= 4000 and pygame.time.get_ticks() % 1500 < 750:
            gamePad.blit(text3, (285, 550))
            
        pygame.display.update()
        clock.tick(60)
        

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                gamePad.fill( BLACK )
                gamePad.blit( text4, ( 400, 150 ) )
                gamePad.blit( text5, ( 400, 300 ) )
                gamePad.blit( text6, ( 400, 450 ) )
                pygame.display.update()
                clock.tick(60)
                time.sleep(5)
                __init__()
                runGame()

def setText() :
    global gamePad
                  
    textfont = pygame.font.Font( 'NanumGothic.ttf', 20 ) # 이름, 크기, bold, italic
    gamePad.blit( textfont.render( f'score : {score}', True, ( 0, 255, 0 ) ), ( 10, 10, 0, 0 ) )
    gamePad.blit( textfont.render( f'passed : {passed}', True, ( 255, 0, 0 ) ), ( 150, 10, 0, 0 ) )

def timeDelay500ms() :
    global time_delay_100ms
                  
    if time_delay_100ms > 100 :
        time_delay_100ms = 0
        return True
    
    time_delay_100ms += 1
    return False

def __init__() :
    
    global BLACK, isActive, padWidth, padHeight, move, missileXY, time_delay_100ms, score, \
        passed, isGameOver, monsterSpeed, gamePad, background1, background2, background3, background4, background5, background6, player, \
            recPlayer, playerSize, playerWidth, playerHeight, monster, recMonster, monsterSize, \
                monsterWidth, monsterHeight, missile, recMissile, explosion, missileSound, gameOverSound, \
                  boomSound, clock, missileWidth, missileHeight, background1_x, background2_x, \
                      Rect, monster2, monster3, isBoom, explosionSound
    
    #1. 변수 초기화
    BLACK = ( 0, 0, 0 )
    
    isActive = True
    padWidth = 1080
    padHeight = 640
    move = Rect( 0, 0, 0, 0 )
    missileXY = []
    time_delay_100ms = 0
    score = 0

    passed = 0
    isGameOver = False
    isBoom = True
    monsterSpeed = 2
    
    
    #2. 스크린 생성
    pygame.init()
    
    
    gamePad = pygame.display.set_mode( ( padWidth, padHeight ) )
    
    pygame.display.set_caption('PyShooting')
    background1 = pygame.image.load( 'background1.png' )
    background2 = background1.copy()
    background3 = pygame.image.load( 'background2.png' )
    background4 = background3.copy()
    background5 = pygame.image.load( 'background3.png' )
    background6 = background5.copy()
    background1_x = 0
    background2_x = 1080
    
    
    #3. player 생성
    player = pygame.image.load( 'cat.png' )
    recPlayer = player.get_rect()
    playerSize = recPlayer.size
    playerWidth = playerSize[ 0 ]
    playerHeight = playerSize[ 1 ]
    recPlayer.x = ( padWidth * 0.05 )
    recPlayer.y = ( padHeight * 0.5 )
    
    
    #4. monster 생성
    
    monster = [ pygame.image.load( 'monster1.png' ) for k in range ( 10 ) ]
    recMonster = [ None for k in range( len( monster ) ) ]
    monsterSize = [ None for k in range( len( monster ) ) ]
    for k in range( len( monster ) ) :
    #monster = pygame.transform.scale( monster, ( 20, 20 ) )
        recMonster[ k ] = monster[ k ].get_rect()
        monsterSize[ k ] = recMonster[ k ].size
        monsterWidth = monsterSize[ k ][ 0 ]
        monsterHeight = monsterSize[ k ][ 1 ]
        recMonster[ k ].x = padWidth + 1
        
    monster2 = [ pygame.image.load( 'monster2.png' ) for k in range ( 10 ) ]
    recMonster = [ None for k in range( len( monster2 ) ) ]
    monsterSize = [ None for k in range( len( monster2 ) ) ]
    for k in range( len( monster2 ) ) :
    #monster = pygame.transform.scale( monster, ( 20, 20 ) )
        recMonster[ k ] = monster[ k ].get_rect()
        monsterSize[ k ] = recMonster[ k ].size
        monsterWidth = monsterSize[ k ][ 0 ]
        monsterHeight = monsterSize[ k ][ 1 ]
        recMonster[ k ].x = padWidth + 1
        
    monster3 = [ pygame.image.load( 'monster3.png' ) for k in range ( 10 ) ]
    recMonster = [ None for k in range( len( monster3 ) ) ]
    monsterSize = [ None for k in range( len( monster3 ) ) ]
    for k in range( len( monster3 ) ) :
    #monster = pygame.transform.scale( monster, ( 20, 20 ) )
        recMonster[ k ] = monster[ k ].get_rect()
        monsterSize[ k ] = recMonster[ k ].size
        monsterWidth = monsterSize[ k ][ 0 ]
        monsterHeight = monsterSize[ k ][ 1 ]
        recMonster[ k ].x = padWidth + 1
        
    
    #5. missile 생성
    missile = [ pygame.image.load("cat_missile.png") for k in range( 500 ) ]
    recMissile = [ None for k in range( len( missile) ) ]
    missileSize = [ None for k in range( len (missile) ) ]
    for k in range( len( missile ) ):
        recMissile[k] = missile[k].get_rect()
        missileSize[ k ] = recMissile[ k ].size
        missileWidth = missileSize[ k ][ 0 ]
        missileHeight = missileSize[ k ][ 1 ]
        recMissile[k].x = -1
    
    #6. 폭발 이미지 생성
    explosion = pygame.image.load( 'explosion.png' )
    
    #6. Sound 생성
    missileSound = pygame.mixer.Sound( 'missile.wav' )
    gameOverSound = pygame.mixer.Sound( 'gameover.wav' )
    boomSound = pygame.mixer.Sound( 'boom.wav' )
    explosionSound = pygame.mixer.Sound( 'explosion.wav' ) 
    
    #6. 기타
    clock = pygame.time.Clock()
    ###반복###
    
def runGame() :
    global BLACK, gamePad, clock
    pygame.mixer.music.stop()
    pygame.mixer.music.load( 'music1.wav' )
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play( -1 ) # 배경음악재생
    textfont = pygame.font.Font( 'NanumGothic.ttf', 60 )
    text1 = textfont.render("Stage1", True, (255, 0, 0))
    textpos = text1.get_rect()
    textpos.center = ( padWidth / 2, padHeight / 2 )
    gamePad.fill( BLACK )
    gamePad.blit(text1, textpos )
    pygame.display.update()
    time.sleep(2)
    __init__()
    while isActive :
        #1. 화면 지움
        gamePad.fill( BLACK )
        back()
        #2. 이벤트 처리
        eventProcess()
        #3. player 이동
        movePlayer()
        #4. monster 생성 및 이동
        moveMonster( monster )
        #5. missile 생성 및 이동
        moveMissile()
        #6. 충돌 확인
        CheckCollision()
        CheckCollisionMissile()
        #7. text 업데이트
        setText() 
        #8. 화면 갱신
        pygame.display.flip()
        clock .tick( 60 )
    ###반복###
    pygame.qiuit()

def runGame2() :
    global BLACK, gamePad, clock, score, monsterSpeed
    pygame.mixer.music.stop()
    pygame.mixer.music.load( 'music2.wav' )
    pygame.mixer.music.set_volume(1.2)
    pygame.mixer.music.play( -1 ) # 배경음악재생
    textfont = pygame.font.Font( 'NanumGothic.ttf', 60 )
    text1 = textfont.render("Stage2", True, (255, 0, 0))
    textpos = text1.get_rect()
    textpos.center = ( padWidth / 2, padHeight / 2 )
    gamePad.fill( BLACK )
    gamePad.blit(text1, textpos )
    pygame.display.update()
    time.sleep(2)
    __init__()
    score = 6
    monsterSpeed = 4
    
    while isActive :
        #1. 화면 지움
        gamePad.fill( BLACK )
        back2()
        #2. 이벤트 처리
        eventProcess()
        #3. player 이동
        movePlayer()
        #4. monster 생성 및 이동
        moveMonster( monster2 )
        #5. missile 생성 및 이동
        moveMissile()
        #6. 충돌 확인
        CheckCollision()
        CheckCollisionMissile()
        #7. text 업데이트
        setText() 
        #8. 화면 갱신
        pygame.display.flip()
        clock .tick( 60 )
    ###반복###
    pygame.qiuit()

def runGame3() :
    global BLACK, gamePad, clock, score, monsterSpeed
    pygame.mixer.music.stop()
    pygame.mixer.music.load( 'music3.wav' )
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play( -1 ) # 배경음악재생
    textfont = pygame.font.Font( 'NanumGothic.ttf', 60 )
    text1 = textfont.render("Stage3", True, (255, 0, 0))
    textpos = text1.get_rect()
    textpos.center = ( padWidth / 2, padHeight / 2 )
    gamePad.fill( BLACK )
    gamePad.blit(text1, textpos )
    pygame.display.update()
    time.sleep(2)
    __init__()     
    score = 11
    monsterSpeed = 6
    
    while isActive :
        #1. 화면 지움
        gamePad.fill( BLACK )
        back3()
        #2. 이벤트 처리
        eventProcess()
        #3. player 이동
        movePlayer()
        #4. monster 생성 및 이동
        moveMonster( monster3 )
        #5. missile 생성 및 이동
        moveMissile()
        #6. 충돌 확인
        CheckCollision()
        CheckCollisionMissile()
        #7. text 업데이트
        setText() 
        #8. 화면 갱신
        pygame.display.flip()
        clock .tick( 60 )
    ###반복###
    pygame.qiuit()    

    
__init__()
showOpening()


