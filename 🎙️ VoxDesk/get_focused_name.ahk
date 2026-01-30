#NoEnv
#SingleInstance Force
SetBatchLines, -1

#Include Acc.ahk

try {
    hwnd := WinActive("A")
    if !hwnd {
        FileAppend, , *
        ExitApp
    }

    acc := Acc_ObjectFromWindow(hwnd)
    if acc {
        name := acc.accName(0)
        FileAppend, %name%, *
    } else {
        FileAppend, , *
    }
} catch {
    FileAppend, , *
}
ExitApp
