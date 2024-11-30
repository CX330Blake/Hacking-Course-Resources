# Source: https://github.com/pablocelayes/rsa-wiener-attack

from Crypto.Util.number import long_to_bytes

e = 21765803687512212712163635631428708695453847412110055286687485847508839281105752503180692089257488606774271741012069565129906591185976791283049836431482339848078129948965056137917234818373249017129636314916121106119141791988280880331997979313593792446538886073233027097630384003399279332488341523568146345047116385347915501332852466196657657878013746368237964118882766416129119889496080041741076058915668902613547472857803757381900738809957581478364366531939726628738914478635563863736479821338988018560639178882381027869173449608694213353961578976620137018688997562534407403675658065130497893699412761900233409371737
n = 25838541062218749914223461366309043023670188097143750819323667441033920231009626728360530977618507390012799494467461858443551876965115335639697506550809106379832839915173384373631343910092307921679546936243735058168638296302360298125212747380144625403844429578719961866735719017388711283571412468856175225689053871482587886638657733689156742282060517586625273195334110894881800674612428825560043620899824910091444069575535065720992347370350153658238533461063761591298312797794432502054130225120517883375942288681233305883592649860508636539560383083427887116107857780416850810474994590548245060740453448160227502581009
flag = 15255326897772326000229208511884668230792335715918267905881533086253307472972255687293519435537930366845675793332689902592407071885538098042062367162822454359703135828166812173479505968191378249751209448641075688584939520437774339996867999042087077237352675739867992362236935533590964200067456712914039618702507882760626347291631848238334871857378406448369915296476314678306844780104549123212749216524185139434873208771817755004014761849828445672227861890016478790952071421789854636918425951475192376922296833655678082961963060083988853964127342332065374307712277432617946917386611609659332790132261425365066439863351

CFListT = list[int]  # CF coefficients
CVListT = list[tuple[int, int]]  # Convergents at each coefficient level


def rational_to_contfrac(x: int, y: int) -> tuple[CFListT, CVListT]:
    """
    Converts a rational x/y fraction into
    a list of partial coefficients [a0, ..., an], and
    a list of convergents at each coefficient level [(n0, d0), (n1, d1), ...]

    The algorithm of computing the convergents from left to right is available
    in Section 9.1 of https://r-knott.surrey.ac.uk/Fibonacci/cfINTRO.html#CFtofract

    Args:
        x (int): numerator of the given rational number
        y (int): denominator of the given rational number

    Returns:
        tuple[CFListT, CVListT]: a tuple of coefficients and convergents at each
        coefficient level
    """
    a = x // y
    cflist = [a]
    cvlist = [(a, 1)]
    ppn, ppd = 1, 0  # pre-pre numerator and denominator of convergent
    pn, pd = a, 1  # pre numerator and denominator of convergent
    while a * y != x:
        x, y = y, x - a * y
        a = x // y
        cflist.append(a)
        cn, cd = a * pn + ppn, a * pd + ppd
        cvlist.append((cn, cd))
        ppn, ppd = pn, pd
        pn, pd = cn, cd
    return cflist, cvlist


def bitlength(x):
    """
    Calculates the bitlength of x
    """
    assert x >= 0
    n = 0
    while x > 0:
        n = n + 1
        x = x >> 1
    return n


def isqrt(n):
    """
    Calculates the integer square root
    for arbitrary large nonnegative integers
    """
    if n < 0:
        raise ValueError("square root not defined for negative numbers")

    if n == 0:
        return 0
    a, b = divmod(bitlength(n), 2)
    x = 2 ** (a + b)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def is_perfect_square(n):
    """
    If n is a perfect square it returns sqrt(n),

    otherwise returns -1
    """
    h = n & 0xF
    # last hexadecimal "digit"

    if h > 9:
        return -1  # return immediately in 6 cases out of 16.

    # Take advantage of Boolean short-circuit evaluation
    if h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8:
        # take square root if you must
        t = isqrt(n)
        if t * t == n:
            return t
        else:
            return -1

    return -1


def wiener_attack(e, n):
    """
    Finds d knowing (e,n)
    applying the Wiener continued fraction attack
    """
    _, convergents = rational_to_contfrac(e, n)

    for k, d in convergents:

        # check if d is actually the key
        if k != 0 and (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            s = n - phi + 1
            # check if the equation x^2 - s*x + n = 0
            # has integer roots
            discr = s * s - 4 * n
            if discr >= 0:
                t = is_perfect_square(discr)
                if t != -1 and (s + t) % 2 == 0:
                    print("Hacked!")
                    return d


d = wiener_attack(e, n)
print(long_to_bytes(pow(flag, d, n)))


"""CHALLENGE.py
    Here's the code for the challenge:
import gmpy2
from Crypto.Util.number import GCD, bytes_to_long, getPrime, inverse
from secret import FLAG


def gen() -> tuple[int, int]:
    p, q = 0, 1
    while abs(p - q) >= min(p, q):
        p, q = getPrime(1024), getPrime(1024)

    n = p * q
    phi = (p - 1) * (q - 1)

    e, d = 0, 0
    while GCD(e, phi) > 1 or d >= int(gmpy2.iroot(n, 4)[0]) // 3:
        d = getPrime(201)
        e = inverse(d, phi)

    return e, n


def main():
    m, (e, n) = bytes_to_long(FLAG.encode()), gen()
    print(f"e = {e}")
    print(f"n = {n}")
    print(f"flag = {pow(m, e, n)}")


if __name__ == "__main__":
    main()

"""
