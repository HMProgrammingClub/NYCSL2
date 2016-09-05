#pragma once

#include <iostream>
#include <vector>
#include <ctype.h>
#include <sstream>
#include <algorithm>

#define NORTH 0
#define EAST 1
#define SOUTH 2
#define WEST 3

#define UNKNOWN 0
#define EMPTY 1
#define WALL 2
#define GLASS 3
#define GOAL 4
#define PLAYER 5

typedef std::vector< std::vector<int> > Maze;
static std::istream & operator>>(std::istream & i, Maze & m) {
    std::string str;
    char c;
    do {
        c = i.get();
        if(!isspace(c)) throw 0;
    } while(c != '[');
    int sq_br_cntr = 1, vrt_cntr = 0;
    do {
        c = i.get();
        if(c == '[') {
            sq_br_cntr++;
            vrt_cntr++;
            str.push_back(' ');
        }
        else if(c == ']') {
            sq_br_cntr--;
            str.push_back(' ');
        }
        else if(c == ',') str.push_back(' ');
        else if(isdigit(c)) str.push_back(c);
        else if(!isspace(c)) throw 0;
    } while(sq_br_cntr > 0);
    m.resize(vrt_cntr);
    int wdth = std::count(str.begin(), str.end(), ' ') / vrt_cntr;
    std::stringstream strstrm(str);
    for(auto a = m.begin(); a != m.end(); a++) {
        a->resize(wdth);
        for(auto b = a->begin(); b != a->end(); b++) strstrm >> *b;
    }
    return i;
}
