import keyboard, pyautogui

KEYBOARD_KEY_LIST = {
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "W",
    "X",
    "Y",
    "Z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "/",
    "*",
    "-",
    "+",
    ".",
    "?",
    "}",
    "]",
    "[",
    "{",
    "=",
    "|",
    "!",
    "@",
    "#",
    "$",
    "%",
    "&",
    "(",
    ")",
    "_",
}

def keyboardIsActive() :
    keyPressed = None
    for key in KEYBOARD_KEY_LIST :
        if keyboard.is_pressed(key):
            keyPressed = key
            break
    return keyPressed

def altTab(tabs=1) :
    pyautogui.keyDown('alt')
    for _ in range(tabs) :
        pyautogui.press('tab')
    pyautogui.keyUp('alt')
    pyautogui.keyUp('enter')

def ctrlV() :
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('enter')

def esc() :
    pyautogui.press('esc')
