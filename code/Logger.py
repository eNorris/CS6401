
import datetime

class Logger(object):

    logfile = None
    evalcount = 0
    logtime = None

    def __init__(self):
        pass

    @staticmethod
    def initialize(filename):
        Logger.logfile = open(filename, 'w')
        Logger.logtime = datetime.datetime.now()

    @staticmethod
    def write_indiv(indiv):
        pass

    @staticmethod
    def write_eval(team, fitness):
        Logger.evalcount += 1
        Logger.logfile.write("E: " + str(Logger.evalcount) + "  (" + str(datetime.datetime.now() - Logger.logtime) + ")\n")
        Logger.logfile.write("X: " + str(team[0]) + "\n")
        Logger.logfile.write("Y: " + str(team[1]) + "\n")
        Logger.logfile.write("Z: " + str(team[2]) + "\n")
        Logger.logfile.write("F: " + fitness.detail_string() + "\n")

    @staticmethod
    def finish():
        Logger.logfile.close()
