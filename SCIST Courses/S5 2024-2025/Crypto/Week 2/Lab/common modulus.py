from Crypto.Util.number import inverse, long_to_bytes

# 已知参数
n = 79466774258570652794732143076881721248357924313804495918839594598373092266689466846736029585634734404777530025940530076614619084538506181484865843673363735669715975868551562179019517936376162037209284734078710544170717295438532873033443489455642052013355339940650763973378439258937987322336922689907393102411663418119660768459961200849314990145359779168850408767442673780373518625264630231575342829650610355023157107331670364776439693187760286195036778029411887165083757465559528106695320159799858127673864068841089614946928789963175358060976616137972188081630998945871662078177967311436396227089886245318584486765441
e1 = 2686537139313725050483218215122996056759938188386695701495129
e2 = 2861854619504934492087441304835700273613391529292837570149991
c1 = 9629027184090735396433992022607311357012707938362658687071596942052066844557415299491784638902507816261036562801746514695552785897018334372958442387160354611373232784944279757058303273711692299107515427590063437249132836558366957689240237284314826291229246495940270728901499183912516876767323301371570726813014134416174309147817251948361390312124009886265627953085819595458416108626383901888453307422097679659450593455892975169718371495691549950709354101347978391428334797940623855811897650473643700651322351085221896053877965674315918607156550542615522356725779630172200477966423221265764895433825854341844416533072
c2 = 6587850485066898382052597392740450217182883145708337816196949482406017031618179834810397806758063420322718058462540805349817506824048434036883263491387464491833680742143805990256297721083734190335815638825572637899105898096804492447284946795838888037663066032460959069477169752021299171213148166152989779866964562071846551079607791259503833462812706644439336507226031816956462358168067668006543314703640244406573970740970582322994201448547739763181595253813203811828308612643662337499960146270697202108528379445131497080120280012457233250199445186752244578832937498446744855215693491999985463746598713057437221183934


# 扩展欧几里得算法求解 x 和 y
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


# 求解 x 和 y
gcd, x, y = extended_gcd(e1, e2)

# 确保 e1 和 e2 互质
assert gcd == 1

# 计算 m = c1^x * c2^y mod n
if x < 0:
    c1_inv = inverse(c1, n)
    c1_part = pow(c1_inv, -x, n)
else:
    c1_part = pow(c1, x, n)

if y < 0:
    c2_inv = inverse(c2, n)
    c2_part = pow(c2_inv, -y, n)
else:
    c2_part = pow(c2, y, n)

# 合并结果
m = (c1_part * c2_part) % n

# 转换为字符串
flag = long_to_bytes(m).decode()
print("Decrypted FLAG:", flag)


""" CHALLENGE.py

from Crypto.Util.number import bytes_to_long, getPrime

from secret import FLAG


if __name__ == "__main__":
    flag = bytes_to_long(FLAG.encode())
    n = getPrime(1024) * getPrime(1024)
    e1 = getPrime(201)
    e2 = getPrime(201)

    print(f"n = {n}")
    print(f"e1 = {e1}")
    print(f"e2 = {e2}")
    print(f"c1 = {pow(flag, e1, n)}")
    print(f"c2 = {pow(flag, e2, n)}")
    
"""