include("GLNS.jl")

ranges = 20:5:60
kk = 5
mm = 3
print("k ", kk, " m ", mm,"\n")
k_m = "k_" * string(kk) * "_m_" * string(mm)
itera = 5

function runSimulation()
    scale = 1000
    for num_clusters = ranges
        for iter = 1:2
            file_name = "F:/Acad/research/Carlsson/GLNS/TPP_results/result_$num_clusters" * "_" * "$iter.txt"
            instance_name = "GLNSLIB/input_" * string(num_clusters) * "_" * string(iter) * ".gtsp"
            ret = GLNS.solver("$instance_name", mode = "slow")
            sol_obj = ret[1]/scale
            sol_time = ret[2]
            f = open(file_name, "w")
            write(f, "Optimal Objective: $sol_obj \r\n")
            write(f, "Solution Time: $sol_time \r\n")
            close(f)
        end
    end
end
# runSimulation()

function runProofTest()
    scale = 1000
    file_name = "F:/Acad/research/Carlsson/GLNS/TPP_proof/result" * k_m * ".txt"
    f = open(file_name, "w")
    for num_clusters = ranges
        println("num_clusters = $num_clusters")
        sol_obj = 0
        divided = mm * sqrt(2 * num_clusters / kk)
        for iter = 1:itera
            instance_name = "PROOFLIB_" * k_m *"/input_" * string(num_clusters) * "_" * string(iter) * ".gtsp"
            ret = GLNS.solver("$instance_name", mode = "slow")
            sol_obj += ret[1]/scale
        end
        sol_obj = sol_obj / itera
        println("obj = $sol_obj")
        retVal = sol_obj / divided
        println("normed_obj = $retVal")
        write(f, "$retVal,")
    end
    close(f)
end
runProofTest()
