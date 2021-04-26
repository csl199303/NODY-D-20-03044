import networkx as ne #导入建网络模型包，命名ne


for N in [10000]:
    for k in [14,16,18,20]:
        for p in [0.1]:
            ws=ne.watts_strogatz_graph(N,k,p)
            ne.write_gml(ws,'N_'+str(N)+'_p_'+str(p)+'_k_'+str(k)+'.gml')