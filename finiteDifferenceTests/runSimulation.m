function [x, u] = runSimulation(computationalNodes, a, a0, b, frames)
%Finte difference scheme to solve the equation:
%u_t + au_x +a0 u_x = b u_xx
%where
%a is solved with central difference advection, and
%a0 is solved with upwinding difference advection

%equations
    physicalNodes=100;
    deltax = 1.0;
    %a = 0;
    %a0 = 0;
    %b = 1;

%optimal time step
    tmax = numericalStability(@(t)constructMatrix(physicalNodes, computationalNodes, deltax, t, b, a, a0));
    fudge = 0.7; %fudge factor to bring time step back from maximum.
    t = fudge*tmax;

%construct matrix
    A = constructMatrix(physicalNodes, computationalNodes, deltax, t, b, a, a0);

%construct initial condition
    u = zeros((computationalNodes-1)*2 + physicalNodes,1);
    u(1) = 1;

%run computation
    Nt = 10000/t;
    ufinal = transpose(recombineSolution(u, physicalNodes, computationalNodes));
    for i = 1:Nt
        u = A*u;
        if abs(mod(i*t,10000/frames))<t/2
            ufinal = [ufinal; transpose(recombineSolution(u, physicalNodes, computationalNodes))];
        end
    end

%reduce solution
x = 0:deltax:physicalNodes-1;
u = ufinal;

end
