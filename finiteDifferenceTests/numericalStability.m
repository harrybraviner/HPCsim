function t = numericalStability(constructMatrix)
    %numericalStability checks the stability of a finite difference array by 
    %applying a nonlinear constrained minimiser to find the maximum time step
    %while ensuring absolute value of eigen values less than one.
    %constructMatrix is a function that takes delta t

        %Bounded minimisation requires a range for maximum time step to search in.
        dtb = [0.01,21.0]; %delta t bounds
    
        %maximise time step 
        objfun = @(t) -t;
        %subject to constraint
        nlcon = @(x)mycon(x, @(t)constructMatrix(t));
        %perform minimisation
        t = fmincon(objfun,1.1,[],[],[],[],dtb(1), dtb(2),nlcon);

        %display results
        disp(['Maximum time step: ', num2str(dtb(1)), '< ', num2str(t), ' <', num2str(dtb(2))]);
        %error if time step less than minimum search bond
        assert(abs(dtb(1) - t)>1e-8)
        %warning if time step greater than maximum search bond.
        if abs(dtb(2) - t)<1e-12
            disp('WARNING: time step has reached the upper limit')
        end
end

function [c,ceq] = mycon(x, conMatr)
    %Constraint that absolute value of eigen functions are less than one.
    c = max(abs(eig(conMatr(x))))-1;  % Compute nonlinear inequalities at x.
    ceq = [];   % Compute nonlinear equalities at x.
end
