include("GLNS.jl")

using  DataFrames, CSV
DataFrames_ = DataFrames;
function mkdire_(dire_)
	if !isdir(dire_)
		mkdir(dir_)
	end
end

ranges = 20:5:60
kk = 5
mm = 3
# print("k ", kk, " m ", mm,"\n")
# k_m = "k_" * string(kk) * "_m_" * string(mm)
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

function write_res(ins, n,k,m,obj)

	df = DataFrames_.DataFrame(ins=ins, n=n,k=k,m=m,obj=obj)

    CSV.write("res.csv", df, append=true)
end

function runGTSPApx(ins_folder, ins_name)
    scale = 1000
	ins_na = "\n\n\n"*ins_name
	println(ins_na)

	ins_info = split(ins_name,"_")
	nn = parse(Int, ins_info[end-2])
	kk = parse(Int, ins_info[end-1])
	mm = parse(Int, split(ins_info[end],".")[1])
	sol_obj = 0
	divided = mm * sqrt(2 * nn / kk)
	for iter = 1:itera
		ret = GLNS.solver(ins_folder* ins_name, mode = "fast")
		sol_obj += ret[1]/scale
	end
	sol_obj = sol_obj / itera
	println("obj = $sol_obj \n")
	retVal = sol_obj / divided
	println("normed_obj = $retVal \n")
	write_res(ins_name, nn,kk,mm,sol_obj)

end

if size(ARGS)[1]>0
	ins_folder = ARGS[1]
	ins_name = ARGS[2]
	runGTSPApx(ins_folder, ins_name)
	exit()
end

function runGTSPApx_folder()
    for ins in readdir(ins_folder)
		runGTSPApx(ins_folder, ins)
    end
end
runGTSPApx_folder()




