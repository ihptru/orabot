# Copyright 2011-2013 orabot Developers
#
# This file is part of orabot, which is free software: you can redistribute it and/or modify
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Makes mathematical calculations. Use command without arguments to see a list of math functions.
"""

import math

def calc(self, user, channel):
    command = (self.command).split()
    if ( len(command) > 1 ):
        expr = " ".join(command[1:])
        expr = expr.replace('^','**')

        def calc(expr):
            return self.safe_eval(expr, vars(math))

        try:
            result = calc(expr)
            self.send_reply( (str(result)), user, channel )
        except (ArithmeticError, NameError, TypeError, SyntaxError):
            self.send_reply( ("Error encountered!"), user, channel )
    else:
        functions = 'pow, fsum, cosh, ldexp, hypot, acosh, tan, asin, isnan, log, fabs, floor, atanh, modf, sqrt, frexp, degrees, pi, log10, asinh, exp, atan, factorial, copysign, ceil, isinf, sinh, trunc, cos, e, tanh, radians, sin, atan2, fmod, acos, log1p'
        self.send_reply( ("Available functions: "+functions), user, channel )
