from datetime import datetime
import sys

ResetAll = "\033[0m"

Bold = "\033[1m"
Dim = "\033[2m"
Underlined = "\033[4m"
Blink = "\033[5m"
Reverse = "\033[7m"
Hidden = "\033[8m"

ResetBold = "\033[21m"
ResetDim = "\033[22m"
ResetUnderlined = "\033[24m"
ResetBlink = "\033[25m"
ResetReverse = "\033[27m"
ResetHidden = "\033[28m"

Default = "\033[39m"
Black = "\033[30m"
Red = "\033[31m"  # Fatal
Green = "\033[32m"
Yellow = "\033[33m"  # Debug
Blue = "\033[34m"
Magenta = "\033[35m"
Cyan = "\033[36m"  # Info
LightGray = "\033[37m"
DarkGray = "\033[90m"
LightRed = "\033[91m"
LightGreen = "\033[92m"
LightYellow = "\033[93m"  # LightYellow
LightBlue = "\033[94m"
LightMagenta = "\033[95m"
LightCyan = "\033[96m"
White = "\033[97m"

BackgroundDefault = "\033[49m"
BackgroundBlack = "\033[40m"
BackgroundRed = "\033[41m"
BackgroundGreen = "\033[42m"
BackgroundYellow = "\033[43m"
BackgroundBlue = "\033[44m"
BackgroundMagenta = "\033[45m"
BackgroundCyan = "\033[46m"
BackgroundLightGray = "\033[47m"
BackgroundDarkGray = "\033[100m"
BackgroundLightRed = "\033[101m"
BackgroundLightGreen = "\033[102m"
BackgroundLightYellow = "\033[103m"
BackgroundLightBlue = "\033[104m"
BackgroundLightMagenta = "\033[105m"
BackgroundLightCyan = "\033[106m"
BackgroundWhite = "\033[107m"


class logLevel:
	Info = 0x1
	Fatal = 0x2
	Warn = 0x4
	Debug = 0x8
	Verbose = 0x10


_fatal = Red
_debug = Yellow
_info = Cyan
_warn = LightYellow

LogLevel = logLevel.Info | logLevel.Debug | logLevel.Fatal | logLevel.Warn

_out = sys.stdout


def formated_time():
	return '[{0:%Y-%m-%d %H:%M:%S}]'.format(datetime.now())


def colored_text(color, content):
	return color + content + ResetAll;


def prefix(color, content):
	return colored_text(color, f'[{content}]') + formated_time()


def info(content):
	if LogLevel & logLevel.Info != logLevel.Info:
		return
	print(prefix(_info, 'INFO') + str(content), file=_out)


def warn(content):
	if LogLevel & logLevel.Warn != logLevel.Warn:
		return
	print(prefix(_warn, 'WARN') + str(content), file=_out)


def fatal(content):
	if LogLevel & logLevel.Fatal != logLevel.Fatal:
		return
	print(prefix(_fatal, 'FATA') + str(content), file=_out)


def debug(content):
	if LogLevel & logLevel.Debug != logLevel.Debug:
		return
	print(prefix(_debug, 'DBUG') + str(content), file=_out)
