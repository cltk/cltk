% Prolog Algorithm containing rules to match generated scansions to patterns we believe are found on the disk
rightWay1(S, I):- append([[_], [S], [_]], [_,- u u | - - | - _,_]).