include("GLNS.jl")

function mkdire_(dire_)
	if !isdir(dire_)
		mkdir(dir_)
	end
end

ranges = 20:5:60
kk = 5
mm = 3
print("k ", kk, " m ", mm,"\n")
k_m = "k_" * string(kk) * "_m_" * string(mm)
itera = 5
ins_folder = "GLNSLIB_RANDOM_TPP/"

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
    file_name = "result" * k_m * ".txt"
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
# runProofTest()


function runGTSPApx()
    scale = 1000
    file_name = "result.txt"
    f = open(file_name, "w")
    for ins in readdir(ins_folder)
        println(ins*"\n")
        ins_info = split(ins,"_")
        nn = parse(Int, ins_info[end-2])
        kk = parse(Int, ins_info[end-1])
        mm = parse(Int, split(ins_info[end],".")[1])

        sol_obj = 0
        divided = mm * sqrt(2 * nn / kk)
        for iter = 1:itera
            ret = GLNS.solver(ins_folder* ins, mode = "fast")
            sol_obj += ret[1]/scale
        end
        sol_obj = sol_obj / itera
        println("obj = $sol_obj \n")
        retVal = sol_obj / divided
        println("normed_obj = $retVal \n")
        write(f, "$retVal,")
    end
    close(f)
end
runGTSPApx()