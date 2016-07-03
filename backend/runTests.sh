#!/bin/bash
mongod &
python3 tests.py | python tests.py
