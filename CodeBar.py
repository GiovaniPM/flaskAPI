#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime, timedelta
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from json import dumps
from requests import post

import hashlib
import os

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*","methods":"POST,DELETE,PUT,GET,OPTIONS"}})

def ipte(codigo):
    """
        Format: AAABC.CCDDX DDDDD.DEFFFY FGGGG.GGHHHZ K  UUUUVVVVVVVVVV
                C1          C2           C3           C4 C5

        Onde:

        C1 (AAABC.CCDDX)
            AAA = Código do Banco na Câmara de Compensação (Itaú=341)
            B   = Código da moeda = "9"
            CCC = Código da carteira de cobrança
            DD  = Dois primeiros dígitos do Nosso Número
            X   = DAC que amarra o campo 1

        C2 (DDDDD.DEFFFY)
            DDDDDD = Restante do Nosso Número
            E      = DAC do campo [Agência/Conta/Carteira/ Nosso Número]
            FFF    = Três primeiros números que identificam a Agência
            Y      = DAC que amarra o campo 2

        C3 (FGGGG.GGHHHZ)
            F = Restante do número que identifica a agência
            GGGGGG = Número da conta corrente + DAC
            HHH = Zeros ( Não utilizado )
            Z = DAC que amarra o campo 3

        C4 (K)
            K = DAC do Código de Barras

        C5 (UUUUVVVVVVVVVV)
            UUUU = Fator de vencimento
            VVVVVVVVVV = Valor do Título
    """

    dados = {}
    codigo = codigo.replace(" ", "").replace(".", "")
    data_base = datetime(1997, 10, 7)

    dados['banco'        ] =     codigo[0 :3 ]
    dados['moeda'        ] =     codigo[3 :4 ]
    dados['carteira'     ] =     codigo[4 :7 ]
    dados['nosso numero' ] =     codigo[7 :9 ] + codigo[10:16]
    dados['dac1'         ] =     codigo[9 :10]
    dados['dac2'         ] =     codigo[16:17]
    dados['agencia'      ] =     codigo[17:20] + codigo[21:22]
    dados['dac3'         ] =     codigo[20:21]
    dados['conta'        ] =     codigo[22:28]
    dados['zero'         ] =     codigo[28:31]
    dados['dac4'         ] =     codigo[31:32]
    dados['dac5'         ] =     codigo[32:33]
    dados['fator'        ] =     codigo[33:37]
    dados['valor'        ] = int(codigo[37:47])/100
    dados['vencimento'] = data_base + timedelta(days=int(dados['fator']))

    return dados

def pedmidia(codigo):

    dados = {}
    linha = codigo.split(';')

    for x in range(50):
        linha.append('<N/D>')

    dados['FTFNUM         '] = linha[0 ]
    dados['FTCODPRODU     '] = linha[1 ]
    dados['FTCEMP         '] = linha[2 ]
    dados['FT55CHQDIA     '] = linha[3 ]
    dados['FT55CHQANO     '] = linha[4 ]
    dados['FTCLIAGE       '] = linha[5 ]
    dados['FTAAN8         '] = linha[6 ]
    dados['FTLAGY         '] = linha[7 ]
    dados['FTAN8          '] = linha[8 ]
    dados['FTCTNB         '] = linha[9 ]
    dados['FTNRPEDBIL     '] = linha[10]
    dados['FTBACS         '] = linha[11]
    dados['FTBCT          '] = linha[12]
    dados['FTDTFM         '] = linha[13]
    dados['FTDATAENV      '] = linha[14]
    dados['FTDEMS         '] = ' '
    dados['FTVLRPROD      '] = linha[15]
    dados['FTVLRTOTLI     '] = linha[16]
    dados['FTVLRTOTBR     '] = linha[17]
    dados['FTCARBAN       '] = linha[18]
    dados['FTDAYF         '] = linha[19]
    dados['FTDAYT         '] = 0
    dados['FTPTYPE        '] = linha[20]
    dados['FTDTVN         '] = linha[21]
    dados['FTTITULO       '] = linha[22]
    dados['FTBRULIQ       '] = linha[23]
    dados['FTCODORIGE     '] = linha[24]
    dados['FTFATMIN       '] = linha[25]
    dados['FTACTAPP       '] = linha[26]
    dados['FTDSPA1        '] = ' '
    dados['FTCNOP         '] = ' '
    dados['FTAA07         '] = linha[27]
    dados['FTAA02         '] = linha[28]
    dados['FTAA03         '] = linha[28]
    dados['FTMODE         '] = linha[30]
    dados['FTCOMD         '] = 0
    dados['FTAN8R         '] = 0
    dados['FTDOC          '] = 0
    dados['FTPRODID       '] = linha[31]
    dados['FTCO           '] = linha[32]
    dados['FTAC03         '] = linha[33]
    dados['FTUPMJ         '] = 0
    dados['FTUPMT         '] = 0
    dados['FTCRTDT        '] = 0
    dados['FTCRTM         '] = 0
    dados['FTC75PRNO      '] = linha[34]
    dados['FTCDC          '] = linha[35]
    dados['FTRETRANCA     '] = linha[36]
    dados['FTREFATUR      '] = linha[37]
    dados['FTCODTPVEN     '] = linha[38]
    dados['FTFATSUBS      '] = linha[39]
    dados['FTMCDTL        '] = ' '
    dados['FTACPL         '] = linha[40]
    dados['FTAA10         '] = linha[41]
    dados['FTCCDP         '] = linha[42]
    dados['FTCTA          '] = linha[43]
    dados['FTCTCR         '] = linha[44]
    dados['FTCTDB         '] = linha[45]
    dados['FTCTDC         '] = linha[46]
    dados['FTCTPT         '] = linha[47]

    return dados

def climidia(codigo):

    dados = {}
    linha = codigo.split(';')

    for x in range(50):
        linha.append('<N/D>')

    dados['FTUKCENM   '] = linha[0 ]
    dados['FTCLIAGE   '] = linha[1 ]
    dados['FTAN8      '] = linha[2 ]
    dados['FTWBICGC   '] = linha[3 ]
    dados['FTBCGC     '] = linha[4 ]
    dados['FTWBEND    '] = linha[5 ]
    dados['FTLOCAT    '] = linha[6 ]
    dados['FTWBCID    '] = linha[7 ]
    dados['FTWBUF     '] = linha[8 ]
    dados['FTWBCEP    '] = linha[9 ]
    dados['FTWBIE16   '] = linha[10]
    dados['FTWBIM16   '] = linha[11]
    dados['FTCTNB     '] = linha[12]
    dados['FTMODE     '] = 'N'
    dados['FTBACS     '] = 0
    dados['FTBCT      '] = linha[13]
    dados['FTALPH     '] = linha[14]
    dados['FTAAN8     '] = 0
    dados['FTLAGY     '] = 0
    dados['FTBLCT     '] = 0
    dados['FTBRD60    '] = linha[15]
    dados['FTNRBIL    '] = '16'

    return dados

def pedsiscom(codigo):

    dados = {}

    dados['_tipo'] = codigo[0:2]

    if dados['_tipo'] == '20':
        dados['FTCO           '] = codigo[2  :4  ]
        dados['FTINT01        '] = codigo[4  :10 ]
        dados['FTINT02        '] = codigo[10 :12 ]
        dados['FTINT03        '] = codigo[12 :13 ]
        dados['FTNRAUTORI     '] = codigo[13 :23 ]
        dados['FTDATE01       '] = codigo[23 :29 ]
        dados['FTINT05        '] = codigo[29 :33 ]
        dados['FTAA04         '] = codigo[33 :37 ]
        dados['FTINT06        '] = codigo[37 :40 ]
        dados['FTAA03         '] = codigo[42 :45 ]
        dados['FTEV01         '] = codigo[45 :46 ]
        dados['FTAA08         '] = codigo[46 :54 ]
        dados['FTAA40         '] = codigo[54 :94 ]
        dados['FTAA03A        '] = codigo[94 :97 ]
        dados['FTAA02         '] = codigo[97 :99 ]
        dados['FTAA03B        '] = codigo[99 :102]
        dados['FTEV02         '] = codigo[102:103]
        dados['FTAA03C        '] = codigo[103:106]
        dados['FTEV04         '] = codigo[106:107]
        dados['FTINT08        '] = codigo[107:110]
        dados['FTINT09        '] = codigo[110:113]
        dados['FTINT10        '] = codigo[113:116]
        dados['FTAA03D        '] = codigo[116:119]
        dados['FTEV05         '] = codigo[119:120]
        dados['FTINT11        '] = codigo[120:127]
        dados['FTAA15         '] = codigo[127:142]
        dados['FTAA04B        '] = codigo[142:146]
        dados['FTINT12        '] = codigo[146:153]
        dados['FTAA16         '] = codigo[153:168]
        dados['FTAA04C        '] = codigo[168:172]
        dados['FTMATH11       '] = codigo[172:185]
        dados['FTMATH11A      '] = codigo[185:198]
        dados['FTMATH11B      '] = codigo[198:211]
        dados['FTMATH03       '] = codigo[211:216]
        dados['FTAA09         '] = codigo[225:226]
        dados['FTEV03         '] = codigo[225:226]
        dados['FTDTEJ         '] = codigo[226:232]
        dados['FTUPMT         '] = codigo[232:238]
        dados['FTMUPM         '] = codigo[238:244]
        dados['FTMUPT         '] = codigo[244:250]
        dados['FTEV06         '] = codigo[265:266]
        dados['FTEV07         '] = codigo[266:267]
    elif dados['_tipo'] == '40':
        dados['FTCO           '] = codigo[2  :4  ]
        dados['FTINT01        '] = codigo[4  :10 ]
        dados['FTINT02        '] = codigo[10 :12 ]
        dados['FTINT03        '] = codigo[12 :13 ]
        dados['FTIA02         '] = codigo[13 :15 ]
        dados['FTA301         '] = codigo[15 :18 ]
        dados['FTAA06         '] = codigo[18 :24 ]
        dados['FTAA03         '] = codigo[26 :29 ]
        dados['FTAA03A        '] = codigo[29 :32 ]
        dados['FTAA02         '] = codigo[32 :34 ]
        dados['FTAA03B        '] = codigo[34 :37 ]
        dados['FTAA03C        '] = codigo[37 :40 ]
        dados['FTAA03D        '] = codigo[40 :43 ]
        dados['FTEV05         '] = codigo[43 :44 ]
        dados['FTINT11        '] = codigo[44 :51 ]
        dados['FTAA15         '] = codigo[51 :66 ]
        dados['FTAA04B        '] = codigo[66 :70 ]
        dados['FTINT12        '] = codigo[70 :77 ]
        dados['FTAA16         '] = codigo[77 :92 ]
        dados['FTAA04C        '] = codigo[92 :96 ]
        dados['FTMATH11       '] = codigo[96 :109]
        dados['FTMATH11B      '] = codigo[109:122]
        dados['FTEV03         '] = codigo[122:123]
        dados['FTDTEJ         '] = codigo[123:129]
        dados['FTUPMT         '] = codigo[129:135]
        dados['FTMUPM         '] = codigo[135:141]
        dados['FTMUPT         '] = codigo[141:147]

    return dados

def agesiscom(codigo):

    dados = {}

    dados['FTWBTR1        '] = codigo[0  :1  ]
    dados['FTWBEMP        '] = codigo[1  :3  ]
    dados['FTWBMNE1       '] = codigo[3  :18 ]
    dados['FTWBNOME       '] = codigo[18 :58 ]
    dados['FTWBMNE2       '] = codigo[58 :73 ]
    dados['FTEV01         '] = codigo[73 :74 ]
    dados['FTWBCEND       '] = codigo[74 :78 ]
    dados['FTWBICGC       '] = codigo[78 :79 ]
    dados['FTWBCGC        '] = codigo[79 :93 ]
    dados['FTWBCPF        '] = codigo[93 :104]
    dados['FTWBNOME2      '] = codigo[104:144]
    dados['FTWBEND        '] = codigo[144:184]
    dados['FTAA10         '] = codigo[204:214]
    dados['FTWBBAIR       '] = codigo[214:239]
    dados['FTWBCID        '] = codigo[244:269]
    dados['FTWBUF         '] = codigo[304:306]
    dados['FTWBCEP        '] = codigo[306:314]
    dados['FTWBIE16       '] = codigo[314:330]
    dados['FTWBIM16       '] = codigo[330:346]
    dados['FTWBISSQN      '] = codigo[346:357]
    dados['FTWBINPS       '] = codigo[357:368]
    dados['FTWBPORTA5     '] = codigo[368:373]
    dados['FTWBCAO        '] = codigo[373:380]
    dados['FTWBCCO        '] = codigo[380:387]
    dados['FTWBIAGE       '] = codigo[387:388]
    dados['FTWBEND        '] = dados['FTWBEND        '] + ' ' + dados['FTAA10         ']

    return dados

def clisiscom(codigo):

    dados = {}

    dados['FTWBTR1        '] = codigo[0  :1  ]
    dados['FTWBEMP        '] = codigo[1  :3  ]
    dados['FTWBMNE1       '] = codigo[3  :18 ]
    dados['FTWBNOME       '] = codigo[18 :58 ]
    dados['FTWBMNE2       '] = codigo[58 :73 ]
    dados['FTWBLIM        '] = codigo[73 :82 ]
    dados['FTWBSCLI       '] = codigo[82 :83 ]
    dados['FTWBTCLI       '] = codigo[83 :85 ]
    dados['FTWBDSDO       '] = codigo[85 :92 ]
    dados['FTWBSANT       '] = codigo[92 :107]
    dados['FTWBSATU       '] = codigo[107:121]
    dados['FTWBCEND       '] = codigo[121:125]
    dados['FTWBICGC       '] = codigo[125:126]
    dados['FTWBCGC        '] = codigo[126:140]
    dados['FTWBNOME2      '] = codigo[140:180]
    dados['FTWBEND        '] = codigo[180:220]
    dados['FTAA10         '] = codigo[240:250]
    dados['FTWBBAIR       '] = codigo[250:275]
    dados['FTWBCID        '] = codigo[280:305]
    dados['FTWBUF         '] = codigo[340:342]
    dados['FTWBCEP        '] = codigo[342:350]
    dados['FTWBIE16       '] = codigo[350:366]
    dados['FTWBIM16       '] = codigo[366:382]
    dados['FTWBBCO        '] = codigo[382:386]
    dados['FTWBNCO        '] = codigo[386:393]
    dados['FTWBEND        '] = dados['FTWBEND        '] + ' ' + dados['FTAA10         ']

    return dados

def conv115(codigo):

    linha = codigo['linha']

    dados = {}

    dados['CNPJ tomador'] = linha[0  :14 ]
    dados['Data Emissao'] = linha[81 :89 ]
    dados['Número NF   '] = linha[94 :103]
    dados['Valor NF    '] = linha[135:147]
    dados['Base ICMS   '] = linha[147:159]
    dados['Valor ICMS  '] = linha[159:171]
    dados['CNPJ emissor'] = codigo['cnpj']

    mensagem = dados['CNPJ tomador'] +\
               dados['Número NF   '] +\
               dados['Valor NF    '] +\
               dados['Base ICMS   '] +\
               dados['Valor ICMS  '] +\
               dados['Data Emissao'] +\
               dados['CNPJ emissor']

    dados['linha       '] = mensagem
    dados['hash antiga '] = linha[103:135]
    dados['hash nova   '] = hashlib.md5(mensagem.encode()).hexdigest().upper()

    return dados

@app.route('/cb', methods=['GET'])
def decompoe():
    reg = {}

    if request.json == None:
        return jsonify( { 'error': 'No parameters found.' } )
    else:
        if 'ipte' in request.json or\
           'ped.midia+' in request.json or\
           'cli.midia+' in request.json or\
           'ped.siscom' in request.json or\
           'cli.siscom' in request.json or\
           'age.siscom' in request.json or\
           'conv115' in request.json:
            if 'ipte' in request.json:
                reg['ipte'] = ipte(request.json['ipte'])
            if 'ped.midia+' in request.json:
                reg['ped.midia+'] = pedmidia(request.json['ped.midia+'])
            if 'cli.midia+' in request.json:
                reg['cli.midia+'] = climidia(request.json['cli.midia+'])
            if 'ped.siscom' in request.json:
                reg['ped.siscom'] = pedsiscom(request.json['ped.siscom'])
            if 'age.siscom' in request.json:
                reg['age.siscom'] = agesiscom(request.json['age.siscom'])
            if 'cli.siscom' in request.json:
                reg['cli.siscom'] = clisiscom(request.json['cli.siscom'])
            if 'conv115' in request.json:
                reg['conv115'] = conv115(request.json['conv115'])
            print(reg)
        else:
            return jsonify( { 'error': 'No keys valid found.' } )

    json_result = reg
    return jsonify(json_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))