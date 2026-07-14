# This file is part of O-positive-test-with-python.
# Copyright (C) 2026 jajhehbreal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from run_lang import run_langu

class Main:
    __slots__ = ('running')
    def __init__(self) -> None:
        self.running = True

    def run(self):
        while self.running:
            user_inputs = input('>>').strip() # the input will be GIVEN to the lexer after LEXING INTO TOKENS we print
            run_langu(user_inputs)

def run():
    main = Main()
    main.run()

if __name__ == '__main__':
    run()
