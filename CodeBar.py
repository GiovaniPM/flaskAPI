#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime, timedelta
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from json import dumps
from requests import post

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

@app.route('/cb', methods=['GET'])
def decompoe():
    reg = {}

    if request.json == None:
        return jsonify( { 'error': 'No parameters found.' } )
    if 'ipte' in request.json or 'ped.siscom' in request.json or 'cli.siscom' in request.json:
        if 'ipte' in request.json:
            reg['ipte'] = ipte(request.json['ipte'])
        if 'ped.siscom' in request.json:
            reg['ped.siscom'] = pedsiscom(request.json['ped.siscom'])
        if 'age.siscom' in request.json:
            reg['age.siscom'] = agesiscom(request.json['age.siscom'])
        if 'cli.siscom' in request.json:
            reg['cli.siscom'] = clisiscom(request.json['cli.siscom'])
    else:
        return jsonify( { 'error': 'No keys valid found.' } )

    json_result = reg
    return jsonify(json_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))