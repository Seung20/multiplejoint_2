# Draw a robot arm with multiple joints, controlled with keyboard inputs
#
# -*- coding: utf-8 -*- 

import pygame
import numpy as np
from pygame.locals import *
import os

# 게임 윈도우 크기
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (200, 0 ,0)
GREEN = (0, 200, 0)



def Rmat(deg):
    radian = np.deg2rad(deg)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array( [[ c, -s, 0], [s, c, 0], [0, 0, 1] ] )
    return R

def FRmat():
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array( [[ c, -s, 0], [s, c, 0], [0, 0, 1] ] )
    return R


def Tmat(a,b):
    H = np.eye(3)
    H[0,2] = a
    H[1,2] = b
    return H


# Pygame 초기화
pygame.init()

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')


sound_1 = pygame.mixer.Sound(os.path.join(assets_path, 'fizzle.mp3'))
sound_2= pygame.mixer.Sound(os.path.join(assets_path, 'fizzle_2.mp3'))

# 윈도우 제목
pygame.display.set_caption("Drawing")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

# 게임 종료 전까지 반복
done = False
# 폰트 선택(폰트, 크기, 두껍게, 이탤릭)
font = pygame.font.SysFont('FixedSys', 50, True, False)
font_2 = pygame.font.SysFont("Arial", 20, True, False)
# poly: 4 x 3 matrix
poly = np.array( [[0, 0, 1], [100, 0, 1], [100, 20, 1], [0, 20, 1]])
poly_2 = np.array([[0, 0, 1], [20, 0, 1], [20, 50, 1], [0, 50, 1]])
poly_3 = np.array([[0, 0, 1], [40, 0, 1], [40, 10, 1], [0, 10, 1]])



poly = poly.T # 3x4 matrix 
poly_2 = poly_2.T
poly_3 = poly_3.T

cor_1 = np.array([10, 10, 1])
cor_2 = np.array([10,5,1])

degree = 300

joint_1 = 300
joint_2 = 300
joint_3 = 300



#x는 로봇의 degree를 움직이기 위한 변수
x = 0
#x_a는 로봇의 전체 x 좌표를 움직이기 위한 변수
x_a = 0


x_i = 0
x_ii = 0
x_iii = 0

y_b= 600

#x_f 는 로봇의 x좌표
x_f = 300

a = True
b = False

# 게임 반복 구간
while not done:
# 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #방향키 상하는 각각 각도 조절, 좌우는 로봇 전체의 x좌표 움직임
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                x += 1
                a = True
                b = False
            #a,b,c는 각도를 +시계방향으로, p, q, r은 각도를 -반시계방향으로 감소하게끔 만들었다.
            if event.key == pygame.K_a:
                x_i+= 1
                sound_2.play()
            if event.key == pygame.K_b:
                x_ii+= 1
                sound_2.play()
            if event.key == pygame.K_c:
                x_iii+= 1
                sound_2.play()
            if event.key == pygame.K_p:
                x_i -= 1
                sound_2.play()
            if event.key == pygame.K_q:
                x_ii -= 1
                sound_2.play()
            if event.key == pygame.K_r:
                x_iii -= 1
                sound_2.play()

            if event.key == pygame.K_LEFT:
                x_a -= 5
            if event.key == pygame.K_RIGHT:
                x_a += 5
            

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_2:
                x=0 
                b = True
                a = False


            if event.key == pygame.K_a:
                x_i= 0
            if event.key == pygame.K_b:
                x_ii= 0
            if event.key == pygame.K_c:
                x_iii= 0
            if event.key == pygame.K_p:
                x_i = 0
            if event.key == pygame.K_q:
                x_ii = 0
            if event.key == pygame.K_r:
                x_iii = 0
            if event.key == pygame.K_LEFT:
                x_a=0
            if event.key == pygame.K_RIGHT:
                x_a= 0

# 윈도우 화면 채우기
    screen.fill(WHITE)

    if 265 <= (joint_1 + x) <= 359:
        joint_1 += x
        joint_2 += x
        joint_3 += x
        if (joint_1+x) == 359:
            x*=-1
        if (joint_1+x) == 265:
            x*=-1
    else:
        joint_1 -= x
        joint_2 -= x
        joint_3 -= x

    joint_1 += x_i
    joint_2 += x_ii
    joint_3 += x_iii

    #로봇의 x좌표 움직이기
    x_f += x_a

    #1을 눌렀을 때와 2를 눌렀을
    if a:
        H = Tmat(x_f, y_b) @ Tmat(10, 10) @ Rmat(joint_1) @ Tmat(-10, -10)
        K = H @ Tmat(80,0) @ Tmat(10, 10) @ Rmat(joint_2) @ Tmat(-10, -10)
        T = K @ Tmat(80,0) @ Tmat(10, 10) @ Rmat(joint_3) @ Tmat(-10, -10)
    if b:
        H = Tmat(x_f, y_b) @ Tmat(10, 10) @ Rmat(joint_1) @ Tmat(-10, -10)
        K = H @ Tmat(80,0) @ Tmat(10, 10) @Rmat(joint_2) @ Tmat(-10, -10)
        T = K @ Tmat(80,0) @ Tmat(10, 10) @Rmat(joint_3) @ Tmat(-10, -10)

    

    #로봇 arm의 끝, 손 부분
    L = T @ Tmat(80,-15)
    A = T @ Tmat(80, 35)
    AA = T @ Tmat(80, -25)
    
    
    # print(Tmat(300,600))
    
    #로봇 arm의 마디
    corp = H @ cor_1
    corp_2 = K @ cor_1
    corp_3 = T @ cor_1


    #arm의 끝부분 손의 마디
    corp_7 = A @ cor_2
    corp_8 = AA @ cor_2

    


    pp = H @ poly
    pp_2 = K @ poly
    pp_3 = T @ poly

    HH_1 = L @ poly_2
    HR = A @ poly_3
    HH_3 = AA @ poly_3

    q = pp[0:2, :].T # N x 2 matrix
    r = pp_2[0:2, :].T
    s = pp_3[0:2, :].T

    v = HH_1[0:2, :].T
    w = HR[0:2, :].T
    y = HH_3[0:2, :].T
   

    # print(pp.shape, pp, pp.T )
    # pygame.draw.polygon(screen, RED, [300,650], 4)
   
    
    
    if a:
        pygame.draw.polygon(screen, RED, [[(x_f)-10,600],[(x_f)-10, 699], [(x_f)+30,699], [(x_f)+30, 600]], 4)
        pygame.draw.polygon(screen, RED, q, 4)
        pygame.draw.polygon(screen, RED, r, 4)
        pygame.draw.polygon(screen, RED, s, 4)
        pygame.draw.polygon(screen, RED, v, 4)
        pygame.draw.polygon(screen, RED, w, 4)
        pygame.draw.polygon(screen, RED, y, 4)
    
    if b:
        pygame.draw.polygon(screen, GREEN, [[(x_f)-10,600],[(x_f)-10, 699], [(x_f)+30,699], [(x_f)+30, 600]], 4)
        pygame.draw.polygon(screen, GREEN, q,4)
        pygame.draw.polygon(screen, GREEN, r,4)
        pygame.draw.polygon(screen, GREEN, s,4)
        pygame.draw.polygon(screen, GREEN, v,4)
        pygame.draw.polygon(screen, GREEN, w,4)
        pygame.draw.polygon(screen, GREEN, y,4)

    #바퀴
    pygame.draw.circle(screen, GREY, [(x_f)-10, 690], 10)
    pygame.draw.circle(screen, GREY, [(x_f)+30, 690], 10)




    pygame.draw.circle(screen, (0, 0, 0), corp[:2], 3)
    pygame.draw.circle(screen, (0, 0, 0), corp_2[:2], 3)
    pygame.draw.circle(screen, (0, 0, 0), corp_3[:2], 3)
    pygame.draw.circle(screen, (0, 0, 0), corp_7[:2], 3)
    pygame.draw.circle(screen, (0, 0, 0), corp_8[:2], 3)

    # print(corp[:2])

    
    text = font.render("Robot arm", True, BLACK)
    text_1 = font_2.render("Press 1 for automatic mode", True, RED)
    text_2 = font_2.render("Press 2 for passive mode", True, GREEN)
    text_3 = font_2.render("a,b,c are +degree for joints 1, 2, 3", True, BLACK)
    text_4 = font_2.render("p,q,r are -degree for joints 1, 2, 3", True, BLACK)


    screen.blit(text, [WINDOW_WIDTH/2-70, 0])
    screen.blit(text_1, [0,100])
    screen.blit(text_2, [0,120])
    screen.blit(text_3, [0,140])
    screen.blit(text_4, [0,160])

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)  

# 게임 종료
pygame.quit()