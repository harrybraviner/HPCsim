function ufinal = recombineSolution(u, physicalNodes, computationalNodes)
% This function removes the duplicated values that 'have been copied between computational nodes'.
% where u is the computed solution.
    npN = ceil(physicalNodes/computationalNodes);

    ufinal = u(1:npN);
    for i=1:computationalNodes-2
        firstCell = i*(npN+2);
        ufinal = [ufinal; u(firstCell + (1:npN))];
    end
    if computationalNodes>1
        firstCell = (computationalNodes-1)*(npN+2);
        ufinal = [ufinal; u(firstCell+1:end)];
    end

end
