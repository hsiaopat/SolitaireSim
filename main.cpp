#include <windows.h>
#include <stdio.h>
#include <time.h>
#include <fstream>
#include <string>
#include <iostream>
#include <vector>

HWND solitaire_handle;
DWORD movement_time = 20;

void left_click() {
    // set up INPUT struct to indicate a left mouse down click
    INPUT clickInput = {0};
    clickInput.type = INPUT_MOUSE;
    clickInput.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;

    // Send the input
    SendInput(1, &clickInput, sizeof(INPUT));

    Sleep(movement_time);

    // clear INPUT struct
    ZeroMemory(&clickInput, sizeof(INPUT));
    clickInput.type = INPUT_MOUSE;
    clickInput.mi.dwFlags = MOUSEEVENTF_LEFTUP;
    // Send the input
    SendInput(1, &clickInput, sizeof(INPUT));
}

void start_drag() {
    // set up INPUT struct to indicate a left mouse down click
    INPUT clickInput = {0};
    clickInput.type = INPUT_MOUSE;
    clickInput.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;

    // Send the input
    SendInput(1, &clickInput, sizeof(INPUT));

    Sleep(movement_time);
}

void end_drag() {
    // set up INPUT struct to indicate a left mouse down click
    INPUT clickInput = {0};
    clickInput.type = INPUT_MOUSE;
    clickInput.mi.dwFlags = MOUSEEVENTF_LEFTUP;

    // Send the input
    SendInput(1, &clickInput, sizeof(INPUT));

    Sleep(movement_time);
}

void center_mouse_on_deck() {
    RECT rect = {0};
    GetWindowRect(solitaire_handle, &rect);
    
    Sleep(movement_time);

    SetCursorPos(rect.left + 50, rect.top + 100);
}

void center_mouse_on_deck_cards() {
    RECT rect = {0};
    GetWindowRect(solitaire_handle, &rect);
    
    Sleep(movement_time);

    SetCursorPos(rect.left + 160, rect.top + 100);
}

void center_mouse_on_field(int field_number, int tableausize, int hiddensize) {
    RECT rect = {0};
    GetWindowRect(solitaire_handle, &rect);
    
    Sleep(movement_time);
    printf("%d\n", rect.top + 172 + 20 * tableausize + 2 * hiddensize);
    SetCursorPos(rect.left + (field_number * 82) + 50, rect.top + 172 + 20 * tableausize + 2 * hiddensize);
}

void center_mouse_on_tower(int tower_number) {
    tower_number = 3 - tower_number;
    RECT rect = {0};
    GetWindowRect(solitaire_handle, &rect);
    
    Sleep(movement_time);

    SetCursorPos(rect.left + (tower_number * 82) + 320, rect.top + 100);
}

void test_centering() {
    center_mouse_on_deck();
    left_click();
    center_mouse_on_deck_cards();
    start_drag();
    for (int i = 0; i < 7; i++) {
        //center_mouse_on_field(i, 0);
    }
    for (int i = 0; i < 4; i++) {
        center_mouse_on_tower(i);
    }
    Sleep(100);
    end_drag();
}

void deal_new_game() {
    RECT rect = {0};
    GetWindowRect(solitaire_handle, &rect);
    
    Sleep(movement_time);

    SetCursorPos(rect.left + 25, rect.top + 40);
    left_click();
    SetCursorPos(rect.left + 25, rect.top + 60);
    left_click();
    
}

int main(int argc, char* argv[], char* environment[])
{

    //create two structures to hold our Main Window handle
    //and the Button's handle
    
    if (argc == 2) {
        deal_new_game();
        return 0;
    }

    //this window's caption is "File Download", so we search for it's handle using the FindWindow API		
    solitaire_handle = FindWindow(NULL, "Solitaire");

    if (solitaire_handle == NULL) {
        // Handle error: Window not found
        return 1;
    }

    SetForegroundWindow(solitaire_handle);
    SetActiveWindow(solitaire_handle);
    SetFocus(solitaire_handle);

    //test_centering();
    //deal_new_game(); 
    //test_centering();   

    std::ifstream input_file("output.txt");
    std::string line;

    std::vector<int> revealedsizes = {1, 1, 1, 1, 1, 1, 1};
    std::vector<int> hiddensizes = {0, 1, 2, 3, 4, 5, 6};
    while(getline(input_file, line))
    {
        int from, to, depth;
        sscanf(line.c_str(), "%d %d %d\n", &from, &to, &depth);
        depth = max(depth, 0);
        printf("%d %d %d\n", from, to, depth);
        //getchar();
        if (from == -1) {
            Sleep(movement_time);
            center_mouse_on_deck();
            Sleep(movement_time);
            left_click();
            Sleep(movement_time);
            continue;
        }
        
        int cards_moved = 0;

        if (from == 0) {
            center_mouse_on_deck_cards();
            cards_moved = 1;
        }
        else if (from >= 1 && from <= 7 && to <= 7) {
            center_mouse_on_field(from - 1, 0, hiddensizes[from - 1]);
            cards_moved = revealedsizes[from - 1];
            if (hiddensizes[from - 1] == 0) {
                revealedsizes[from - 1] = 0;
            }
            else {
                revealedsizes[from - 1] = 1;
            }
            hiddensizes[from - 1]--;
            if (hiddensizes[from - 1] < 0) hiddensizes[from - 1] = 0;
        }
        else if (from >= 1 && from <= 7 && to > 7) {
            printf("REVEALED %d\n", revealedsizes[from - 1]);
            center_mouse_on_field(from - 1, revealedsizes[from - 1], hiddensizes[from - 1]);
            cards_moved = 1;
            revealedsizes[from - 1]--;
            if (revealedsizes[from - 1] == 0) {
                if (hiddensizes[from - 1] > 0) {
                    revealedsizes[from - 1] = 1;
                    hiddensizes[from - 1]--;
                }
            }
            else {
            }
            if (hiddensizes[from - 1] < 0) hiddensizes[from - 1] = 0;
        }
        else {
            center_mouse_on_tower(from - 8);
        }
        Sleep(movement_time);
        start_drag();
        Sleep(movement_time);

        if (to >= 1 && to <= 7) {
            center_mouse_on_field(to - 1, revealedsizes[to - 1], hiddensizes[to - 1]);
            revealedsizes[to - 1] += cards_moved;
        }
        else if (to > 7) {
            center_mouse_on_tower(to - 8);
        }
        else {
            printf("Error: not good\n");
        }
        Sleep(movement_time);
        end_drag();
        Sleep(movement_time);

        if (from >= 1 && from <= 7) {
            center_mouse_on_field(from - 1, 0, hiddensizes[from - 1]);
            left_click();
        }

        //getchar();
    
    }


    return 0;
}