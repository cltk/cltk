% Prolog Algorithm containing rules to match generated scansions to patterns we believe are found on the disk
rightWay(S, P, I):- 
    append([_, P, _], S),
    I is 1.