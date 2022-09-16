import _paths
import oems
from neo4j import GraphDatabase
import networkx as nx
import sys
import os
from network2tikz import plot
import matplotlib.pyplot as plt
from fa2 import ForceAtlas2
import seaborn as sns
import numpy as np
import pandas as pd
import plotly.express as px

import graph_mining as gm


def plot_schema(cypherTxt, style):

    nodes, rels = gm.neo4jReturn(cypherTxt)
    G = nx.DiGraph()

    for n in nodes:
        label, = n._labels
        print(label)
        G.add_node(n.id, label=label, name=label)

    for r in rels:
        if r.type == 'NRG_PART':
            continue
        G.add_edge(r.start_node.id, r.end_node.id, type=r.type)

    pos = nx.planar_layout(G)

    posV = list(pos.values())
    simP, partP, measP = posV[1], posV[2], posV[3]
    posV[1], posV[2], posV[3] = partP * 3, simP, measP * 3
    i = 0
    for k, v in pos.items():
        pos[k] = posV[i]
        i += 1

    styleG = style.style(G, pos, w='type')
    styleG['edge_color'] = 'gray!40'
    styleAdd = {
        'canvas': (8, 8),
        'vertex_size': 0.8,
        'edge_label_color': 'black!80',
        'edge_label_size': 7,
        'node_style': '{draw=white}',
    }
    print(styleG)
    plot(G, **styleG, **styleAdd)
    plot(
        G,
        '../publication/KG_energyAbsorption/images/tikz/tikznetwork.tex',
        **styleG, **styleAdd, standalone=False)


def plot_bipartite(cypherTxt, style):
    pidMax = 5
    wscl = 10e6

    cypherTxt = cypherTxt.format('', pidMax)
    G = gm.get_graph(
        cypherTxt, style.nodeColor, w=wscl)

    nodesD = G.nodes(data=True)
    si = 1000
    mapping = {}
    for u in nodesD:
        if u[1]['label'] == 'Sim':
            G = nx.relabel_nodes(G, {u[0]: si})
            si += 1
            u[1]['name'] = '0' + str(int(u[1]['name']) - 3)
    # ---------
    # Bipartite
    # ---------
    top, btw = nx.bipartite.sets(G)
    pos = nx.bipartite_layout(G, top, aspect_ratio=2.5, align='horizontal')

    styleG = style.style(G, pos, w='weight')
    styleG['vertex_label'] = ['' for u in G.nodes()]
    styleG['edge_color'] = 'gray!40'
    styleG['margin'] = 0.5

    styleAdd = {
        'canvas': (12.5, 5),
        'vertex_size': 0.8,
        'edge_label_color': 'black!80',
        'edge_label_size': 8,
        'node_style': '{draw=white}',
        'keep_aspect_ratio': False,
        'edge_label_distance': 0.15
    }
    plot(
        G,
        '../publication/06_KG_energyAbsorption/images/tikz/bipartite.tex',
        **styleG, **styleAdd)  # , standalone = False)


def plot_bipartite_cevt_1(cypherTxt, style):
    pidMax = 8
    con = False
    rls = 'stcr'
    lc = 'fo5'
    filename = 'bipartite_{}_{}_pid{}'.format(rls, lc, pidMax)
    sTxt = '.*{}.*{}.*'.format(rls, lc)

    while not con:
        cypherTxt = cypherTxt.format(sTxt, pidMax)
        G = gm.get_graph(
            cypherTxt, style.nodeColor)
        con = nx.is_connected(G)
        print(con, pidMax)
        pidMax += 1
        if pidMax == 21:
            break

    print(pidMax - 1)
    # ---------
    # Bipartite
    # ---------
    top, btw = nx.bipartite.sets(G)
    print('Total Sim:', len(top), 'Total Des:', len(btw))
    # return
    pos = nx.bipartite_layout(G, top, aspect_ratio=2.5,
                              align='horizontal')  # aspect_ratio=0.4
    # style.node_label_pos['Des'] = 'below'

    # pos = nx.spring_layout(G)
    styleG = style.style(G, pos)
    styleG['vertex_label'] = ['' for u in G.nodes()]
    styleG['edge_color'] = 'gray!70'
    styleG['margin'] = 0.3
    styleAdd = {
        'canvas': (35, 17),
        # 'canvas': (12, 32),
        'vertex_size': 0.4,
        'edge_label_color': 'black!60',
        'node_style': '{draw=none}',
        'keep_aspect_ratio': False,
    }
    # fig = nx.draw_networkx(G, pos, **styleG, **styleAdd)
    # plt.show()
    plot(
        G,
        '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(
            filename),
        **styleG, **styleAdd, standalone=False)


def plot_bipartite_cevt_2(cypherTxt, style):
    pidMax = 15
    con = False
    wscl = 1

    rls = 'stcr'
    lc = 'fo5'
    filename = 'bipartite_{}_{}'.format(rls, lc)
    sTxt = '.*{}.*{}.*'.format(rls, lc)

    while not con:
        cypherTxt = cypherTxt.format(sTxt, pidMax)
        G = gm.get_graph(
            cypherTxt, style.nodeColor, w=wscl)
        con = nx.is_connected(G)
        print(con, pidMax)
        pidMax += 1
        if pidMax == 21:
            break

    print(pidMax - 1)
    # ---------
    # Bipartite
    # ---------
    top, btw = nx.bipartite.sets(G)
    pos = nx.bipartite_layout(G, top, aspect_ratio=0.4)
    # style.node_label_pos['Des'] = 'below'

    # pos = nx.spring_layout(G)
    styleG = style.style(G, pos, w='weight')
    styleG['vertex_label'] = ['' for u in G.nodes()]
    styleG['edge_color'] = 'gray!40'
    styleG['margin'] = 0.3
    styleAdd = {
        'canvas': (6, 16),
        'vertex_size': 0.5,
        'edge_label_color': 'black!60',
        'node_style': '{draw=none}',
        'keep_aspect_ratio': False,
        'edge_label_size': 8,
    }
    # fig = nx.draw_networkx(G, pos, **styleG, **styleAdd)
    # plt.show()
    plot(
        G,
        '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(
            filename),
        **styleG, **styleAdd, standalone=False)


def plot_spring_yaris_FR(cypherTxt, style,
                         pidMax=20,
                         con=False,
                         wscl=1,
                         opt=''
                         ):
    filename = 'spring_layout_yaris_FR{}'.format(opt)

    G = gm.get_graph(
        cypherTxt, style.nodeColor, pidMax=pidMax, w=wscl)

    pos = nx.spring_layout(G, weight='weight')
    styleG = style.style(G, pos)
    # styleG['vertex_label'] = ['' for u in G.nodes()]
    styleG['edge_color'] = 'gray!40'
    styleG['margin'] = 0.5
    styleAdd = {
        'canvas': (20, 20),
        'vertex_size': 0.4,
        'edge_label_color': 'black!60',
        'node_style': '{draw=none}',
        'keep_aspect_ratio': False,
    }
    plot(
        G,
        '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(
            filename),
        **styleG, **styleAdd, standalone=False)


def plot_spring_yaris_KK(cypherTxt, style,
                         pidMax=20,
                         con=False,
                         wscl=1,
                         opt=''
                         ):

    filename = 'spring_layout_yaris_KK{}'.format(opt)

    G = gm.get_graph(
        cypherTxt, style.nodeColor, pidMax=pidMax, w=wscl)

    pos = nx.kamada_kawai_layout(G, weight='weight')
    styleG = style.style(G, pos)
    # styleG['vertex_label'] = ['' for u in G.nodes()]
    styleG['edge_color'] = 'gray!40'
    styleG['margin'] = 0.5
    styleAdd = {
        'canvas': (20, 20),
        'vertex_size': 0.4,
        'edge_label_color': 'black!60',
        'node_style': '{draw=none}',
        'keep_aspect_ratio': False,
    }
    plot(
        G,
        '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(
            filename),
        **styleG, **styleAdd, standalone=False)


def plot_spring_yaris_forceatlas(cypherTxt, style,
                                 pidMax=15,
                                 con=False,
                                 wscl=1,
                                 opt=''
                                 ):

    filename = 'spring_layout_yaris_FA2{}'.format(opt)

    cypherTxt = cypherTxt.format('', pidMax)
    G = gm.get_graph(
        cypherTxt, style.nodeColor, w=wscl)

    sum_w = max([G[u][v]['weight'] for u, v in G.edges()])
    for u, v in G.edges():
        G[u][v]['weight'] = abs(G[u][v]['weight'] / sum_w)

    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=False,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=1.0,
        strongGravityMode=False,
        # gravity=1.0,

        # Log
        verbose=True)
    pos = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=5000)

    styleG = style.style(G, pos)
    # styleG['vertex_label'] = ['' for u in G.nodes()]
    styleG['edge_color'] = 'gray!40'
    styleG['margin'] = 0.5
    styleAdd = {
        'canvas': (30, 30),
        'vertex_size': 1,
        'edge_label_color': 'black!60',
        'node_style': '{draw=none}',
        'keep_aspect_ratio': False,
    }
    print(filename)
    plot(
        G,
        '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(
            filename),
        **styleG, **styleAdd, standalone=False)


def plot_spring_cevt_FR(cypherTxt, style,
                        pidMax=20,
                        con=False,
                        rls='stv03',
                        lc='fo5',
                        wscl=False
                        ):
    filename = 'spring_layout_cevt_FR_{}_{}'.format(rls, lc)

    G = gm.get_graph(
        cypherTxt, style.nodeColor, pidMax=pidMax, sTxt='.*{}.*{}.*'.format(rls, lc), wscl=wscl)

    pos = nx.spring_layout(G, weight='weight')
    styleG = style.style(G, pos)
    styleG['vertex_label'] = ['' for u in G.nodes()]
    styleG['edge_color'] = 'gray!40'
    styleG['margin'] = 0.3
    styleAdd = {
        'canvas': (10, 10),
        'vertex_size': 0.2,
        'edge_label_color': 'black!60',
        'node_style': '{draw=none}',
        'keep_aspect_ratio': False,
    }
    plot(
        G,
        # '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(filename),
        **styleG, **styleAdd, standalone=False)


def plot_spring_cevt_fd_w2(cypherTxt, style,
                           pidMax=20,
                           con=False,
                           rls='stv03',
                           lc='fo5',
                           wscl=False
                           ):
    filename0 = 'spring_layout_cevt_FA2_{}_{}'.format(rls, lc)

    oem = oems.oems('CEVT')
    errList = '", "'.join(oem.err['release'][rls][lc]['errList'])

    cypherTxt = cypherTxt.format('.*{}.*{}.*'.format(rls, lc), errList, pidMax)
    G = gm.get_graph(cypherTxt, style.nodeColor, w=wscl)

    figTex = '''
    \\begin{{subfigure}}[b]{{0.16\\textwidth}}
        \centering
        \includegraphics[width=\\textwidth]{{images/plot/{}.pdf}}
        % \caption{{{}}}
        \label{{{}}}
    \end{{subfigure}}%
    \hfill'''
    outTex = ''
    wi = 1
    sr = 2
    out_list_manual = [
        [19, 20], [50, 51], [40, 41, 42], [118, 48], [43, 44, 45, 47], [1, 97]]
    flt = [0, 3, 4, 6]
    flt = [1, 2, 3, 4, 5, 6]
    flt = [1, 2, 3]
    fi_old = 0
    itr = 3

    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=False,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=wi,

        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=sr,
        strongGravityMode=False,
        # gravity=1.0,

        # Log
        verbose=True)
    pos = forceatlas2.forceatlas2_networkx_layout(
        G, pos=None, iterations=10000)

    for fi in flt:
        # for itr in [10e8, 10e9, 10e10]:
        # fi = 4
        filename = '{}_flt{}_w{}_sr{}_itr{}_2'.format(
            filename0, fi, wi, sr, itr)
        outTex += figTex.format(filename, 'fltr ' + str(fi), 'filename')
        print(outTex)

        out_list = sum(out_list_manual[fi_old:fi], [])
        print(out_list)

    # -------------------------------------------------------------
    # save fig with marked nodes to remove
        styleG = style.style(G, pos)
        styleG['vertex_label'] = ['' for u in G.nodes()]
        styleG['edge_color'] = 'gray!40'
        styleG['margin'] = 0.8
        vsize = [0.4 for u in G.nodes()]
        for i, n in enumerate(G.nodes()):
            if n in out_list:
                print(n)
                styleG['vertex_color'][i] = 'red'
                vsize[i] = 0.8
                styleG['vertex_label'][i] = n
                styleG['vertex_label_position'][i] = 'below'
        styleAdd = {
            'canvas': (20, 20),
            'vertex_size': vsize,
            'edge_label_color': 'black!60',
            'node_style': '{draw=none}',
            'keep_aspect_ratio': False,
        }
        # nx.draw(G, with_labels=True, pos=pos)
        # plt.show()
        print(filename)
        plot(
            G,
            '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(
                filename),
            **styleG, **styleAdd, standalone=False)
    # -------------------------------------------------------------
        for n in out_list:
            G.remove_node(n)
        fi_old = fi

        pos = forceatlas2.forceatlas2_networkx_layout(
            G, pos=None, iterations=10000)


def plot_spring_cevt_fd_w(cypherTxt, style,
                          pidMax=20,
                          con=False,
                          rls='stv03',
                          lc='fo5',
                          wscl=False
                          ):
    filename0 = 'spring_layout_cevt_FA2_dMean_{}_{}'.format(rls, lc)
    # filename0 = 'spring_layout_cevt_FR_dMean_{}_{}'.format(rls, lc)

    oem = oems.oems('CEVT')
    errList = '", "'.join(oem.err['release'][rls][lc]['errList'])
    print(errList)
    cypherTxt = cypherTxt.format('.*{}.*{}.*'.format(rls, lc), errList, pidMax)
    print(cypherTxt)
    G = gm.get_graph(cypherTxt, style.nodeColor, w=wscl)

    figTex = '''
    \\begin{{subfigure}}[b]{{0.12\\textwidth}}
        \centering
        \includegraphics[width=\\textwidth]{{images/plot/{}.pdf}}
        \caption{{{}}}
        \label{{{}}}
    \end{{subfigure}}%
    \hfill'''
    outTex = ''
    wi = 1
    sr = 2
    itr = '2'
    flt = 0.8

    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=False,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=wi,
        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED
        # Tuning
        scalingRatio=sr,
        strongGravityMode=False,
        # gravity=1.0,
        # Log
        verbose=True)
    pos = forceatlas2.forceatlas2_networkx_layout(
        G, pos=None, iterations=10000)
    # pos = nx.spring_layout(G, weight='weight')  # FR

    for ri in range(0, 10):
        fi = flt
        print('---------------------------------------------------------')
        # filename = '{}_flt{}n{}_w{}_sr{}_itr{}'.format(filename0, fi, ri, wi, sr, itr)
        filename = '{}_flt{}n{}_itr{}'.format(filename0, fi, ri, itr)

        # pos = nx.shell_layout(G)

        df = pd.DataFrame()
        posMean = np.mean(np.asarray(list(pos.values())), axis=0)
        print(posMean)

        for n in G.nodes():
            nPos = np.asarray(pos[n])
            dist = np.linalg.norm(nPos - posMean)
            dfi = pd.DataFrame(np.array([[n, dist]]), columns=['n', 'dist'])
            df = df.append(dfi)

        df = df.sort_values(by=['dist'])
        dist_max = df.max()['dist']
        G2 = G

        print('Dist of nodes:')
        print(df)
        print('---------------------------')

        filtLimit = dist_max * fi
        dfilt = df[df['dist'] > filtLimit]
        print(df)

        print('low limit:', filtLimit)
        print('High dist edges:')
        print(dfilt)
        print('---------------------------')

        rNodes = [int(dfilt.n.tolist()[i]) for i in range(len(dfilt))]
        print(rNodes)
        # ------------------------------------------------------
        styleG = style.style(G, pos)
        styleG['vertex_label'] = ['' for u in G.nodes()]
        GNodes = G.nodes(data=True)
        pair_out = []
        for p in rNodes:
            pair = list(list(G.edges(p))[0])
            pair.remove(p)
            if not pair[0] in pair_out:
                pair_out.append(pair[0])

        vsize = [0.2 for u in G.nodes()]
        styleG['edge_color'] = 'gray!40'
        for i, n in enumerate(G.nodes()):
            if n in rNodes:
                print(n)
                styleG['vertex_color'][i] = 'red'
                vsize[i] = 0.4
                styleG['vertex_label'][i] = n
                styleG['vertex_label_position'][i] = 'below'
            elif n in pair_out:
                styleG['vertex_label'][i] = GNodes[n]['name']
                # print(styleG['vertex_label'][i])
                print(GNodes[n]['name'])
            else:
                styleG['vertex_label'][i] = ''
        styleAdd = {
            'canvas': (10, 10),
            'vertex_size': vsize,
            'edge_label_color': 'black!60',
            'node_style': '{draw=none}',
            'keep_aspect_ratio': False,
        }

        # nx.draw(G, with_labels=True, pos=pos)
        # plt.show()
        if ri < 10:
            plot(
                G,
                # '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.   format  (filename),
                **styleG, **styleAdd, standalone=False)
        # ------------------------------------------------------

        print('removed nodes:')
        for ni in rNodes:
            print(ni)
            G.nodes(data=True)[ni]
            G.remove_node(ni)

        print('---------------------------')

        print('removed free nodes')
        unattach_node = [n for n in G.nodes() if G.degree(n) == 0]
        for n in unattach_node:
            G.remove_node(n)
            rNodes.append(n)

            print(n)
        print('---------------------------')

        # l_caption = list(filter(lambda a: a != '', styleG['vertex_label']))
        # caption = 'fltr ' + str(fi) + ', ' + ', '.join([str(n) for n in l_caption])
        caption = 'fltr ' + str(fi) + ', ' + \
            ', '.join([str(n) for n in rNodes])
        outTex += figTex.format(filename, caption, 'filename')
        print(outTex)
        # pos = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=10000)

        pos = nx.spring_layout(G, weight='weight')  # FR


def plot_spring_yaris_fd_w(cypherTxt, style,
                           pidMax=20,
                           con=False,
                           rls='',
                           lc='',
                           wscl=False
                           ):
    filename0 = 'spring_layout_yaris_FA2_dMean_{}_{}'.format(rls, lc)
    # filename0 = 'spring_layout_yaris_FR_dMean_{}_{}'.format(rls, lc)

    cypherTxt = cypherTxt.format('.*{}.*{}.*'.format(rls, lc), [], pidMax)
    G = gm.get_graph(cypherTxt, style.nodeColor, w=wscl)

    figTex = '''
    \\begin{{subfigure}}[b]{{0.12\\textwidth}}
        \centering
        \includegraphics[width=\\textwidth]{{images/plot/{}.pdf}}
        \caption{{{}}}
        \label{{{}}}
    \end{{subfigure}}%
    \hfill'''
    outTex = ''
    wi = 1
    sr = 2
    itr = '2'
    flt = 0.8

    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=False,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=wi,
        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED
        # Tuning
        scalingRatio=sr,
        strongGravityMode=False,
        # gravity=1.0,
        # Log
        verbose=True)
    # pos = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=10000)
    pos = nx.spring_layout(G, weight='weight')  # FR

    for ri in range(0, 10):
        fi = flt
        print('---------------------------------------------------------')
        # filename = '{}_flt{}n{}_w{}_sr{}_itr{}'.format(filename0, fi, ri, wi, sr, itr)
        filename = '{}_flt{}n{}_itr{}'.format(filename0, fi, ri, itr)

        # pos = nx.shell_layout(G)

        df = pd.DataFrame()
        posMean = np.mean(np.asarray(list(pos.values())), axis=0)
        print(posMean)

        for n in G.nodes():
            nPos = np.asarray(pos[n])
            dist = np.linalg.norm(nPos - posMean)
            dfi = pd.DataFrame(np.array([[n, dist]]), columns=['n', 'dist'])
            df = df.append(dfi)

        df = df.sort_values(by=['dist'])
        dist_max = df.max()['dist']
        G2 = G

        print('Dist of nodes:')
        print(df)
        print('---------------------------')

        filtLimit = dist_max * fi
        dfilt = df[df['dist'] > filtLimit]

        print('low limit:', filtLimit)
        print('High dist edges:')
        print(dfilt)
        print('---------------------------')

        rNodes = [int(dfilt.n.tolist()[i]) for i in range(len(dfilt))]
        print(rNodes)
        # ------------------------------------------------------
        styleG = style.style(G, pos)
        # styleG['vertex_label'] = ['' for u in G.nodes()]
        vsize = [0.2 for u in G.nodes()]
        styleG['edge_color'] = 'gray!40'
        for i, n in enumerate(G.nodes()):
            if n in rNodes:
                print(n)
                styleG['vertex_color'][i] = 'red'
                vsize[i] = 0.4
                # styleG['vertex_label'][i] = n
                styleG['vertex_label_position'][i] = 'below'
            else:
                styleG['vertex_label'][i] = ''
        styleAdd = {
            'canvas': (10, 10),
            'vertex_size': vsize,
            'edge_label_color': 'black!60',
            'node_style': '{draw=none}',
            'keep_aspect_ratio': False,
        }

        # nx.draw(G, with_labels=True, pos=pos)
        # plt.show()
        if ri < 10:
            plot(
                G,
                '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.   format(
                    filename),
                **styleG, **styleAdd, standalone=False)
        # ------------------------------------------------------

        print('removed nodes:')
        for ni in rNodes:
            print(ni)
            G.nodes(data=True)[ni]
            G.remove_node(ni)

        print('---------------------------')

        print('removed free nodes')
        unattach_node = [n for n in G.nodes() if G.degree(n) == 0]
        for n in unattach_node:
            G.remove_node(n)
            rNodes.append(n)

            print(n)
        print('---------------------------')

        # l_caption = list(filter(lambda a: a != '', styleG['vertex_label']))
        # caption = 'fltr ' + str(fi) + ', ' + ', '.join([str(n) for n in l_caption])
        caption = 'fltr ' + str(fi) + ', ' + \
            ', '.join([str(n) for n in rNodes])
        outTex += figTex.format(filename, caption, 'filename')
        print(outTex)
        # pos = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=10000)

        pos = nx.spring_layout(G, weight='weight')  # FR


def plot_spring_cevt_simrank_forceatlas(cypherTxt, style,
                                        pidMax=20,
                                        con=False,
                                        rls='stv03',
                                        lc='fo5',
                                        ):

    sLimit = 0
    evd = True
    sprd = True
    wscl = 1000
    filename = 'spring_layout_cevt_simrank_{}_{}'.format(rls, lc)

    cypherTxt = cypherTxt.format('.*{}.*{}.*'.format(rls, lc), [], pidMax)
    G = gm.get_graph(cypherTxt, style.nodeColor, w=wscl)

    # sum_w = sum([G[u][v]['weight'] for u, v in G.edges()])
    # for u, v in G.edges():
    #     G[u][v]['weight'] = abs(G[u][v]['weight']/sum_w)

    source, btw = nx.bipartite.sets(G)
    simMatrix = gm.simrank_pp2_similarity_numpy(
        G, max_iterations=100000000, evd_opt=evd, sprd_opt=sprd, source=list(source))

    G = gm.add_simsim(G, simMatrix, sLimit)
    G2 = gm.subGraph_sim(G)

    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=False,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=0.5,

        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=1.0,
        strongGravityMode=False,
        # gravity=1.0,

        # Log
        verbose=True)
    # pos = forceatlas2.forceatlas2_networkx_layout(G2, pos=None, iterations=5000)
    # pos = nx.kamada_kawai_layout(G2, weight='weight')
    pos = nx.spring_layout(G, weight='weight')

    styleG = style.style(G2, pos)
    styleG['vertex_label'] = ['' for u in G.nodes()]
    styleG['edge_color'] = 'gray!40'
    styleG['margin'] = 0.3
    styleAdd = {
        'canvas': (10, 10),
        'vertex_size': 0.2,
        'edge_label_color': 'black!60',
        'node_style': '{draw=none}',
        'keep_aspect_ratio': False,
    }
    plot(
        G2,
        # '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(filename),
        **styleG, **styleAdd, standalone=False)


def plot_spring_cevt_KK(cypherTxt, style,
                        pidMax=20,
                        con=False,
                        rls='stv03',
                        lc='fp3',
                        wscl=False
                        ):

    filename = 'spring_layout_cevt_KK_{}_{}'.format(rls, lc)

    cypherTxt = cypherTxt.format('.*{}.*{}.*'.format(rls, lc), [], pidMax)
    G = gm.get_graph(cypherTxt, style.nodeColor, w=wscl)

    pos = nx.kamada_kawai_layout(G, weight='weight')
    styleG = style.style(G, pos)
    styleG['vertex_label'] = ['' for u in G.nodes()]
    styleG['edge_color'] = 'gray!40'
    styleG['margin'] = 0.3
    styleAdd = {
        'canvas': (10, 10),
        'vertex_size': 0.2,
        'edge_label_color': 'black!60',
        'node_style': '{draw=none}',
        'keep_aspect_ratio': False,
    }
    plot(
        G,
        # '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(filename),
        **styleG, **styleAdd, standalone=False)


def plot_spring_cevt_forceatlas(cypherTxt, style,
                                pidMax=15,
                                con=False,
                                rls='stv03',
                                lc='fp3',
                                wscl=False
                                ):

    filename2 = 'spring_layout_cevt_FA2_{}_{}_pid{}_wErr'.format(
        rls, lc, pidMax)
    filename1 = 'spring_layout_cevt_FA2_{}_{}_pid{}_noErr'.format(
        rls, lc, pidMax)

    oem = oems.oems('CEVT')
    errList = '", "'.join(oem.err['release'][rls][lc]['errList'])
    cypherTxt1 = cypherTxt.format(
        '.*{}.*{}.*'.format(rls, lc), errList, pidMax)
    cypherTxt2 = cypherTxt.format('.*{}.*{}.*'.format(rls, lc), '', pidMax)
    G1 = gm.get_graph(cypherTxt1, style.nodeColor, w=wscl)
    G2 = gm.get_graph(cypherTxt2, style.nodeColor, w=wscl)

    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=False,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=10.0,

        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=2.0,
        strongGravityMode=False,
        # gravity=1.0,

        # Log
        verbose=True)

    # pos1 = forceatlas2.forceatlas2_networkx_layout(G1, pos=None, iterations=5000)
    # styleG1 = style.style(G1, pos1)
    # styleG1['vertex_label'] = ['' for u in G1.nodes()]
    # styleG1['edge_color'] = 'gray!40'
    # styleG1['margin'] = 0.3
    # styleAdd1 = {
    #     'canvas': (20, 20),
    #     'vertex_size': 0.2,
    #     'edge_label_color': 'black!60',
    #     'node_style': '{draw=none}',
    #     'keep_aspect_ratio': False,
    # }
    # plot(G1,
    #     '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(filename1),
    #     **styleG1, **styleAdd1, standalone=False)
    # -------------------------------------------------
    # pos2 = forceatlas2.forceatlas2_networkx_layout(G2, pos=None, iterations=5000)
    # print(pos2)
    pos2 = {
        0: (-195.0145211594972, 183.6363342344237), 1: (-136.90818931829756, 74.83801650693968), 2: (-153.1377244211523, 160.85040722022865), 3: (-165.51565285371188, 118.95922828185178), 4: (-188.18361607549315, 150.53225270770506), 5: (-136.17934865785455, 109.92683689995778), 6: (-227.14281465177655, 207.93218948322283), 7: (-136.5893552656457, 226.0654437302483), 8: (-226.7668586286411, 183.70788919270538), 9: (-160.3002088600143, 200.3481874972534), 10: (-46.294296333977826, 170.92121062437312), 11: (-84.77665670198559, 99.67553012026615), 12: (-242.88271316693115, 191.0175557757347), 13: (-125.53139086463244, 195.42216300200528), 14: (-117.57403027857872, 236.7621374017818), 15: (-144.29331652842757, 184.530837357448), 16: (-109.59700940730687, 157.58275348976915), 17: (-49.834874541144615, 107.21347056700122), 18: (-131.77043928775825, 149.98444977462998), 19: (-151.22589711751246, 24.697749075261594), 20: (-120.75757564153734, 104.20710787954268), 21: (-91.33827619811845, 204.7207573249423), 22: (-60.6945257676981, 219.50331069512544), 23: (-96.39219834818148, 133.26615122566105), 24: (-120.94824012851613, 177.8977219885887), 25: (-184.64687510128587, 195.73741247220264), 26: (-205.89738263316877, 240.37269314480284), 27: (-81.92534371711282, 183.66130332078345), 28: (-126.61923044571657, 182.43169001559224), 29: (-229.15683303382673, 159.62832851815227), 30: (-85.54158687355104, 46.671138867988546), 31: (-48.52964879603011, -3.093688231343952), 32: (-93.9390107257155, 150.46274339701236), 33: (-109.51941310837395, 190.08569007518832), 34: (-88.79786432336186, 255.23652474231739), 35: (-148.04978618948, 95.74322906395295), 36: (-136.35911613462352, 137.70769186424215), 37: (-135.4393104482334, 130.3570050586746), 38: (-72.93616546645676, 71.77853407090373), 39: (-83.5110428800289, 71.43618008569877), 40: (-83.56186423236493, 78.93804569100753), 41: (-82.10124260870776, 118.39464631579125), 42: (-57.75429255359836, 52.18223778172256), 43: (-1.8513351538402854, 3.3328982073346207), 44: (-71.93867544930092, 81.32881009670606), 45: (-108.29125987189391, 119.42061120166677), 46: (-99.59486069897413, 116.12392552082527), 47: (-118.62488381078266, 158.8960835942792), 48: (-80.31124287206846, 135.53651898834212), 49: (-115.16575683939799, 127.54997071836969), 50: (-115.24327861933418, 109.60986303916515), 51: (-82.63015431514941, 163.4831884617282), 52: (-95.73765704131051, 169.1874803647365), 53: (-90.43905376593251, 158.2791728218582), 54: (-81.26134610622874, 127.35296385956914), 55: (-101.79362025720985, 161.44555589281924), 56: (-81.39690810916967, 145.4090024168162), 57: (-86.71038815415716, 150.7939692552554), 58: (-120.10256371309667, 150.06566491550396), 59: (-110.36984614115245, 168.9727690232205), 60: (-128.60583526558722, 60.27311430934553), 61: (-112.12835935831698, 136.09854974566116), 62: (-34.61616591742576, 116.69379116443825), 63: (16.234237252497874, 119.4524499275572), 64: (-42.057680024129525, 127.81912594607662), 65: (-117.67911485828674, 56.146964948549), 66: (-117.37107802884063, 62.62976703417121), 67: (-113.84461070236411, 93.48992458483436), 68: (-72.10950705290125, 127.3670055529483), 69: (-112.96795269146483, 149.02456751878458), 70: (-107.43780779107702, 63.217152759944526), 71: (-120.85619696563329, 140.6478509217781), 72: (-107.73712369233527, 151.9785008696027), 73: (-113.60688708706029, 82.39943117819571), 74: (-101.12970915762236, 147.92084122873374), 75: (-108.12894017713369, 131.22755319873676), 76: (-45.88563429630964, 144.5194609302027), 77: (-71.12257260376246, 137.1443504620346), 78: (-103.74161973812036, 77.95509290714337), 79: (-108.4724990066507, 142.0148884047768), 80: (-123.66609633339233, 89.99288405348115), 81: (-110.12267634415333, 51.57570412048834), 82: (-104.51225379774016, 84.53978002114849), 83: (-116.01037125390248, 76.25302342968635), 84: (-113.93363296946818, 70.40179044684668), 85: (-105.29363471517223, 106.17003908445338), 86: (-102.12252082575192, 70.4280984407515), 87: (-101.13611736450244, 135.75809426839857), 88: (-90.87115744016309, 122.85874814292053), 89: (-90.23645126380042, 131.14030976355528), 90: (-135.99786105456994, 54.75169677488042), 91: (-90.09145799876795, 142.6819354314804), 92: (-100.66583730016899, 125.11844641019312), 93: (-91.24570564525557, 115.11782920755189), 94: (-12.102023898158995, -153.32920001053182), 95: (-5.092202710033097, -177.2265526665563), 96: (-3.0536366412100926, -172.10546225277523), 97: (-0.944245654635148, -183.79404838083522), 98: (0.5373476535026995, -177.50312319993873), 99: (5.24766903434795, -172.96625198130445), 100: (6.537047121680963, -181.29160213641848), 101: (-6.566444756311748, -183.0247065921026), 102: (-167.05088808784157, 51.19333041679386), 103: (-226.20336942576782, 41.26944685344664), 104: (-181.5869823700376, -24.0683989436015), 105: (-92.16860349658113, 69.03021420978496), 106: (-75.05796910071787, 150.47554354824064), 107: (-90.93391089451958, 137.34670444683036), 108: (-155.6907517261583, 83.40905300450073), 109: (-182.27256336480963, 96.52837089877116), 110: (-242.47399525074695, 69.32364297661198), 111: (-214.08910188601828, 70.46036770442481), 112: (-170.16405740541867, 88.83295059328447), 113: (-255.30002387710275, 93.19453845133417), 114: (-219.49170824577325, 125.67235076445006), 115: (-201.0505413942112, 69.28350089530319), 116: (-189.5524889200313, 48.03408908749365), 117: (-206.31466343658937, 55.508346592177574), 118: (-202.29251619964361, 78.96827389139118), 119: (-203.3827014808842, 102.2329761974917), 120: (-165.92952206749234, 64.84266151595345), 121: (-217.2869832887078, 83.70355111274101), 122: (-182.14903819667478, 34.488897022054886), 123: (-182.51891465847098, 78.59366397426597), 124: (-199.1279517004158, 110.13192799654233), 125: (-208.7988089228852, 80.28168560302987), 126: (-210.3635186269659, 66.97752388901121), 127: (-220.34395133723555, 98.09498284108014), 128: (-183.11120100060907, 85.85652401798414), 129: (-192.89043341873182, 104.30613332301685), 130: (-199.4042526254212, 90.90320262004938), 131: (-239.3421695807582, 108.3680898635189), 132: (-305.7175027059267, 116.33565152250256), 133: (-193.9821916662167, 54.916352982072496), 134: (-194.34513964601416, 71.1183973910825), 135: (-197.25248198201191, 62.587736316332524), 136: (-189.88841738200873, 88.36993242349558), 137: (-222.15196216730857, 107.9777010549335), 138: (-188.68729253169602, 110.18627158720189), 139: (-181.64526648113676, 70.63560923658542), 140: (-171.34678815677515, 71.01673790275872), 141: (-187.34313084888728, 62.549177599719926), 142: (-248.97494679532582, 126.47350661123915), 143: (-306.4777443120219, 131.3986912579607), 144: (-212.97503253929835, 93.07621211806575), 145: (-193.40436068036175, 95.79099050618875), 146: (-214.21480819324952, 118.27632377773708), 147: (-206.70320854791666, 124.93341217463909)}

    styleG2 = style.style(G2, pos2)
    styleG2['vertex_label'] = ['' for u in G2.nodes()]
    styleG2['edge_color'] = 'gray!40'
    styleG2['margin'] = 0.3
    styleAdd2 = {
        'canvas': (20, 20),
        'vertex_size': 0.25,
        'edge_label_color': 'black!60',
        'node_style': '{draw=none}',
        'keep_aspect_ratio': False,
    }
    plot(G2,
         '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(
             filename2),
         **styleG2, **styleAdd2, standalone=False)


def plot_bundle_cevt(cypherTxt, style,
                     pidMax=15,
                     con=False,
                     rls='stv03',
                     lc='fp3',
                     ):

    filename = 'edge_bundle_cevt_FA2_{}_{}'.format(rls, lc)

    cypherTxt = cypherTxt.format('.*{}.*{}.*'.format(rls, lc), [], pidMax)
    G = gm.get_graph(cypherTxt, style.nodeColor, w=wscl)

    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=False,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=10.0,

        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=2.0,
        strongGravityMode=False,
        # gravity=1.0,

        # Log
        verbose=True)
    pos = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=5000)
    input_edges = feb.net2edges(G, positions=pos)
    output_lines = feb.forcebundle(input_edges)
    print(output_lines)
    # bG = feb.lines2net(output_lines)

    styleG = style.style(bG, pos)
    styleG['vertex_label'] = ['' for u in bG.nodes()]
    styleG['edge_color'] = 'gray!40'
    styleG['margin'] = 0.3
    styleAdd = {
        'canvas': (10, 10),
        'vertex_size': 0.2,
        'edge_label_color': 'black!60',
        'node_style': '{draw=none}',
        'keep_aspect_ratio': False,
    }
    plot(
        bG,
        # '../publication/06_KG_energyAbsorption/images/plot/{}.pdf'.format(filename),
        **styleG, **styleAdd, standalone=False)


def plot_simrankpp(cypherTxt, style):

    # ----------------------------------------
    # result for weighted graph with pidMax change
    # ----------------------------------------
    # print_yaris_simrank_result(cypherTxt, 's-evd-we8P-sprd 2', 2, wscl=10e8, sprd=True, evd=True)
    # print_yaris_simrank_result(cypherTxt, 's-evd-we8P-sprd 5', 5, wscl=10e8, sprd=True, evd=True)
    # print_yaris_simrank_result(cypherTxt, 's-evd-we8P-sprd 15', 15, wscl=10e8, sprd=True, evd=True)
    # print_yaris_simrank_result(cypherTxt, 's-evd-we8P-sprd 28', 28, wscl=10e8, sprd=True, evd=True)

    # ----------------------------------------
    # result for weighted graph with IE
    # ----------------------------------------
    # print_yaris_simrank_result(cypherTxt, 's, 5', 5, wscl=False, sprd=False, evd=False)
    # print_yaris_simrank_result(cypherTxt, 's-wIE 5', 5, wscl=1, sprd=False, evd=False)
    # print_yaris_simrank_result(cypherTxt, 's-evd-wIE 5', 5, wscl=1, sprd=False, evd=True)
    # print_yaris_simrank_result(cypherTxt, 's-evd-we6IE-sprd 5', 5, wscl=10e6, sprd=True, evd=True)

    # ----------------------------------------
    # result for weighted graph with P
    # ----------------------------------------
    # print_yaris_simrank_result(cypherTxt, 's, 5', 5, wscl=False, sprd=False, evd=False)
    # print_yaris_simrank_result(cypherTxt, 's-wP 5', 5, wscl=1, sprd=False, evd=False)
    # print_yaris_simrank_result(cypherTxt, 's-evd-wP 5', 5, wscl=1, sprd=False, evd=True)
    # print_yaris_simrank_result(cypherTxt, 's-evd-we8P-sprd 5', 5, wscl=10e8, sprd=True, evd=True)

    # ----------------------------------------
    # scaling weight, spred from 0-2,3,4
    # ----------------------------------------
    print_yaris_simrank_result(
        cypherTxt, 's-evd-we8P-sprd 5 1.6', 5, wscl=10e8, sprd=True, evd=True)
    print_yaris_simrank_result(
        cypherTxt, 's-evd-we8P-sprd 5 1', 5, wscl=1634664833 / 1, sprd=True, evd=True)
    # print_yaris_simrank_result(cypherTxt, 's-evd-we8P-sprd 5', 5, wscl=1634664833 / 2, sprd=True, evd=True)
    # print_yaris_simrank_result(cypherTxt, 's-evd-we8P-sprd 5', 5, wscl=1634664833 / 3, sprd=True, evd=True)
    # print_yaris_simrank_result(cypherTxt, 's-evd-we8P-sprd 5', 5, wscl=1634664833 / 4, sprd=True, evd=True)
    # print_yaris_simrank_result(cypherTxt, 's-evd-we8P-sprd 5', 5, wscl=1634664833 / 8, sprd=True, evd=True)
    return

    # ----------------------------------------
    # from this has not re-runed after debuging simrank
    # ----------------------------------------
    pidMax = 8
    sLimit = 0
    evd = True
    sprd = True
    wscl = 10e8

    # si = 11
    # mapping = {}
    # nodesD = G.nodes(data=True)
    # for u in nodesD:
    #     if u[1]['label'] == 'Sim':
    #         G = nx.relabel_nodes(G, {u[0]: si})
    #         si += 1
    #         u[1]['name'] = '0' + str(int(u[1]['name']) - 3)

    cypherTxt = cypherTxt.format('', 5)
    # wscl scaling the weight
    G = gm.get_graph(cypherTxt, style.nodeColor, w=wscl)
    simMatrix = gm.simrank_pp2_similarity_numpy(
        G, max_iterations=1000000, evd_opt=evd, sprd_opt=sprd)

    G = gm.add_simsim(G, simMatrix, sLimit=sLimit)
    G2 = gm.subGraph_sim(G)
    nodsD = G2.nodes(data=True)

    # print(nx.get_edge_attributes(G2, 'weight'))

    pos = nx.shell_layout(G2)
    styleG = style.style(G2, pos, w='weight')
    styleG['edge_color'] = 'gray!40'
    style.node_label_pos['Des'] = '180'
    styleAdd = {
        'canvas': (8, 8),
        'edge_curved': 0.2,
        'edge_label_distance': 0.3,
        'vertex_size': 0.8,
        'edge_label_color': 'black!80',
        'edge_label_size': 10,
        'node_style': '{draw=white}',
    }
    # plot(
    #     G2,
    #     # '../publication/06_KG_energyAbsorption/images/tikz/simrankpp.tex',
    #     **styleG, **styleAdd,  standalone=False)


def print_yaris_simrank_result(cypherTxt, name, pidMax, wscl=False, sprd=False, evd=False):

    data = {}
    cypherTxt = cypherTxt.format('', pidMax)
    # wscl scaling the weight
    G = gm.get_graph(cypherTxt, style.nodeColor, w=wscl)
    _, _, data[name], top = gm.simRankpp(
        G, pidMax, 0.0, wscl=wscl, sprd=sprd, evd=evd)
    print(top)
    # -----------------------------
    # get interesting relations
    int_rel_simName = [
        [3, 4], [1, 3], [1, 4], [2, 3], [2, 4], [1, 2]
    ]
    int_rel_id = []
    for ri in int_rel_simName:
        ids = []
        ss = ['0' + str(x + 3) for x in ri]

        for n in top:
            nt = G.nodes(data=True)[n]
            name = nt['name']
            if name in ss:
                ids.append(n)
        int_rel_id.append(ids)

    print('==================================')
    print(int_rel_id)
    for d in data:
        print(d)
        print('---------------------')
        for i, r in enumerate(int_rel_id):
            u, v = r[0], r[1]
            un, vn = int_rel_simName[i]
            # print(u, v, r, top)
            print(un, '-', vn, '|', data[d][u][v])


def plot_simrankpp_cevt(cypherTxt, style):
    pidMax = 20
    sLimit = 0.1
    evd = True
    sprd = True
    wscl = 10000

    dst = '../publication/06_KG_energyAbsorption/images/plot/simrank_cevt.pdf'
    cypherTxt = cypherTxt.format('.*stcr.*fp3.*', pidMax)
    G = gm.get_graph(cypherTxt, style.nodeColor, w=wscl)

    MEDIUM_SIZE = 12
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    # --------------------------------
    # add edge for symmetric parts
    # evd = False
    # ---------
    # gData = G.nodes(data=True)
    # names = [ni[1]['name'] for ni in gData]
    # for pair in [[2000001, 2000501], [2000002, 2000502]]:
    #     new_edge = []
    #     for n in pair:
    #         new_edge.append(names.index(n))
    #     G.add_edge(new_edge[0], new_edge[1], type='DES_SYM')

    source, btw = nx.bipartite.sets(G)
    simMatrix = gm.simrank_pp2_similarity_numpy(
        G, max_iterations=100000000, evd_opt=evd, sprd_opt=sprd, source=list(source))

    data = {}
    data['sprd,evd,10e3'] = gm.simRankpp(
        pidMax, 0.0, wscl=wscl, sprd=True, evd=True)

    fig = plt.figure(figsize=(4.5, 3))
    ax = sns.distplot(
        data['sprd,evd,10e3'], kde=True, rug=True, hist=False,
        axlabel='SIM_SIM link predection score',
        # aylabel='Number of simulation density'
    )
    # fig.set_yscale('log')
    ticks = [5, 10, 15, 20]
    xticks = [0.15, 0.3, 0.45]
    # fig.set_yticks(ticks)
    ax.set(yticks=ticks, xticks=xticks)
    plt.subplots_adjust(left=0.12, right=0.975, top=0.93, bottom=0.16)

    # fig.set(size=(3.1, 3.1))
    fig.savefig(dst)
    plt.show()


def plot_simrankpp_cevt_nprt(cypherTxt, style,
                             pidMax=20,
                             sLimit=0,
                             evd=True,
                             sprd=True,
                             # wscl=10e5,  # IE
                             wscl=10e4,  # P
                             rls='stcr',
                             lc='fp3',
                             errList=[],
                             wc=0.9
                             ):

    MEDIUM_SIZE = 12
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    # --------------------------------

    sims = '.*{}_.*{}.*'.format(rls, lc)
    name = 'simrank_cevt_{}_{}_{}_wPe4_.pdf'.format(lc, rls, pidMax)
    dst = '../publication/06_KG_energyAbsorption/images/plot/{}'.format(name)

    cypherTxt = cypherTxt.format(sims, '", "'.join(errList), pidMax)
    G = gm.get_graph(
        cypherTxt, style.nodeColor, w=wscl)

    G, simsim, simMatrix, top = gm.simRankpp(
        G, pidMax, sLimit, wscl=wscl, sprd=True, evd=True)

    if not simsim:
        return(None)

    inv = gm.simrank_inv(simMatrix, G, top, simsim)
    df = pd.DataFrame(data=inv.density())
    inv.upper_range(wc)
    # inv.get_sim(['226_001', '330_001'])

    # -----------------------
    # Plotly Histogram
    # -----------------------
    # fig = px.histogram(
    #     df, x='score', marginal="rug", hover_data=df.columns)
    # fig.show()

    # -----------------------
    # matplotlib density plot
    # -----------------------
    fig = plt.figure(figsize=(4.5, 3))
    ax = sns.distplot(
        df.score, kde=True, hist=True, rug=True,
        # axlabel='SIM_SIM link predection score',
        label=rls
    )
    ax.legend()
    ax.set_title('{0} Parts'.format(pidMax), y=1.0, pad=-14)
    plt.subplots_adjust(left=0.15, right=0.95, top=0.93, bottom=0.16)

    fig.savefig(dst)
    return(name)


def plot_simrankpp_single(cypherTxt, style,
                          pidMax=20,
                          sLimit=0,
                          evd=True,
                          sprd=True,
                          # wscl=10e5,  # IE
                          wscl=10e4,  # P
                          errList=[],
                          wc=0.9
                          ):

    MEDIUM_SIZE = 12
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    # --------------------------------

    sims = '.*'
    cypherTxt = cypherTxt.format(sims, '", "'.join(errList), pidMax)
    G = gm.get_graph(
        cypherTxt, style.nodeColor, w=wscl)

    G, simsim, simMatrix, top = gm.simRankpp(
        G, pidMax, sLimit, wscl=wscl, sprd=True, evd=True)

    inv = gm.simrank_inv(simMatrix, G, top, simsim)
    df = pd.DataFrame(data=inv.density())

    # -----------------------
    # matplotlib density plot
    # -----------------------
    # ax = sns.displot(
    # df.score, kde=True,
    # height=4.5, aspect=4.5 / 3,
    # palette=p
    # )
    fig = plt.figure(figsize=(4.5, 3))
    ax = sns.distplot(
        df.score, kde=False,)  # , hist=True, rug=True,
    ax.set(
        xlabel='SIM_SIM link predection score',
        ylabel='Count'
    )
    ax2 = plt.twinx()
    ax2 = sns.distplot(
        df.score, kde=True, hist=False, ax=ax2,
    )
    ax2.set_ylabel('')
    xticks = [0, 0.1, 0.2, 0.3]
    ax2.set(xticks=xticks)
    ax2.get_yaxis().set_visible(False)
    plt.subplots_adjust(left=0.17, right=0.87, top=0.95, bottom=0.18)

    # print(max(df.score))


def plot_simrankpp_cevt_single(cypherTxt, style,
                               pidMax=20,
                               sLimit=0,
                               evd=True,
                               sprd=True,
                               # wscl=10e5,  # IE
                               wscl=10e4,  # P
                               rls='stcr',
                               lc='fp3',
                               errList=[],
                               wc=0.9
                               ):

    MEDIUM_SIZE = 12
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    # --------------------------------

    sims = '.*{}_.*{}.*'.format(rls, lc)
    name = 'simrank_cevt_{}_{}_{}_wPe4_single.pdf'.format(lc, rls, pidMax)
    dst = '../publication/06_KG_energyAbsorption/images/plot/{}'.format(name)

    cypherTxt = cypherTxt.format(sims, '", "'.join(errList), pidMax)
    G = gm.get_graph(
        cypherTxt, style.nodeColor, w=wscl)

    G, simsim, simMatrix, top = gm.simRankpp(
        G, pidMax, sLimit, wscl=wscl, sprd=True, evd=True)

    inv = gm.simrank_inv(simMatrix, G, top, simsim)
    df = pd.DataFrame(data=inv.density())

    # -----------------------
    # matplotlib density plot
    # -----------------------
    # ax = sns.displot(
    # df.score, kde=True,
    # height=4.5, aspect=4.5 / 3,
    # palette=p
    # )
    fig = plt.figure(figsize=(4.5, 3))
    ax = sns.distplot(
        df.score, kde=False,)  # , hist=True, rug=True,
    ax.set(
        xlabel='SIM_SIM link predection score',
        ylabel='Count'
    )
    ax2 = plt.twinx()
    ax2 = sns.distplot(
        df.score, kde=True, hist=False, ax=ax2,
    )
    ax2.set_ylabel('')
    xticks = [0, 0.1, 0.2, 0.3]
    ax2.set(xticks=xticks)
    ax2.get_yaxis().set_visible(False)
    plt.subplots_adjust(left=0.17, right=0.87, top=0.95, bottom=0.18)

    # fig.savefig(dst)


def simrank_cevt_inv_lc_rls_npid(cypherTxt, style):

    rlss = ['stcr', 'stv0', 'stv03', 'm1']
    lcs = ['fp3', 'fod', 'fo5']
    # lcs = ['fo5']
    npid = [3, 5, 10, 12, 15, 17, 20]
    npid = [20, 17, 15, 12, 10, 5, 3]

    figTxt = '''
        \\begin{{subfigure}}[b]{{0.14\\textwidth}}
            \centering
            \includegraphics[width=\\textwidth]{{images/plot/{}}}
        \end{{subfigure}}%
        \hfill'''

    no_b_g = []
    for lc in lcs:
        outTxt = ''
        for rls in rlss:
            for n in npid:
                name = plot_simrankpp_cevt_nprt(
                    cypherTxt, style, pidMax=n, rls=rls, lc=lc)
                if name:
                    outTxt += figTxt.format(name, '', '')
                else:
                    no_b_g.append('_'.join([lc, rls, str(n)]))
                outTxt += '&'
            outTxt += '\\\\\n'
        print(outTxt)
        # input('wait')
    print(no_b_g)


def plot_simrankpp_cevt_cnvrg(cypherTxt0, style,
                              sLimit=0,
                              evd=True,
                              sprd=True,
                              # wscl=10e5,  # IE
                              wscl=10e4,  # P
                              rls='stcr',
                              lc='fp3',
                              errList=[],
                              wc=0.9):

    sims = '.*{}_.*{}.*'.format(rls, lc)
    # name = 'simrank_cevt_cnvrg_{}_{}_{}_wPe4_.pdf'.format(lc, rls)
    # dst = '../publication/06_KG_energyAbsorption/images/plot/{}'.format(name)

    d = {
        'nPID': [], 'H1': [], 'H2': [],
        'L1': [], 'L2': [], 'w:H1H2': [], 'w:H1L1': [], 'w:H2L2': []}

    for pidMax in range(2, 21, 1):
        cypherTxt = cypherTxt0.format(sims, '", "'.join(errList), pidMax)
        G = gm.get_graph(
            cypherTxt, style.nodeColor, w=wscl)

        G, simsim, simMatrix, top = gm.simRankpp(
            G, pidMax, sLimit, wscl=wscl, sprd=sprd, evd=evd)

        if not simsim is None:
            inv = gm.simrank_inv(simMatrix, G, top, simsim)
            d = inv.simRank_rng(pidMax, d)
        else:
            print('notbgraph', pidMax)

    df = pd.DataFrame(data=d)
    # print(df)
    print(df.to_latex(index=False, float_format="%.3f"))


def plot_simrankpp_HHLL(cypherTxt0, style,
                        sLimit=0,
                        evd=True,
                        sprd=True,
                        # wscl=10e5,  # IE
                        wscl=10e8,  # P
                        rls='',
                        lc='',
                        errList=[],
                        wc=0.9):

    sims = '.*'.format()

    d = {
        'nPID': [], 'H1': [], 'H2': [],
        'L1': [], 'L2': [], 'w:H1H2': [], 'w:H1L1': [], 'w:H2L2': []}

    for pidMax in range(15, 31, 5):
        cypherTxt = cypherTxt0.format(sims, '", "'.join(errList), pidMax)
        G = gm.get_graph(
            cypherTxt, style.nodeColor, w=wscl)

        G, simsim, simMatrix, top = gm.simRankpp(
            G, pidMax, sLimit, wscl=wscl, sprd=sprd, evd=evd)

        if not simsim is None:
            inv = gm.simrank_inv(simMatrix, G, top, simsim)
            d = inv.simRank_rng(pidMax, d)
        else:
            print('notbgraph', pidMax)

    df = pd.DataFrame(data=d)
    print(df)
    # print(df.to_latex(index=False, float_format="%.3f"))


if __name__ == '__main__':

    driver = GraphDatabase.driver(
        uri="bolt://localhost:7687", auth=("neo4j", "ivory123"))

    style = gm.cyTxt()

# SCHEMA
    # plot_schema(style.schema.txt, style)

# BIPARTITE
 # YARIS
    # plot_bipartite(style.sm.txt, style)  # yaris
 # CEVT
    # plot_bipartite_cevt_1(style.sm_name.txt, style)  # stv03 82 sim fp3, stcr cevt 50 sim fp3, stcr fo5
    # plot_bipartite_cevt_2(style.sm_name.txt, style)  # cevt 2 simulation

# Spring Layout
  # CEVT
    # plot_spring_cevt_fd_w2(style.sm_name.txt, style, lc='fp3', pidMax=20, wscl=1)  # cevt force-directedweighted
    # plot_spring_cevt_fd_w2(style.sm_name_err.txt, style, lc='fo5', pidMax=15, wscl=1, rls='stcr')  # cevt force-directedweighted
    # plot_spring_cevt_forceatlas(style.sm_name_err.txt, style, lc='fo5', rls='stcr', pidMax=8)  # cevt

  # off the method
    # for lc in ['fp3', 'fo5']:
    # plot_spring_cevt_FR(style.sm_name.txt, style, lc=lc, pidMax=20) #cevt
    # plot_spring_cevt_KK(style.sm_name.txt, style, lc=lc, pidMax=20) #cevt
    # plot_spring_cevt_forceatlas(style.sm_name.txt, style, lc=lc, pidMax=20) #cevt
    # plot_spring_cevt_FR(style.spem_name.txt, style, lc='fp3', pidMax=20)  # cevt, spem
    # plot_spring_cevt_KK(style.sm_name.txt, style, lc='fp3', pidMax=20)  # cevt
    # plot_spring_cevt_fd_w(style.sm_name_err.txt, style, lc='fo5', rls='stcr', pidMax=15, wscl=1)  # cevt force-directedweighted
    # plot_spring_cevt_simrank_forceatlas(style.sm_name_err.txt, style, lc='fo5', rls='stcr', pidMax=15)  # cevt

  # Yaris
    # plot_spring_yaris_forceatlas(style.sm.txt, style, pidMax=28, opt='_wp_28p')

  # off the method
    # plot_spring_yaris_fd_w2(style.sm_name.txt, style, lc='fp3', pidMax=20, wscl=1)  # cevt force-directedweighted
    # plot_spring_yaris_FR(style.sm.txt, style, pidMax=28, opt='_28p')
    # plot_spring_yaris_KK(style.sm.txt, style, pidMax=28, opt='_28p')

# Bundle graph:
    # plot_bundle_cevt(style.sm_name.txt, style)

# simrankpp
  # YARIS_BUMPER
    oem = oems.oems('YARIS_BUMPER')
    errList = oem.err['release']['']['']['errList']
    plot_simrankpp_single(style.sm_name_err.txt, style,
                          pidMax=30, wscl=10e8, errList=errList)
    plot_simrankpp_HHLL(style.sm_name_err.txt, style,
                        sLimit=0.0, errList=errList, wscl=10e8)
    # plt.show()
  # YARIS
    # plot_simrankpp(style.sm.txt, style)
  # CEVT
    # plot_simrankpp_cevt(style.sm_name.txt, style)
    # simrank_cevt_inv_lc_rls_npid(style.sm_name_err.txt, style)
    # -------------------------------------------------
    oem = oems.oems('CEVT')
    rls, lc = 'stcr', 'fo5'
    errList = oem.err['release'][rls][lc]['errList']
    # table of convergence
    # plot_simrankpp_cevt_cnvrg(style.sm_name_err.txt, style, rls=rls, lc=lc, sLimit=0.0, errList=errList)
    # KDE sample
    # plot_simrankpp_cevt_single(style.sm_name_err.txt, style, pidMax=15, rls=rls, lc=lc)
    plt.show()

  # off the method
    oem = oems.oems('CEVT')
    # rls, lc = 'stcr', 'fp3'
    # errList = oem.err['release'][rls][lc]['errList']
    # plot_simrankpp_cevt_nprt(style.sm_name_err.txt, style, pidMax=20, rls=rls, lc=lc, sLimit=0.0, errList=errList, wc=0.325243)

    rls, lc = 'stcr', 'fo5'
    errList = oem.err['release'][rls][lc]['errList']

    # plot_simrankpp_cevt_cnvrg(
    #     style.sm_name_err.txt, style, rls=rls,
    #     lc=lc, sLimit=0.0, errList=errList
    # )
    # plot_simrankpp_cevt_nprt(
    #     style.sm_name_err.txt, style, rls=rls,
    #     lc=lc, sLimit=0.0, errList=errList,
    #     pidMax=12, wc=0.306227)

    rls, lc = 'stv0', 'fod'
    errList = oem.err['release'][rls][lc]['errList']
    # plot_simrankpp_cevt_nprt(
    #     style.sm_name_err.txt, style, rls=rls,
    #     lc=lc, sLimit=0.0, errList=errList,
    # pidMax=3, wc=0.5888)  # 009_001-005_001 >>  227_001
    # pidMax=5, wc=0.5436)  # 001_001-011_001 >>  129_001
    # pidMax=7, wc=0.4945)  # 001_001-009_001 >>  330_001
    # pidMax=10, wc=0.4445)  # 226_001-330_001 >>  001_001
    # pidMax=12, wc=0.41667)  # 226_001-330_001 >>  001_001
    # pidMax=14, wc=0.3981)  # 226_001-330_001 >> 001_001
    # pidMax=15, wc=0.3894)  # 226_001-330_001 >> 004_001
    # pidMax=16, wc=0.3821)  # 226_001-330_001 >> 004_001-009_001
    # pidMax=17, wc=0.375985)  # 226_001-330_001 >> 227_001, 009_001
    # pidMax=18, wc=0.3713)  # 005_001-011_001 >> 227_001
    # pidMax=17, wc=0.3)  # 227_001-330_001 >> 009_001
    # pidMax=20, wc=0.362)  # 226_001-330_001 >> 227_001