import sys
import time
import pygame
from pygame.locals import *
from math import sin, cos, radians


class ModelClock:
    """
    Diese Applikation zeigt eine Uhr an. Die Uhrzeit kann analog, aber auch digital angezeigt werden.
    Mit der Taste P ist es Möglich bei der analogen Uhr zwischen der kontinuierlichen oder der
    diskreten Variante zu wechseln.
    Es is ein switchen zwischen Digital und Analog mit der Taste A und D möglich.

    In der Model Klasse dieser Applikation werden wichtige Daten, wie zum Beispiel die Anzeigenart
    (Analog oder Digital), wichtige Koordinaten oder auch Farben gespeichert.

    __version__ = '1.0'
    __author__ = 'Yunus Sari'
    """
    def __init__(self):
        self.isAnalog = True
        self.isSmooth = False
        self.xAxis = 300
        self.yAxis = 300
        self.center = (self.xAxis, self.yAxis)
        "Colors"
        self.background = (220, 220, 220)
        self.secondHand = (150, 80, 80)
        self.minuteHand = (200, 80, 80)
        self.hourHand = (250, 80, 80)
        self.markers = (100, 0, 0)
        self.font = (50, 50, 50)
        pygame.init()

class ViewClockAnalog:
    """
    Diese View-Klasse, dient zur Darstellund der Uhrzeit in analoger Form.

    __version__ = '1.0'
    __author__ = 'Yunus Sari'
    """
    def __init__(self, modelclock):
        self.ModelClock = modelclock
        self.field = pygame.display.set_mode((600, 600))
        self.field.fill(self.ModelClock.background)
        time_save = time.localtime()
        s = time_save.tm_sec
        if self.ModelClock.isSmooth:
            s += (time.time() % 1)
        m = time_save.tm_min
        h = time_save.tm_hour
        if h > 12:
            h -= 12
        hm = (h + m / 60.0) * 5
        pygame.draw.circle(self.field, self.ModelClock.background, self.ModelClock.center, 222)
        pygame.draw.line(self.field, self.ModelClock.hourHand, self.ModelClock.center,
                         (int(self.ModelClock.xAxis + 180 * cos(radians(hm * 6 - 90))),
                          int(self.ModelClock.yAxis + 180 * sin(radians(hm * 6 - 90)))), 6)
        pygame.draw.line(self.field, self.ModelClock.minuteHand, self.ModelClock.center,
                         (int(self.ModelClock.xAxis + 210 * cos(radians(m * 6 - 90))),
                          int(self.ModelClock.yAxis + 210 * sin(radians(m * 6 - 90)))), 3)
        pygame.draw.line(self.field, self.ModelClock.secondHand, self.ModelClock.center,
                         (int(self.ModelClock.xAxis + 220 * cos(radians(s * 6 - 90))),
                          int(self.ModelClock.yAxis + 220 * sin(radians(s * 6 - 90)))), 1)
        for i in range(0, 60, 1):
            pygame.draw.line(self.field, self.ModelClock.markers,
                             (int(self.ModelClock.xAxis + 282 * cos(radians(i * 6 - 90))),
                              int(self.ModelClock.yAxis + 282 * sin(radians(i * 6 - 90)))),
                             (int(self.ModelClock.xAxis + 298 * cos(radians(i * 6 - 90))),
                              int(self.ModelClock.yAxis + 298 * sin(radians(i * 6 - 90)))), 2)
        for i in range(0, 12, 1):
            pygame.draw.circle(self.field, self.ModelClock.markers,
                               (int(self.ModelClock.xAxis + 290 * cos(radians(i * 30 - 90))),
                                int(self.ModelClock.yAxis + 290 * sin(radians(i * 30 - 90)))), 10)
        pygame.display.update()


class ViewClockDigital:
    """
    Diese View-Klasse, dient zur Darstellund der Uhrzeit in digitaler Form.

    __version__ = '1.0'
    __author__ = 'Yunus Sari'
    """
    def __init__(self, modelclock):
        self.ModelClock = modelclock
        self.field = pygame.display.set_mode((600, 600))
        self.field.fill(self.ModelClock.background)
        pygame.init()
        zeit = time.localtime()
        seku = zeit.tm_sec
        minu = zeit.tm_min
        hour = zeit.tm_hour
        if seku < 10:
            seku = "0" + str(seku)
        if minu < 10:
            minu = "0" + str(minu)
        if hour < 10:
            hour = "0" + str(hour)
        pygame.draw.rect(self.field, self.ModelClock.markers, (80, 195, 445, 160), 0)
        pygame.draw.rect(self.field, self.ModelClock.background, (85, 200, 435, 150), 0)
        myfont = pygame.font.SysFont("Arial", 125)
        label = myfont.render(str(hour) + ":" + str(minu) + ":" + str(seku), 1, self.ModelClock.font)
        self.field.blit(label, (100, 210))
        pygame.display.update()


class ControllerClock:
    """
    Die Klasse Controller beinhaltet alle wichtigen Funktionen.
    Hier wurden die Befehle zum Ändern der Anzeigeart, zwischen Analog und Digital, als auch zwischen
    kontinuierlich und diskreter Variante, geschrieben.

    __version__ = '1.0'
    __author__ = 'Yunus Sari'
    """
    def __init__(self, modelclock):
        self.ModelClock = modelclock
        if self.ModelClock.isAnalog:
            ViewClockAnalog(self.ModelClock)
        else:
            ViewClockDigital(self.ModelClock)

    def handleevent(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    sys.exit(0)
                if event.type == KEYDOWN and event.key == K_d:
                    self.ModelClock.isAnalog = False
                if event.type == KEYDOWN and event.key == K_p:
                    self.ModelClock.isSmooth = not self.ModelClock.isSmooth
                if event.type == KEYDOWN and event.key == K_a:
                    self.ModelClock.isAnalog = True
            if self.ModelClock.isAnalog:
                ViewClockAnalog(self.ModelClock)
            else:
                ViewClockDigital(self.ModelClock)
            pygame.display.update()

if __name__ == '__main__':
    ControllerClock(ModelClock()).handleevent()
