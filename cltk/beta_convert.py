import re

#to use:
#from beta_convert import *
#b = BetaReplacer()
#b.replace(B)

B = r"""
O(/PWS OU)=N MH\ TAU)TO\ PA/QWMEN E)KEI/NOIS, E)PI\ TH\N DIA/GNWSIN AU)TW=N E)/RXESQAI DEI= PRW=TON. TINE\S ME\N OU)=N AU)TW=N EI)SIN A)KRIBEI=S, TINE\S DE\ OU)K A)KRIBEI=S O)/NTES METAPI/-PTOUSIN EI)S TOU\S E)PI\ SH/YEI: OU(/TW GA\R KAI\ LOU=SAI KAI\ QRE/YAI KALW=S KAI\ MH\ LOU=SAI PA/LIN, O(/TE MH\ O)RQW=S DUNHQEI/HMEN. @@@{1$10*PERI\ TW=N E)PI\ KO/PW| PURECA/NTWN.$}1 @*TOU\S E)PI\ KO/PW| PURE/CANTAS, E)PEIDA\N A)KRIBW=S DIAGNW=|S O(/TI TO\N E)FH/MERON E)PU/RECAN PURETO/N, U(GRAI/NEIN E)C A)NA/GKHS KAI\ E)MYU/XEIN DEI=. GENH/SETAI OU)=N TAU=TA DIA/ TE LOUTRW=N EU)KRA/TWN KAI\ DIAI/THS KAI\ A)LEIMMA/TWN MHDE\N E)XO/NTWN DIAFORHTIKO/N. E)PI\ GA\R TOU/TWN DEI= PRA/TTEIN A(/PANTA, O(/SA PROSQEI=NAI MA=LLON U(GRO/THTA DU/NANTAI H)/PER A)FELEI=N E)K TOU= SW/MATOS, W(/STE OU)DE\ A)NATRI/BEIN DEI= E)PI\ POLU\ TO\ SW=MA OU)D' A)LOIFH=| KEXRH=SQAI XLIARA=| DI' E)LAI/OU MO/NOU, A)LLA\ DI' U(DRELAI/OU MA=LLON: KAI\ GA\R U(GRAI/NEI TOU=TO PLE/ON TOU= KAQ' AU(TO\ E)LAI/OU KAI\ PODHGEI=TAI MA=LLON EI)S BA/QOS U(F' U(/DATOS KAI\ E)MYU/XEI TA\ A)/RQRA DIAQERMANQE/NTA KAI\ DIA/PURA E)K TOU= KO/POU GENO/MENA. DIO\ OU)DE\ A)LEI/FEIN E)N TW=| QERMW=| XRH\ A)E/RI OU)DE\ A)NATRI/BEIN. I(DRW/TWN GA\R KINOUME/NWN OU)DE\ U(GRA=NAI O(/LWS H( A)LOIFH\ DUNH/SETAI DIEKPI/PTOUSA SU\N AU)TOI=S. BE/LTION D' OI)=MAI A)POPLU=NAI TO\N I(DRW=TA XLIARW=| POLLW=| EI)S TO\N E)KTO\S OI)=KON E)CELQO/NTA E)NAPOMA/SSEIN TW=| MA/KTRW| KAI\ OU(/TWS A)LEI/FESQAI TW=| U(DRELAI/W|: EI)=TA PERIMEI/NANTA MIKRO\N @1 EI)SIE/NAI EI)S TH\N TOU= U(/DATOS QERMOU= DECAMENH\N MHD' O(/LWS E)N TW=| A)E/RI DIAMEI/NANTA POLLH\N W(/RAN, A)LLA\ PARO/DW| MO/NON XRW/MENON: OU(/TW GA\R U(GRAN-QH/SETAI KAI\ OU) DE/OS E)/STAI, MH\ DIAKAEI\S KAI\ E)KPURWQEI\S U(PO\ TOU= A)E/ROS E(/TERON PA/LIN E)PIKTH/SHTAI PURETO/N. AU(/TH ME\N H( A)GWGH\ PA=SI TOI=S E)PI\ KO/PW| SUMBA/LLETAI KAI\ MA/LISTA TOI=S E)/XOUSI QERMOTE/RAN TH\N KRA=SIN. OU)K OI)=DA OU)=N, DIA\ TI/ O( QEIO/TATOS *GALHNO\S E)LAI/W| ME\N E)XRH/SATO MO/NON XLIARW=|, TH\N DE\ DIA\ TOU= U(/DATOS MI=CIN E)/FUGEN: E)CO\N GA/R E)STI KAI\ YUXRO\N AU)TW=| U(/DWR MI=CAI, E)/TI DE\ KAI\ XLIARO\N, KAI\ A(PLW=S PRO\S TH\N KRA=SIN E(KA/STOU KAI\ PRO\S TH\N \u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000E)KTROPH\N TH=S QERMASI/AS KAI\ TH=S CHRO/THTOS TH=S E)K TOU= KO/POU TEXQEI/SHS OU(/TW XRHSA/SQW KAI\ TH=| A)LOIFH=|. EI) DE\ KAI\ QELH/SEIAS AU)TOU\S E)K DEUTE/ROU PA/LIN LOU=SAI KAI\ OU(/TW PA/LIN A)LEI=YAI KAI\ EI)S TH\N TOU= QERMOU= DECAMENH\N E)MBIBA/SAI KAI\ POIH=SAI E)GXRONI/SAI, MEGA/LWS GE OU(/TWS AU)TOU\S O)NH/SEIS, W(S U(POSTRE/YANTAS AU)TOU\S A)PO\ LOUTROU= PANTELW=S E)PILAQE/SQAI TOU= KO/POU KAI\ PA/SHS DUSKRASI/AS: KAI\ TAU/TH| TH=| A)GWGH=| KEXRH=SQAI KAI\ E)PI\ TW=N DI' A)GRUPNI/AN PURECA/NTWN KAI\ E)PI\ LU/PH| KAI\ E)PI\ TW=N A)NAKOMIZOME/NWN E)K NO/SOU. LOIPO\N DE\ KAI\ PERI\ TW=N DIA\ SUMBA=SAN A)PEYI/AN PURECA/NTWN TO\N E)FH/-MERON PURETO\N DIALA/BWMEN. @@@{1$10*PERI\ TW=N E)PI\ A)PEYI/A| PURECA/NTWN.$}1 @*(H A)PEYI/A GI/NETAI DIA\ QERMO/THTA KAI\ DIA\ YUXRA\N DE\ MA=LLON DUSKRA-SI/AN: KAI\ GINW/SKETAI R(A|DI/WS E)K TH=S E)RUGH=S KNISSW/DOUS ME\N E)PI\ TW=N DIA\ QERMO/THTA, O)CW/DOUS DE\ E)PI\ TW=N DIA\ YUXRO/THTA A)PEPTOU/NTWN. DEI= DE\ OU) MO/NON TAI=S E)RUGAI=S, A)LLA\ KAI\ TOI=S A)/LLOIS A(/PASI PROSE/XEIN SHMEI/OIS, H(LIKI/A| LE/GW KAI\ KRA/SEI KAI\ E)PITHDEU/MATI KAI\ BI/W| KAI\ TH=| A)/LLH| PA/SH| DIAI/TH| TOU= KA/MNONTOS. OU)/TE GA\R EI) KNISSW/DHS E)STI\N E)RUGH\, PA/NTWS H)/DH KAI\ QERMH\N U(PONOEI=N DEI= TH\N A)PEYI/AN EI)=NAI: E)/SQ' O(/TE GA\R E)GE/NETO KAI\ DIA\ TH\N TW=N E)DHDESME/NWN POIO/THTA H)\ KNISSW=DES H)\ MELITW=DES AU)TW=N FAGO/NTWN: OU) MH\N OU)D' EI) O)CW/DHS E)RUGH\, PA/NTWS U(PONOEI=N DEI= YUXRA\N LE/GEIN TH\N DUSKRASI/AN: POLLA/KIS GA\R KAI\ O)CW/DHS TROFH\ KAI\ STRUFNH\ TH\N O)CW/DH PARESKEU/ASEN E)RUGH\N FANH=NAI: E)/SQ' O(/TE DE\ KAI\ QERMO/THS. GI/NETAI @1 GA\R KAI\ O)CW/DHS E)RUGH\ OU) MO/NON DIA\ YU=CIN, A)LLA\ KAI\ DIA\ QERMH\N DUSKRA-SI/AN KAI\ A)MH/XANON TOIAU/THN E)RUGH\N PAU/SASQAI, EI) MH\ YUXOU/SH| KAI\ U(GRAI-NOU/SH| DIAI/TH| XRH/SAITO/ TIS. DEI= OU)=N E)K PA/NTWN, W(S EI)RH/KAMEN, DIAGINW/SKEIN KAI\ OU(/TW DIAKRI/NANTA BE/BAION AU)TW=N POIEI=SQAI TH\N QERAPEI/AN. @{1$10*PERI\ TH=S DIA\ QERMO/THTA GINOME/NHS FQORA=S KAI\ KNISSW/DOUS E)RUGH=S.$}1 @*TOI=S ME\N OU)=N DIA\ QERMO/THTA FQORA\N U(POMEI/NASI KAI\ A)PEYI/AN KNISSW/DH KAI\ DIA\ TOU=TO PURE/CASI TO\N E)FH/MERON PURETO\N OU) DEI= TA\ QERMAI/NONTA PROS2-FE/REIN E)DE/SMATA H)\ POTA/: KAI\ GA\R EI) PRO\S O)LI/GON DO/COUSI PARHGOREI=SQAI TW=N E)NOXLOU/NTWN PNEUMA/TWN EI)S DIAFO/RHSIN E)LQO/NTWN, A)LL' EI)S U(/STERON AI)/TIA GI/NETAI TOU= MA=LLON E)KPURWQH=NAI TO\N E)FH/MERON PURETO\N, E)/SQ' O(/TE DE\ KAI\ TO\N E)PI\ SH/YEI PA/LIN E)PAKOLOUQH=SAI. O(/PWS OU)=N MH\ TAU=TA GE/NHTAI, KATALLH/LWS XRH\ DIAITA=N KAI\ PRO\S TH\N POIOU=SAN AI)TI/AN E)C E)NANTI/AS I(/STASQAI QERAPEI/AN: A)MH/XANON GA\R TELEI/WS A)POPAU/SASQAI TH\N E)NOXLOU=SAN DIA/QESIN KAI\ OI(=ON E)K R(IZW=N E)KKOPH=NAI MH\ TH=S POIOU/SHS AU)TH\N AI)TI/AS A)NAIRE-QEI/SHS. EI) ME\N OU)=N E)/TI METE/WROS H( FQA/SASA KNISSWQH=NAI TROFH\ FAI/NOITO/ SOI, THNIKAU=TA KEXRH=SQAI PO/MATI TW=| QERMW=| MA/LISTA U(/DATI. DUNATO\N GA/R E)STI TOU=TO TO\ PO/MA TO\ ME\N A)POPLU=NAI KAI\ A)POR)R(I=YAI KAI\ W)QH=SAI PERI\ TH\N KA/TW GASTE/RA, TO\ DE/ TI KAI\ A)NADOQH=NAI PARASKEUA/SAI KAI\ PROSE/TI TO\ CHRO\N KAI\ E)KPURWQE\N H)/DH E)PIKERA/SAI PNEU=MA KAI\ PRAU=+NAI KAI\ XAUNW=SAI TOU\S PO/ROUS. OU)K OI)=DA EI) TOU/TOU KA/LLION A)/N TIS E)PINOH/SEIE TOI=S A)PEPTH/-SASI DIA\ QERMH\N DUSKRASI/AN KAI\ DIA\ TOU=TO PURE/TTOUSI TO\N E)FH/MERON PURETO/N. EI) DE/ SOI TA\ DIEFQARME/NA MH\ BASTAZO/MENA FAI/NOITO PERI\ TO\N STO/MAXON, A)LLA\ FE/ROITO DIA\ GASTRO\S, OU) XRH\ KWLU/EIN, A)LLA\ KAI\ SUNER-GEI=N, W(/STE DU/NASQAI KENWQH=NAI TA\ DIEFQARME/NA MA=LLON DIA\ GASTRO/S: EI) DE\ SUMBH=| DIA\ GASTRO\S FE/RESQAI A)METRO/TERON KAI\ DA/KNESQAI TO\ E)/NTERON, KAI\ E)PI\ LOUTRO\N A)/GEIN AU)TOU\S DEI= KAI\ A)LEI/FEIN OI)/NW| MHLI/NW| TA\ PERI\ TH\N GASTE/RA KAI\ TO\ H(=PAR MA/LISTA KAI\ TRE/FEIN A)/RTW| E)C U(/DATOS QERMOU=: E)MBALLE/SQW DE\ KAI\ R(I/ZA TOU= SELI/NOU KAI\ KORIA/NOU: MH\ A)POZENNU/SQW DE\ TO\ SE/LINON PA/NU, A)LL' EU)QE/WS A)FAIREI/SQW PRO\ TOU= BRA/SAI. OU)X A(/PAC DE\ AU)TO\ @1 E)MBRE/CEIS, A)LLA\ POLLA/KIS E)N TW=| QERMW=|. EI) DE\ QERMO/THS EI)/H E)PI\ TO\N STO/MAXON H)\ FLEGMONH/ TIS, OU)DE\ TH\N R(I/ZAN E)PIBA/LLEIN DEI= TOU= SELI/NOU, A)LL' A)/RA TOU= KORIA/NOU H)\ KAQ' E(AUTOU\S E)SQI/EIN DEI= TOU\S YWMOU\S META\ TOU= QERMOU= DEU/TERON H)\ TRI/TON A)POZENNU/ONTA. EI) DE\ TA\ TH=S GASTRO\S E)PI\ PLE/ON FERO/MENA EI)/H, W(S LOIPO\N A)POKA/MNEIN TH\N DU/NAMIN, KAI\ TO\ O)MFAKO/MELI DOTE/ON H)\ TO\ U(DRO/MHLON H)\ TO\ U(DRORO/SATON: EI) DE\ MH\ FLEGMONH\ FAINOME/NH EI)/H PERI\ TO\ STO/MA TH=S GASTRO\S, KAI\ BRAXU\ DOTE/ON AU)TOI=S *KNIDI/OU H)\ *SABI/NOU BRAXEI=AN E)/XONTOS STU/YIN: EI) DE\ H( DU/NAMIS A)BLABH\S EI)/H, FEUGE/TW E)PIDIDO/NAI TO\N OI)=NON KAI\ MA/LISTA E)PI\ TW=N E)XO/NTWN QERMOTE/RAN TH\N KRA=SIN: EI) GA\R U(PO\ QERMO/THTOS H( KNISSW/DHS A)PEYI/A SUNE/BH, DH=LON O(/TI MA=LLON AU)CHQH/SETAI E)N TOI=S QERMOTE/ROIS, EI) BOULHQEI/HMEN XRH/SASQAI: KAI\ QAUMA/ZEIN E)PE/RXETAI/ MOI, PW=S O( QEIO/TATOS *GALHNO\S E)N TH=| QERAPEUTIKH=| PRAGMATEI/A| TOI=S QERMAI/NOUSI KEXRHME/NOS FAI/NETAI: A)NTI/DOTON GA\R AU)TOI=S E)PITRE/PEI DIDO/NAI TH\N DIA\ TRIW=N PEPE/REWN KAI\ TH\N DIA\ TW=N KUDWNI/WN MH/LWN, E)/CWQEN DE\ PA/LIN E)PITI/QESQAI KATA\ TOU= STOMA/XOU PORFU/RAN E)/XOUSAN NA/RDOU KAI\ A)YINQI/AS KAI\ MASTI/XHS. KAI\ TAU=TA QERMA\ E)PITI/QEI DIA\ TO\ MH\ E)KLU/ESQAI, FHSI/, TO\N TO/NON TOU= STOMA/XOU. E)GW\ DE\ TAU=TA OU)DAMW=S A(RMO/ZEIN H(GOU=MAI TOI=S E)/XOUSI QERMOTE/RAN DIA/QESIN KAI\ TAU=TA LE/GW OU)DAMW=S EI)S A)NTI-LOGI/AN A)FORW=N, A)LL' O(/TI MOI TO\ A)LHQE\S OU(/TWS E)FA/NH E)/XON. DEI= DE\ TO\ A)LHQE\S PANTO\S PROTIMA=N A)EI/: EI) GA\R A)PO\ QERMO/THTOS H( KNISSW/DHS E)RUGH\ KAI\ A)PEYI/A SUNE/BH, E)XRH=N OI)=MAI TOI=S E)NANTI/OIS XRW/MENON TAU/THN OU(/TWS I)A=SQAI: EI) DE\ U(PO\ QERMOTE/RWN KAI\ LIPARW=N E)DESMA/TWN E)GE/NETO, A)NAGKAI=ON H)=N KAI\ OU(/TWS A)MEI=YAI TH\N DI/AITAN E)PI\ TO\ E)NANTI/ON YU/XEIN @1 METRI/WS DUNAME/NHN: KAI\ KAQO/LOU MEMAQH/KAMEN, W(S PA/NTA DIA\ TW=N E)NANTI/WN TA\ PARA\ FU/SIN I)A=SQAI DEI=. KAI\ TO\ PHGA/NINON E)/LAION PROSFE/RESQAI PARAITOU=MAI KAI\ EI)/ TI A)/LLO E)STI\ QERMO\N E)/NEMA KAI\ TOU=TO DIAFEU/GEIN, E)F' W(=N H( FQORA\ KAI\ O( PURETO\S DIA\ QERMH\N DUSKRASI/AN H)KOLOU/QHSE. @{1$10*PERI\ TW=N E)PI\ A)PEYI/A| PURECA/NTWN O)CWDESTE/ROU GINOME/NOU XUMOU=.$}1 @*TOSAU=TA PERI\ TW=N E)PI\ KNISSW/DEI E)RUGH=| PURECA/NTWN: EI)/PWMEN DE\ KAI\ PERI\ TW=N E)K YUXRA=S DUSKRASI/AS A)PEPTHSA/NTWN. H( O)CW/DHS A)PEYI/A OU) PA/NU PE/FUKE TAXE/WS A)NA/PTEIN PURETO/N: EI) D' A)/RA KAI\ SUMBH=| GENE/SQAI PURETO\N, U(PONO/EI KAI\ ZH/TEI, MH/ POTE A)/RA KAI\ DIA\ QERMH\N E)GE/NETO DUS2-KRASI/AN H( O)CW/DHS E)RUGH/: SUMBAI/NEI GA\R E)/SQ' O(/TE MH\ MO/NON DIA\ YU=CIN, A)LLA\ KAI\ DIA\ QERMO/THTA POLLA/KIS E)PIGI/NESQAI: TO\ GA\R AU)TO\ KAI\ E)PI\ TW=N E)KTO\S O(RW=MEN: SUMBAI/NEI GA\R E)N TOI=S QERMOI=S PA/NU OI)KH/MASIN, W(S2-AU/TWS DE\ KAI\ E)N TOI=S YUXROI=S PA/NU TO\N OI)=NON E)/SQ' O(/TE EI)S TO\ O)CW=DES METABA/LLESQAI: O(MOI/WS DE\ KAI\ E)PI\ TH=S ZU/MHS TO\ AU)TO\ QEA/SASQAI E)/STI: KAI\ GA\R AU(/TH E)N QERMOTE/ROIS OI)KH/MASIN E)GXRONI/SASA TRE/PETAI EI)S TO\ O)CW=DES, TO\ DE\ AU)TO\ U(FI/STATAI KAI\ YUXQEI=SA U(PO\ TOU= YUXROU= A)E/ROS, W(/STE U(PO\ TW=N E)NANTI/WN E(\N KAI\ TO\ AU)TO\ GI/NETAI SU/MPTWMA. PROSE/XEIN OU)=N A)NA/GKH KAI\ TOI=S PAROU=SI SHMEI/OIS KAI\ TOI=S PROHGHSAME/NOIS, W(/STE E)K PA/NTWN DUNHQH=NAI GNWRI/SAI, TI/ POT' E)STI\ TO\ AI)/TION, EI)/TE QERMO\N EI)/TE YUXRO\N, KAI\ OU(/TWS E)PI\ TH\N QERAPEI/AN E)/RXESQAI. EI) OU)=N H( O)CW/DHS E)RUGH\ DIA\ QERMO/THTA SUNE/BH, TOI=S E)MYU/XOUSI KAI\ PO/MASI KAI\ SITI/OIS KEXRH=SQAI DEI= KAI\ MA/LISTA TOI=S A)NTE/XEIN DUNAME/NOIS KAI\ MH\ EU)XERW=S DIAFQEI/RESQAI. DIA\ TOU=TO OU)=N OU)DE\ TO\N XULO\N TH=S PTISA/NHS E)PIDIDO/NAI TOU/TOIS DEI= OU)DE\ A)/LIKOS. EU)/FQARTOI GA/R EI)SI KAI\ E)PIPOLA/ZOUSI KAI\ METEWRI/ZONTAI PERI\ TO\N STO/MAXON, O(/QEN KAI\ MA=LLON AU)TOI=S SUMBAI/NEI TO\ O)CU/NESQAI. I)XQU/WN OU)=N OI( SKLHRO/SARKOI TOU/TOIS E)PITH/DEIOI KAI\ O)/RNIS A)PO\ ZE/MATOS H( A(PLOUSTE/RW| GEINAME/NH ZWMW=| \u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000KAI\ I)SIKO\S O(MOI/WS SKLHRO\S, OI(=O/S E)STIN O( A)PO\ TH=S KHRI/DOS KAI\ O( A)PO\ @1 TOU= GLAU/KOU KAI\ O)RFOU= MA/LISTA. KAI\ MH\ QAUMA/SH|S, O(/TI TAU=TA LE/GW: TOI=S GA\R U(POME/NOUSI DIA\ QERMH\N DUSKRASI/AN O)CI/DAS KAI\ PO/DA BO/EION E)PI-DOU\S OU) BLA/YEIS, A)LLA\ KAI\ W)FELH/SEIS: E)GW\ GOU=N OI)=DA E)PI\ POLU\N XRO/NON O)CI/DA U(POME/NONTA/ TINA DIA\ TOU/TWN I)ASA/MENOS. KAI\ PROSE/TI KAI\ O)/STREA MH\ E(YHQE/NTA E)PIDEDWKW\S KAI\ R(ODA/KINA KAI\ PA/SH| TH=| E)MYUXOU/SH| KAI\ DUSFQA/RTW| KAI\ DUSMETABLH/TW| E)XRHSA/MHN TROFH=|. @{1$10*PERI\ TH=S DIA\ YUXRA\N DUSKRASI/AN GINOME/NHS O)CW/DOUS E)RUGH=S.$}1 @*EI) DE\ MH\ GE/NOITO U(PO\ QERMOTE/RAS H( O)CW/DHS E)RUGH\, A)LL' U(PO\ YUXROTE/RAS DUSKRASI/AS, A(RMO/ZEI TO/TE MA=LLON H( QERMAI/NOUSA DI/AITA KAI\ A)NTI/DOTOI, OI(/APE/R E)STI KAI\ H( DIA\ TW=N KUDWNI/WN MH/LWN KAI\ H( DIA\ TRIW=N PEPE/REWN KALOUME/NH KAI\ H( DIA\ TOU= NA/RDOU E)MBROXH/. O(/SA OU)=N O( QEIO/TATOS *GALHNO\S E)PI\ TH=S KNISSW/DOUS E)RUGH=S E)PE/TREYE GI/NESQAI, A(/PANTA MA=LLON E)GW\ TAU=TA TOI=S A)PEPTH/SASI DIA\ YUXRA\N DUSKRASI/AN A(RMO/ZEIN NOMI/ZW KAI\ MH\ A)/LLWS E)/XEIN DU/NASQAI. @@{1$10*PERI\ E)FHME/RWN PURETW=N E)PI\ E)MFRA/CEI GINOME/NWN.$}1 @*GI/NETAI DE\ KAI\ DIA\ GLI/SXROUS XUMOU\S KAI\ PAXEI=S O( E)FH/MEROS PURETO\S A)DIAPNEUSTOU/NTWN KAI\ DRIMUTE/RWN GINOME/NWN DHLONO/TI DIA\ TH\N A)DIAPNEUSTI/AN TW=N PERITTWMA/TWN: PROSE/XEIN OU)=N A)KRIBW=S E)NTAU=QA XRH\ TO\N NOU=N KAI\ DIAGINW/SKEIN, EI)/TE PLH=QOS MO/NON E)STI\ TO\ POIH=SAN TH\N E)/MFRACIN EI)/TE PAXU/THS MO/NH KAI\ GLISXRO/THS XUMW=N: EI) ME\N GA\R PLH=QOS EI)/H, KENW=SAI DEI= PRO/ GE PA/NTWN DIA\ FLEBOTOMI/AS: EI)=Q' OU(/TW TOI=S KATA\ ME/ROS XRH/SASQAI BOHQH/MASIN, O(/SA TE XALA=N KAI\ DIAFOREI=N H)\ LEPTU/NEIN DU/NATAI: EI) GA\R MH\ KENW/SAS TOI=S XALASTIKOI=S H)\ DIAFOROU=SI BOULHQEI/H TIS XRH/SASQAI, @1 MEGA/LWN KAKW=N AI)/TIOS GI/NETAI: TH\N GA\R E)/MFRACIN E)/TI MA=LLON E)PITEI/NOUSI TOI=S DIAFORHTIKOI=S PRO\ TH=S PE/YEWS H)\ KENW/SEWS KEXRHME/NOI BOHQH/MASIN. EI) DE\ MH\ PLH=QOS EI)/H TO\ TH\N E)/MFRACIN E)RGASA/MENON, A)LLA\ GLI/SXROI KAI\ PAXEI=S XUMOI\, OU) DEI= FLEBOTOMEI=N, A)LLA\ KEXRH=SQAI/ TISI MA=LLON A)PO-ZE/MASI TOI=S LEPTU/NEIN A)/NEU TOU= QERMAI/NEIN DUNAME/NOIS KAI\ MH\ E)PITA/TTEIN, A(/PER A)POTOLMW=SIN OI( POLLOI\ TW=N I)ATRW=N, E(/RPULLON H)\ KALAMI/NQHN H)\ U(/SSWPON H)\ O)RI/GANON H)\ PH/GANON PROSFE/REIN TOU/TOIS OU)K EI)DO/TES, O(/TI MEIZO/NWS A)DIKOU=SIN H)/PER MA=LLON W)FELOU=SI TOU\S KA/MNONTAS: EI) GA/R TI KAI\ LEPTU/NEIN DOKOU=SI TH\N U(/LHN, A)LL' OU)=N A)/LLWS BLA/PTOUSI DRIMUTE/ROUS E)RGAZO/MENOI TOU\S PURETOU/S: SPOUDA/ZEIN OU)=N MA=LLON E)KEI=NA ZHTEI=N, O(/SA R(U/PTEIN KAI\ LEPTU/NEIN OI)=DEN A)/NEU TOU= QERMAI/NEIN. E)/STI D' E)N TOU/TOIS TO\ O)CU/MELI KAI\ R(U/PTON GENNAI/WS KAI\ TOU\S PURETOU\S MH\ PAROCU/NON.
"""

#en.wikipedia.org/wiki/Beta_code
#lowercase almost done, upper remaining
replacement_patterns = [
    #CAPS
    #BREVE, ALL, UPPER
    #Ᾰ Ῐ Ῠ
    (r'\*A\'', 'Ᾰ'),
    (r'\*I\'', 'Ῐ'),
    (r'\*U\'', 'Ῠ'),
    #MACRON, ALL, UPPER
    #Ᾱ Ῑ Ῡ
    (r'\*A&', 'Ᾱ'),
    (r'\*I&', 'Ῑ'),
    (r'\*U&', 'Ῡ'),
    #ALL RHOS, LOWER
    (r'\*R\(', 'Ῥ'),
    #IOTA SUBSCRIPTS + ALL ACCENTS, UPPER
    #ᾈ 	ᾉ 	ᾊ 	ᾋ 	ᾌ 	ᾍ 	ᾎ 	ᾏ
    (r'\*A\)\|', 'ᾈ'),
    (r'\*A\(\|', 'ᾉ'),
    (r'\*A\)\\\|', 'ᾊ'),
    (r'\*A\(\\\|', 'ᾋ'),
    (r'\*A\)/\|', 'ᾌ'),
    (r'\*A\(/\|', 'ᾍ'),
    (r'\*A\)=\|', 'ᾎ'),
    (r'\*A\(=\|', 'ᾏ'),
    #ᾘ 	ᾙ 	ᾚ 	ᾛ 	ᾜ 	ᾝ 	ᾞ 	ᾟ
    (r'\*H\)\|', 'ᾘ'),
    (r'\*H\(\|', 'ᾙ'),
    (r'\*H\)\\\|', 'ᾚ'),
    (r'\*H\(\\\|', 'ᾛ'),
    (r'\*H\)/\|', 'ᾜ'),
    (r'\*H\(/\|', 'ᾝ'),
    (r'\*H\)=\|', 'ᾞ'),
    (r'\*H\(=\|', 'ᾟ'),
    #MAKE UPPER: ᾠ 	ᾡ 	ᾢ 	ᾣ 	ᾤ 	ᾥ 	ᾦ 	ᾧ
    #ᾨ 	ᾩ 	ᾪ 	ᾫ 	ᾬ 	ᾭ 	ᾮ 	ᾯ
    (r'W\)\|', 'ᾨ'),
    (r'W\(\|', 'ᾩ'),
    (r'W\)\\\|', 'ᾪ'),
    (r'W\(\\\|', 'ᾫ'),
    (r'W\)/\|', 'ᾬ'),
    (r'W\(/\|', 'ᾭ'),
    (r'W\)=\|', 'ᾮ'),
    (r'W\(=\|', 'ᾯ'),
    #MAKE UPPER: ᾲ 	ᾳ 	ᾴ  ᾷ
    #(r'A\\\|', 'ᾲ'),
    #(r'A\|', 'ᾳ'),
    #(r'A/\|', 'ᾴ'),
    #(r'A=\|', 'ᾷ'),
    #MAKE UPPER: ῂ 	ῃ 	ῄ  ῇ
    #(r'H\\\|', 'ῂ'),
    #(r'H\|', 'ῃ'),
    #(r'H/\|', 'ῄ'),
    #(r'H=\|', 'ῇ'),
    #MAKE UPPER: ῲ 	ῳ 	ῴ  ῷ
    #(r'W\\\|', 'ῲ'),
    #(r'W\|', 'ῳ'),
    #(r'W/\|', 'ῴ'),
    #(r'W=\|', 'ῷ'),
    #BREATHING + GRAVE, UPPER
    (r'\*A\)\\', 'Ἂ'),
    (r'\*A\(\\', 'Ἃ'),
    (r'\*E\)\\', 'Ἒ'),
    (r'\*E\(\\', 'Ἓ'),
    (r'\*H\)\\', 'Ἢ'),
    (r'\*H\(\\', 'Ἣ'),
    (r'\*I\)\\', 'Ἲ'),
    (r'\*I\(\\', 'Ἳ'),
    (r'\*O\)\\', 'Ὂ'),
    (r'\*O\(\\', 'Ὃ'),
    #(r'\*U\)\\', 'ὒ'),
    (r'\*U\(\\', 'Ὓ'),
    (r'\*W\)\\', 'Ὢ'),
    (r'\*W\(\\', 'Ὣ'),
    #BREATHING + SHARP, UPPER
    (r'\*A\)/', 'Ἄ'),
    (r'\*A\(/', 'Ἅ'),
    (r'\*E\)/', 'Ἔ'),
    (r'\*E\(/', 'Ἕ'),
    (r'\*H\)/', 'Ἤ'),
    (r'\*H\(/', 'Ἥ'),
    (r'\*I\)/', 'Ἴ'),
    (r'\*I\(/', 'Ἵ'),
    (r'\*O\)/', 'Ὄ'),
    (r'\*O\(/', 'Ὅ'),
    #(r'\*U\)/', ''),
    (r'\*U\(/', 'Ὕ'),
    (r'\*W\)/', 'Ὤ'),
    (r'\*W\(/', 'Ὥ'),
    #BREATHING + CIRCUMFLEX, UPPER
    (r'\*A\)=', 'Ἆ'),
    (r'\*A\(=', 'Ἇ'),
    (r'\*H\)=', 'Ἦ'),
    (r'\*H\(=', 'Ἧ'),
    (r'\*I\)=', 'Ἶ'),
    (r'\*I\(=', 'Ἷ'),
    #(r'\*U\)=', 'ὖ'),
    (r'\*U\(=', 'Ὗ'),
    (r'\*W\)=', 'Ὦ'),
    (r'\*W\(=', 'Ὧ'),
    #CIRCUMFLEX, UPPER
    (r'\*A=', 'Ἆ'),
    (r'\*H=', 'Ἦ'),
    (r'\*I=', 'Ἶ'),
    #(r'\*U=', 'ῦ'),
    (r'\*W=', 'Ὦ'),
    #BREATHING, UPPER
    (r'A\)', 'ἀ'),
    (r'A\(', 'ἁ'),
    (r'E\)', 'ἐ'),
    (r'E\(', 'ἑ'),
    (r'H\)', 'ἠ'),
    (r'H\(', 'ἡ'),
    (r'I\)', 'ἰ'),
    (r'I\(', 'ἱ'),
    (r'O\)', 'ὀ'),
    (r'O\(', 'ὁ'),
    (r'U\)', 'ὐ'),
    (r'U\(', 'ὑ'),
    (r'W\)', 'ὠ'),
    (r'W\(', 'ὡ'),
    ########################
    ########################
    ########################
    ########################
    #diaresis, all, lower
    #ῒ 	ΐ 	ῖ 	ῗ
    (r'i\\+', 'ῒ'),
    (r'i/+', 'ΐ'),
    (r'i=+', 'ῗ'),
    #ῢ 	ΰ 	ῧ
    (r'U\\+', 'ῢ'),
    (r'U/+', 'ΰ'),
    (r'U=+', 'ῧ'),
    #breve, all, lower
    #ᾰ ῐ ῠ
    (r'A\'', 'ᾰ'),
    (r'I\'', 'ῐ'),
    (r'U\'', 'ῠ'),
    #macron, all, lower
    #ᾱ ῑ ῡ
    (r'A&', 'ᾱ'),
    (r'I&', 'ῑ'),
    (r'U&', 'ῡ'),
    #all rhos, lower
    (r'R\)', 'ῤ'),
    (r'R\(', 'ῥ'),
    #iota subscripts + all accents, lower
    #ᾀ 	ᾁ 	ᾂ 	ᾃ 	ᾄ 	ᾅ 	ᾆ 	ᾇ
    (r'A\)\|', 'ᾀ'),
    (r'A\(\|', 'ᾁ'),
    (r'A\)\\\|', 'ᾂ'),
    (r'A\(\\\|', 'ᾃ'),
    (r'A\)/\|', 'ᾄ'),
    (r'A\(/\|', 'ᾅ'),
    (r'A\)=\|', 'ᾆ'),
    (r'A\(=\|', 'ᾇ'),
    #ᾐ 	ᾑ 	ᾒ 	ᾓ 	ᾔ 	ᾕ 	ᾖ 	ᾗ
    (r'H\)\|', 'ᾐ'),
    (r'H\(\|', 'ᾑ'),
    (r'H\)\\\|', 'ᾒ'),
    (r'H\(\\\|', 'ᾓ'),
    (r'H\)/\|', 'ᾔ'),
    (r'H\(/\|', 'ᾕ'),
    (r'H\)=\|', 'ᾖ'),
    (r'H\(=\|', 'ᾗ'),
    #ᾠ 	ᾡ 	ᾢ 	ᾣ 	ᾤ 	ᾥ 	ᾦ 	ᾧ
    (r'W\)\|', 'ᾠ'),
    (r'W\(\|', 'ᾡ'),
    (r'W\)\\\|', 'ᾢ'),
    (r'W\(\\\|', 'ᾣ'),
    (r'W\)/\|', 'ᾤ'),
    (r'W\(/\|', 'ᾥ'),
    (r'W\)=\|', 'ᾦ'),
    (r'W\(=\|', 'ᾧ'),
    #ᾲ 	ᾳ 	ᾴ  ᾷ
    (r'A\\\|', 'ᾲ'),
    (r'A\|', 'ᾳ'),
    (r'A/\|', 'ᾴ'),
    (r'A=\|', 'ᾷ'),
    #ῂ 	ῃ 	ῄ  ῇ
    (r'H\\\|', 'ῂ'),
    (r'H\|', 'ῃ'),
    (r'H/\|', 'ῄ'),
    (r'H=\|', 'ῇ'),
    #ῲ 	ῳ 	ῴ  ῷ
    (r'W\\\|', 'ῲ'),
    (r'W\|', 'ῳ'),
    (r'W/\|', 'ῴ'),
    (r'W=\|', 'ῷ'),
    #breathing + grave, lower
    (r'A\)\\', 'ἂ'),
    (r'A\(\\', 'ἃ'),
    (r'E\)\\', 'ἒ'),
    (r'E\(\\', 'ἓ'),
    (r'H\)\\', 'ἢ'),
    (r'H\(\\', 'ἣ'),
    (r'I\)\\', 'ἲ'),
    (r'I\(\\', 'ἳ'),
    (r'O\)\\', 'ὂ'),
    (r'O\(\\', 'ὃ'),
    (r'U\)\\', 'ὒ'),
    (r'U\(\\', 'ὓ'),
    (r'W\)\\', 'ὢ'),
    (r'W\(\\', 'ὣ'),
    #breathing + sharp, lower
    (r'A\)/', 'ἄ'),
    (r'A\(/', 'ἅ'),
    (r'E\)/', 'ἔ'),
    (r'E\(/', 'ἕ'),
    (r'H\)/', 'ἤ'),
    (r'H\(/', 'ἥ'),
    (r'I\)/', 'ἴ'),
    (r'I\(/', 'ἵ'),
    (r'O\)/', 'ὄ'),
    (r'O\(/', 'ὅ'),
    (r'U\)/', 'ὔ'),
    (r'U\(/', 'ὕ'),
    (r'W\)/', 'ὤ'),
    (r'W\(/', 'ὥ'),
    #breathing + circumflex, lower
    (r'A\)=', 'ἆ'),
    (r'A\(=', 'ἇ'),
    (r'H\)=', 'ἦ'),
    (r'H\(=', 'ἧ'),
    (r'I\)=', 'ἶ'),
    (r'I\(=', 'ἷ'),
    (r'U\)=', 'ὖ'),
    (r'U\(=', 'ὗ'),
    (r'W\)=', 'ὦ'),
    (r'W\(=', 'ὧ'),
    #circumflex, lower
    (r'A=', 'ᾶ'),
    (r'H=', 'ῆ'),
    (r'I=', 'ῖ'),
    (r'U=', 'ῦ'),
    (r'W=', 'ῶ'),
    #breathing, lower
    (r'A\)', 'ἀ'),
    (r'A\(', 'ἁ'),
    (r'E\)', 'ἐ'),
    (r'E\(', 'ἑ'),
    (r'H\)', 'ἠ'),
    (r'H\(', 'ἡ'),
    (r'I\)', 'ἰ'),
    (r'I\(', 'ἱ'),
    (r'O\)', 'ὀ'),
    (r'O\(', 'ὁ'),
    (r'U\)', 'ὐ'),
    (r'U\(', 'ὑ'),
    (r'W\)', 'ὠ'),
    (r'W\(', 'ὡ'),
    #accent, lower
    (r'A\\', 'ὰ'),
    (r'A/', 'ά'),
    (r'E/', 'έ'),
    (r'E\\', 'ὲ'),
    (r'H/', 'ή'),
    (r'H\\', 'ὴ'),
    (r'I/', 'ί'),
    (r'I\\', 'ὶ'),
    (r'O/', 'ό'),
    (r'O\\', 'ὸ'),
    (r'U/', 'ύ'),
    (r'U\\', 'ὺ'),
    (r'W/', 'ώ'),
    (r'W\\', 'ὼ'),
    #plain, upper + lower
    (r'\*A', 'Α'),
    (r'A', 'α'),
    (r'\*B', 'Β'),
    (r'B', 'β'),
    (r'\*C', 'Ξ'),
    (r'C', 'ξ'),
    (r'\*D', 'Δ'),
    (r'D', 'δ'),
    (r'\*E', 'Ε'),
    (r'E', 'ε'),
    (r'\*F', 'Φ'),
    (r'F', 'φ'),
    (r'\*G', 'Γ'),
    (r'G', 'γ'),
    (r'\*H', 'Η'),
    (r'H', 'η'),
    (r'\*I', 'Ι'),
    (r'I', 'ι'),
    (r'\*K', 'Κ'),
    (r'K', 'κ'),
    (r'\*L', 'Λ'),
    (r'L', 'λ'),
    (r'\*M', 'Μ'),
    (r'M', 'μ'),
    (r'\*N', 'Ν'),
    (r'N', 'ν'),
    (r'\*O', 'Ο'),
    (r'O', 'ο'),
    (r'\*P', 'Π'),
    (r'P', 'π'),
    (r'\*Q', 'Θ'),
    (r'Q', 'θ'),
    (r'\*R', 'Ρ'),
    (r'R', 'ρ'),
    (r'\*S', 'Σ'),
    (r'S1', 'σ'),
    (r'S2', 'ς'),
    (r'\*S3', 'Σ'),
    (r'S3', 'c'),
    (r'S', 'σ'),
    (r'\*T', 'Τ'),
    (r'T', 'τ'),
    (r'\*U', 'Υ'),
    (r'U', 'υ'),
    (r'\*V', 'Ϝ'),
    (r'V', 'ϝ'),
    (r'\*W', 'Ω'),
    (r'W', 'ω'),
    (r'\*X', 'Χ'),
    (r'X', 'χ'),
    (r'\*Y', 'Ψ'),
    (r'Y', 'ψ'),
    (r'\*Z', 'Ζ'),
    (r'Z', 'ζ'),
    #punctuation
    (r'\.', '.'),
    (r',', ','),
    (r':', '·'),
    (r';', ';'),
    (r'\'', '’'),
    #cut hyphens above, before this processing
    (r'-', '-'),
    (r'_', '—'),
]

class BetaReplacer(object):
    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
        return s
