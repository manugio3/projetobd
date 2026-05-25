Modelo Lógico EER Copa do Mundo



Pessoa{**CPF**, NOME, NACIONALIDADE, DT\_NASC}



Jogador{**CPF**, N\_CAMISA, POSIÇÃO, \[CPF\_I]}

&#x09;CPF->Pessoa   //herança

&#x09;CPF\_I->Jogador  //autor relacionamento

IDIOMA{**CPF\_JG,IDIOMAS**}   //atributo multivalorado de jogador

&#x09;CPF\_JG->Jogador



Juiz{**CPF**, CATEGORIA}

&#x09;CPF->Pessoa



Técnico{**CPF**, SALÁRIO}

&#x09;CPF->Pessoa



Seleção{**ID**, RANKING\_FIFA, PAÍS, \[CPF\_T]!}

&#x09;CPF\_T->Técnico  //relacionamento treina



Estádio{**ID**, NOME, CAPACIDADE, ENDEREÇO\_CEP, ENDEREÇO\_NUM, ENDEREÇO\_LOGRADOURO}



Partida{**MATCH\_ID**, DATA, FASE, PÚBLICO, PLACAR\_A, PLACAR\_B, ID\_ESTÁDIO!, ID\_TIME\_A!, ID\_TIME\_B!}

&#x09;ID\_ESTÁDIO->Estádio   //relacionamento ocorre

&#x09;-- Restrição: ID\_TIME\_A <> ID\_TIME\_B

&#x09;ID\_TIME\_A->Seleção

&#x09;ID\_TIME\_B->Seleção



Apita{**CPF\_J,MATCH\_ID\_P**}  //relacionamento

&#x09;CPF\_J->Juiz

&#x09;MATCH\_ID\_P->Partida



Gol{**CPF\_JG**, **MINUTO**, TIPO, MATCH\_ID\_P!}  //entidade fraca de jogador

&#x09;CPF\_JG->Jogador

&#x09;MATCH\_ID\_P->Partida   //relacionamento pode ocorrer



Escalação{**CPF\_JG, MATCH\_ID\_P, ID\_S**, SITUAÇÃO, MIN\_JOGADOS}

&#x09;CPF\_JG->Jogador

&#x09;MATCH\_ID\_P->Partida

&#x09;ID\_S->Seleção

CARTÕES{**CPF\_JG, MATCH\_ID\_P**, CARTÕES\_TIPO}

&#x09;CPF\_JG, MATCH\_ID\_P->Escalação



Convocação{**CPF\_JG, ID\_S**, DATA}

&#x09;CPF\_JG->Jogador

&#x09;ID\_S->Seleção



Prêmio{**COD**, NOME, DESCRIÇÃO, CPF\_JG, ID\_S}

&#x09;CPF\_JG, ID\_S->Convocação

