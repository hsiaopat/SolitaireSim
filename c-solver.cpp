#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <filesystem>
#include <iostream>
#include <algorithm>
#include <ctime>      
#include <cstdlib>      
#include <random>
#include <sstream>

class Board {
    public:
        Board();
        Board(std::string game_state);
        Board(Board &board_to_copy);
        void print_board();
        std::string card_to_string(int card);
        std::string board_to_string();
        std::vector<int> m_deck;
        std::vector<std::vector<int>> m_tableau;
        std::vector<std::vector<int>> m_finished;
        std::vector<std::vector<bool>> m_hidden;
        std::vector<int> num_hidden;
        bool is_move_valid(int from_pos, int to_pos);
        bool is_tableau_move_valid(int from_pos, int from_depth, int to_pos, int to_depth);
        void perform_move(int from_pos, int to_pos);
        void perform_tableau_move(int from_pos, int from_depth, int to_pos, int to_depth);
        void draw_card();
        int m_deck_position;
        std::vector<std::string> previous_moves;
};

std::unordered_set<std::string> visited_boards = {};
bool are_cards_stackable(int current_card, int dest_card);
Board winning_board;
int dead_ends = 0;

Board::Board() {

}

Board::Board(std::string game_state) {
    std::vector<int> cards;
    std::string current_card = "  ";
    previous_moves = {};
    for (int i = 2; i <= 104; i+=2) {
        current_card[0] = game_state[i];
        current_card[1] = game_state[i + 1];
        cards.push_back(std::stoi(current_card));
    }
    for (int i = 0; i < 7; i++) {
        m_tableau.push_back(std::vector<int>());
        m_hidden.push_back(std::vector<bool>());
        num_hidden.push_back(i);
    }
    for (int i = 0; i < 4; i++) {
        m_finished.push_back(std::vector<int>());
    }

    int card_index = cards.size() - 1;

    for (int i = 0; i < 7; i++) {
        for (int j = i; j < 7; j++) {
            m_tableau[j].push_back(cards[card_index]);
            m_hidden[j].push_back(true);
            card_index--;
        }
        m_hidden[i][i] = false;
        
    }

    for (int i = 0; i < 24; i++) {
        m_deck.push_back(cards[i]);
    }

    m_deck_position = m_deck.size();
}

Board::Board(Board &board_to_copy) {
    m_deck = board_to_copy.m_deck;
    num_hidden = board_to_copy.num_hidden;

    for (int i = 0; i < 7; i++) {
        m_tableau.push_back(std::vector<int>());
        m_hidden.push_back(std::vector<bool>());
        m_tableau[i] = board_to_copy.m_tableau[i];
        m_hidden[i] = board_to_copy.m_hidden[i];
    }

    for (int i = 0; i < 4; i++) {
        m_finished.push_back(std::vector<int>());
        m_finished[i] = board_to_copy.m_finished[i];
    }
    m_deck_position = board_to_copy.m_deck_position;
    previous_moves = board_to_copy.previous_moves;
}

std::string Board::card_to_string(int card) {
    std::string card_str = "  ";
    if (card / 4 == 0) {
        card_str[0] = 'A';
    }
    else if (card / 4 == 9) {
        card_str[0] = 'T';
    }
    else if (card / 4 == 10) {
        card_str[0] = 'J';
    }
    else if (card / 4 == 11) {
        card_str[0] = 'Q';
    }
    else if (card / 4 == 12) {
        card_str[0] = 'K';
    }
    else {
        card_str[0] = std::to_string(card / 4 + 1)[0];
    }

    if (card % 4 == 0) {
        card_str[1] = 'C';
    }
    else if (card % 4 == 1) {
        card_str[1] = 'D';
    }
    else if (card % 4 == 2) {
        card_str[1] = 'H';
    }
    else if (card % 4 == 3) {
        card_str[1] = 'S';
    }
    return card_str;
}

void Board::print_board() {
    printf("Deck: ");
    for (int i = 0; i < m_deck.size(); i++) {
        printf("%s ", card_to_string(m_deck[i]).c_str());
        if (i == m_deck_position - 1) {
            printf("|");
        }
    }
    printf("\n");

    int max_size = 0;
    for (int i = 0; i < 7; i++) {
        max_size = max_size > m_tableau[i].size() ? max_size : m_tableau[i].size();
    }

    printf("Tableau:\n");
    for (int j = 0; j < max_size; j++) {
        for (int i = 0; i < 7; i++) {
            if (m_tableau[i].size() <= j) {
                printf("     ");
            }
            else {
                if (m_hidden[i][j]) {
                    printf("(%s) ", card_to_string(m_tableau[i][j]).c_str());
                }
                else {
                    printf(" %s  ", card_to_string(m_tableau[i][j]).c_str());
                }
            }
        }
        printf("\n");
    }

    max_size = 0;
    for (int i = 0; i < 4; i++) {
        max_size = max_size > m_finished[i].size() ? max_size : m_finished[i].size();
    }

    printf("Finish piles :\n");
    for (int j = 0; j < max_size; j++) {
        for (int i = 0; i < 4; i++) {
            if (m_finished[i].size() <= j) {
                printf("   ");
            }
            else {
                printf("%s ", card_to_string(m_finished[i][j]).c_str());
            }
        }
        printf("\n");
    }
    printf("\n");
}

std::string Board::board_to_string() {
    std::string board_string;
    std::vector<std::vector<int>> tableau_copy;
    for (int i = 0; i < 7; i++) {
        tableau_copy.push_back(std::vector<int>());
        tableau_copy[i] = m_tableau[i];
    }
    std::sort(tableau_copy.begin(), tableau_copy.end(), [](const std::vector<int> & a, const std::vector<int> & b){ return a.size() < b.size(); });
    for (int i = 0; i < m_deck.size(); i++) {
        board_string += card_to_string(m_deck[i]);
        if (i == m_deck_position - 1) {
            board_string += "|";
        }
    }
    if (m_deck_position == m_deck.size()) {
        board_string += "|";
    }

    board_string += "$";


    for (int i = 0; i < 7; i++) {
        for (int j = 0; j < tableau_copy[i].size(); j++) {
            board_string += card_to_string(tableau_copy[i][j]);
        }
        board_string += "|";
    }

    board_string += "$";


    
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < m_finished[i].size(); j++) {
            board_string += card_to_string(m_finished[i][j]);
        }
        board_string += "|";
    }

    return board_string;
}

bool are_cards_stackable(int current_card, int dest_card, bool is_finished_pile) {
    int card_mod = current_card % 4;
    int dest_mod = dest_card % 4;
    
    if (is_finished_pile)
    {
        if (card_mod != dest_mod) {
            return false;
        }
        if ((current_card / 4) == (dest_card / 4 + 1)) {
            return true;
        }
        else {
            return false;
        }
    }
    else {
        if ( (card_mod == 0 || card_mod == 3) && (dest_mod == 1 || dest_mod == 2)) {
            
        }
        else if ( (card_mod == 1 || card_mod == 2) && (dest_mod == 0 || dest_mod == 3)) {
            
        }
        else {
            return false;
        }
        if ((current_card / 4) == (dest_card / 4 - 1)) {
            return true;
        }
        else {
            return false;
        }
    }
}

bool Board::is_move_valid(int from_pos, int to_pos) {
    if (from_pos < 0 || from_pos > 7 || to_pos < 1 || to_pos > 11) {
        printf("Error: is_move_valid %d %d\n", from_pos, to_pos);
        return false;
    }
    int current_card = 0;
    if (from_pos == 0) {
        if (m_deck_position >= m_deck.size()) {
            return false;
        }
        current_card = m_deck[m_deck_position];
    }
    else {
        if (m_tableau[from_pos - 1].size() == 0) {
            return false;
        }
        current_card = m_tableau[from_pos - 1][m_tableau[from_pos - 1].size() - 1];
    }

    bool dest_is_empty = true;
    bool is_dest_finished = false;
    int dest_card = 0;
    if (to_pos > 7) {
        if (m_finished[to_pos - 8].size() > 0) {
            dest_is_empty = false;
            dest_card = m_finished[to_pos - 8][m_finished[to_pos - 8].size() - 1];
            is_dest_finished = true;
        }
        else {
            if ( (current_card / 4 == 0) && ((to_pos - 8) == current_card % 4)) {
                return true;
            }
            else {
                return false;
            }
        }
    }
    
    else {
        if (m_tableau[to_pos - 1].size() > 0) {
            dest_is_empty = false;
            dest_card = m_tableau[to_pos - 1][m_tableau[to_pos - 1].size() - 1];
            is_dest_finished = false;
        }
        else {
            if (current_card >= 48) {
                return true;
            }
            else {
                return false;
            }
        }
    }


        //std::cout << card_to_string(current_card) <<  " " << card_to_string(dest_card) << " " << is_dest_finished << "\n";

        return are_cards_stackable(current_card, dest_card, is_dest_finished);


    return false;
}

bool Board::is_tableau_move_valid(int from_pos, int from_depth, int to_pos, int to_depth){
    if (m_tableau[from_pos].size() <= from_depth) {
        return false;
    }
    
    // todo - add moving stacks
    for (int i = 0; i < from_depth; i++) {
        if (m_hidden[from_pos][m_tableau[from_pos].size() - 2 - i]) {
            return false;
        }
    }
    
    int card_to_move = m_tableau[from_pos][m_tableau[from_pos].size() - 1 - from_depth];

    if (m_tableau[to_pos].size() == 0) {
        if (card_to_move >= 48) {
            return true;
        }
        else {
            return false;
        }
    }

    int dest_card = m_tableau[to_pos][m_tableau[to_pos].size() - 1];

    return are_cards_stackable(card_to_move, dest_card, false);
}

void Board::perform_move(int from_pos, int to_pos) {
    int current_card;
    if (from_pos == 0) {
        current_card = m_deck[m_deck_position];
        m_deck.erase(m_deck.begin() + m_deck_position);
    }
    else {
        current_card = m_tableau[from_pos - 1][m_tableau[from_pos - 1].size() - 1];
        m_tableau[from_pos - 1].pop_back();
        if (m_hidden[from_pos - 1][m_hidden[from_pos - 1].size() - 1] == true) num_hidden[from_pos - 1]--;
        m_hidden[from_pos - 1].pop_back();
        if (m_tableau[from_pos - 1].size() != 0) {
            m_hidden[from_pos - 1][m_hidden[from_pos - 1].size() - 1] = false;
        }
    }

    if (to_pos > 7) {
        m_finished[to_pos - 8].push_back(current_card);
    }
    
    else {
        m_tableau[to_pos - 1].push_back(current_card);
        m_hidden[to_pos - 1].push_back(false);
    }
}

void Board::perform_tableau_move(int from_pos, int from_depth, int to_pos, int to_depth) {
    int current_card = 0;
    for (int i = from_depth; i >= 0; i--) {
        int index = m_tableau[from_pos].size() - 1 - i;
        current_card = m_tableau[from_pos][index];
        m_tableau[from_pos].erase(m_tableau[from_pos].begin() + index);
        if (m_hidden[from_pos][m_hidden[from_pos].size() - 1] == true) num_hidden[from_pos - 1]--;
        m_hidden[from_pos].erase(m_hidden[from_pos].begin() + index);
        
        
        m_tableau[to_pos].push_back(current_card);
        m_hidden[to_pos].push_back(false);
    }
    if (m_tableau[from_pos].size() != 0) {
        m_hidden[from_pos][m_hidden[from_pos].size() - 1] = false;
    }
}

void Board::draw_card() {
    m_deck_position--;
    if (m_deck_position < 0) {
        m_deck_position = m_deck.size();
    }
}

bool recursive_solver(Board &current_board, int consecutive_draws, int consecutive_moves) {
    if (consecutive_draws > current_board.m_deck.size()) {
        dead_ends++;
        return false;
    }

    std::string current_board_string = current_board.board_to_string();
    if (visited_boards.find(current_board_string) != visited_boards.end()) {
        return false;
    }
    visited_boards.insert(current_board_string);
    //current_board.print_board();

    int cards_left = current_board.m_deck.size();
    for (int i = 0; i < 7; i++) {
        cards_left += current_board.m_tableau[i].size();
    }
    if (cards_left <= 0) {
        winning_board = current_board;
        return true;
    }
    if (dead_ends >= 500) {
        return false;
    }
    //current_board.previous_moves.push_back(current_board_string);
    for (int i = 0; i < 8; i++) {
        for (int j = 8; j < 12; j++) {
            //printf("Attempting Moving from %d to %d\n", i, j);
            if (current_board.is_move_valid(i, j)) {
                Board new_board(current_board);
                new_board.perform_move(i, j);
                std::ostringstream move;
                move << i << " " << j << " -1";
                new_board.previous_moves.push_back(move.str());
                //printf("Moving from %d to %d\n", i, j);
                if (recursive_solver(new_board, 0, consecutive_moves + 1)) {
                    return true;
                }
            }
        }
    }
    // move cards from one tableau to another
    for (int i = 0; i < 7; i++) {
        current_board.num_hidden[i] = 0;
        for (int j = 0; j < current_board.m_hidden[i].size(); j++) {
            if(current_board.m_hidden[i][j]) current_board.num_hidden[i]++;
        }
    }
    for (int i = 0; i < 7; i++) {
        int k = current_board.m_tableau[i].size() - current_board.num_hidden[i] - 1;
        //for (int k = current_board.m_tableau[i].size() - current_board.num_hidden[i] - 1; k >= 0; k--) {
            for (int j = 0; j < 7; j++) {
            
                if (current_board.is_tableau_move_valid(i, k, j, 0)) {
                    Board new_board(current_board);
                    new_board.perform_tableau_move(i, k, j, 0);
                    std::ostringstream move;
                    move << i + 1<< " " << j + 1 << " " << k;
                    new_board.previous_moves.push_back(move.str());
                    //printf("Moving from %d to %d, %d deep\n", i, j, k);
                    if (recursive_solver(new_board, 0, consecutive_moves + 1)) {
                        return true;
                    }
                }
            }
        //}
    }
    // move draw card to tableau
    for (int i = 0; i < 1; i++) {
        for (int j = 1; j < 8; j++) {
            if (current_board.is_move_valid(i, j)) {
                Board new_board(current_board);
                new_board.perform_move(i, j);
                std::ostringstream move;
                move << i << " " << j << " -1";
                new_board.previous_moves.push_back(move.str());
                //printf("Moving from %d to %d\n", i, j);
                if (recursive_solver(new_board, 0, consecutive_moves + 1)) {
                    return true;
                }
            }
        }
    }
    // draw from pile
    Board new_board(current_board);
    new_board.draw_card();
    new_board.previous_moves.push_back("-1 -1 -1");
    //printf("Draw\n");
    if (recursive_solver(new_board, consecutive_draws + 1, consecutive_moves + 1)) {
        return true;
    }
    return false;
}

std::string get_cheat_filename() {
    std::string cheat_file_path = ".";
    std::string cheat_file_name;
    time_t youngest_time = 0;
    for (const auto & entry : std::filesystem::directory_iterator(cheat_file_path)) {
        std::string path = entry.path().string();
        if (path.length() == 106) {
            struct stat t_stat;
            stat(path.c_str(), &t_stat);
            if (t_stat.st_ctime > youngest_time) {
                youngest_time = t_stat.st_ctime;
                cheat_file_name = path;
            }
        }
    }
    return cheat_file_name;
}

std::string generate_cheat_file() {
    std::vector<int> deck;
    for (int i = 0; i < 52; i++) {
        deck.push_back(i);
    }

    // using built-in random generator:
    std::shuffle(std::begin(deck), std::end(deck), std::random_device());
    
    std::string cheat_file_name = "..";
    for (int i = 0; i < 52; i++) {
        if (deck[i] < 10) {
            cheat_file_name += "0";
        }
        cheat_file_name += std::to_string(deck[i]);
    }

    return cheat_file_name;
}

void test_solver() {
    int ws = 0;
    for (int i = 0; i < 20; i++) {
        std::string cheat_file_name = generate_cheat_file();
        std::cout << cheat_file_name << "\n";
        Board initial_board(cheat_file_name);
        visited_boards = {};
        dead_ends = 0;

        if (recursive_solver(initial_board, 0, 0)) {
            printf("Solution found\n");
            ws++;
        }
        else {
            printf("Nothing found\n");
        }
    }
    printf("%d/20\n", ws);
}

int main() {
    std::string cheat_file_name = get_cheat_filename();
    //cheat_file_name = "..00010203040506070809101112131415161718192021222324252627282930313233343536373839404142434445464748495051";
    //cheat_file_name = "..22254936501229152142262807370648243431080314014705273500331744200245092332105119134143403918113046163804";
    //cheat_file_name = "..28462210274348054720360313264238323945142512412923180050512130161704443401350649081124314015331937020709";
    // test_solver();
    // return 1;

    // cheat_file_name = "..03334119021410442730183532474621172801251539290549130748264022430011082350313404204224090638163651124537";
    Board initial_board(cheat_file_name);
    if (recursive_solver(initial_board, 0, 0)) {
        printf("Solution found\n");
    }
    else {
        printf("Nothing found\n");
        return 0;
    }
    printf("%d %s\n", winning_board.previous_moves.size(), cheat_file_name.c_str());
    FILE *f = fopen("output.txt", "w");
    for (int i = 0; i < winning_board.previous_moves.size(); i++) {
        fprintf(f, "%s\n", winning_board.previous_moves[i].c_str());
    }
    return 0;
}