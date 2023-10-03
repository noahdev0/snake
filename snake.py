import math
import random
import cv2
from cvzone import HandDetector, overlayPNG

cap = cv2.VideoCapture(0)
cap.set(3, 800)  # width
cap.set(4, 600)  # height
detector = HandDetector(detectionCon=0.7, maxHands=1)

class SnakeGame:
    def __init__(self, pathFood):
        self.points = []  # Define all snake points
        self.lenght = []  # Distance between each point
        self.currentLenght = 0  # Total length of the snake
        self.allowedLenght = 150  # Maximum allowed length
        self.previousHead = 0, 0  # Previous main point

        self.imageFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imageFood.shape
        self.foodPoints = 0, 0
        self.randomFoodLocation()

        self.score = 0  # Initialize score to 0

    def randomFoodLocation(self):
        self.foodPoints = random.randint(100, 600), random.randint(100, 400)

    def update(self, imgMain, currentHead):
        px, py = self.previousHead
        cx, cy = currentHead
        self.points.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.lenght.append(distance)
        self.currentLenght += distance
        self.previousHead = cx, cy

        # Length reduction
        if self.currentLenght > self.allowedLenght:
            for i, length in enumerate(self.lenght):
                self.currentLenght -= length
                self.lenght.pop(i)
                self.points.pop(i)
                if self.currentLenght < self.allowedLenght:
                    break

        # Food eaten
        rx, ry = self.foodPoints
        if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and ry - self.hFood // 2 < cy < ry + self.hFood // 2:
            self.randomFoodLocation()
            self.allowedLenght += 25
            self.score += 1  # Increment the score when food is eaten

        # Draw worm
        if self.points:
            for i, points in enumerate(self.points):
                if i != 0:
                    cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

        # Draw food
        rx, ry = self.foodPoints
        imgMain = overlayPNG(imgMain, self.imageFood, (rx - self.wFood // 2, ry - self.hFood // 2))

        return imgMain

    def displayScore(self, img):
        cv2.putText(img, f"Score: {self.score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return img

game = SnakeGame('E:/opencv project/project_python/AI snake game/apple.png')
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)

    img = game.displayScore(img)  # Call the displayScore method to render the score

    cv2.imshow("Snake game", img)
    key = cv2.waitKey(1)
